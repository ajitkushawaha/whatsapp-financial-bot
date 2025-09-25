from dotenv import load_dotenv
import os
import pandas as pd
import time
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from config import GEMINI_MODEL
import json
import re
from termcolor import cprint
from csv_operation import read_queries, write_response

# Import database functions
from add_data_in_database import add_user, add_interaction, TransactionType


class GeminiChat:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        os.environ["GOOGLE_API_KEY"] = self.api_key  # Required by LangChain for Gemini
        self.model_name = GEMINI_MODEL

        self.chat_model = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=0.7,
            max_tokens=512
        )

    def extract_json(self, text):
        try:
            # Remove markdown-style code blocks (```json ... ```)
            cleaned_text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE).strip()
            obj = json.loads(cleaned_text)
            return obj
        except Exception as e:
            print(f"Failed to extract JSON: {e}")
            print(f"Raw Gemini output:\n{text}")
        return None

    def get_response(self, user_message: str) -> str:
        system_prompt = """
                        You are an intelligent assistant for a financial tracker bot.

Classify the user message into one of the following intents:
1. `greeting`: Greetings, thanks, or social niceties.
2. `transaction`: Reports one or more completed financial activities.
3. `information`: Questions about spending, budgeting, or advice.
4. `out_of_context`: Irrelevant to finance or the bot.

Return ONLY one JSON object:
- For `greeting`, `information`, or `out_of_context`: return {"intent": {}, e.g., "greeting": {}}
- For `transaction`: return as
{
  "transaction": [
    {
      "transaction_type": "Debit" or "Credit",
      "amount": number or null,
      "category_name": general purpose (e.g. Food, Transport),
      "subcategory_name": specific use (e.g. Taxi, Groceries),
      "transaction_date": "YYYY-MM-DD" (today = 2025-05-31)
    },
    ...
  ]
}
No markdown, no explanation.
                        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]

        while True:
            try:
                response = self.chat_model.invoke(messages)
                extracted_data = self.extract_json(response.content)
                return extracted_data
            except Exception as e:
                if "ResourceExhausted" in str(e):
                    print("Rate limit hit. Waiting 60 seconds before retrying...")
                    time.sleep(60)
                else:
                    return f"error: {str(e)}"

    def process_and_store_message(self, user_message: str, whatsapp_number: str = None):
        """
        Process user message and store in database
        """
        # Get or create user
        if whatsapp_number:
            user_id = add_user(whatsapp_number)
        else:
            # For console testing, use a default number
            user_id = add_user("console_user")
        
        if user_id is None:
            print("Failed to get/create user")
            return None

        # Get AI response
        ai_response = self.get_response(user_message)
        cprint(ai_response, "blue")
        
        if isinstance(ai_response, str) and ai_response.startswith("error:"):
            # Store error interaction
            add_interaction(user_id, user_message)
            return ai_response
        
        if ai_response is None:
            add_interaction(user_id, user_message)
            return "Failed to process message"

        # Process based on intent
        if "transaction" in ai_response:
            transactions = ai_response["transaction"]
            for transaction in transactions:
                # Convert transaction_type string to enum
                transaction_type_enum = None
                if transaction.get("transaction_type"):
                    if transaction["transaction_type"] == "Debit":
                        transaction_type_enum = TransactionType.Debit
                    elif transaction["transaction_type"] == "Credit":
                        transaction_type_enum = TransactionType.Credit

                # Convert date string to date object
                transaction_date = None
                if transaction.get("transaction_date"):
                    try:
                        transaction_date = datetime.strptime(
                            transaction["transaction_date"], "%Y-%m-%d"
                        ).date()
                    except ValueError:
                        print(f"Invalid date format: {transaction['transaction_date']}")

                # Store interaction in database
                add_interaction(
                    user_id=user_id,
                    message_text=user_message,
                    transaction_type=transaction_type_enum,
                    amount=transaction.get("amount"),
                    category_name=transaction.get("category_name"),
                    subcategory_name=transaction.get("subcategory_name"),
                    transaction_date=transaction_date
                )
            
            return f"Stored {len(transactions)} transaction(s) successfully!"
        
        else:
            # Do not store non-transaction messages
            intent_type = list(ai_response.keys())[0] if ai_response else "unknown"
            return f"Message processed as: {intent_type} (not stored)"


def interactive_console():
    """
    Interactive console for testing
    """
    chat = GeminiChat()
    
    print("=== Financial Tracker Chat (Database Enabled) ===")
    print("Type 'exit' or 'quit' to stop")
    print("Enter your WhatsApp number (optional, press Enter to skip):")
    
    whatsapp_number = input("WhatsApp Number: ").strip()
    if not whatsapp_number:
        whatsapp_number = "console_user"
    
    print(f"\n--- Chat started for user: {whatsapp_number} ---\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        
        if not user_input:
            continue
            
        result = chat.process_and_store_message(user_input, whatsapp_number)
        cprint(f"Result: {result}", "green")


def batch_process_csv():
    """
    Process CSV file and store results in database
    """
    chat = GeminiChat()
    df = read_queries()

    for idx, row in df.iterrows():
        if pd.notna(row.get("response", "")) and row["response"].strip() != "":
            continue  # Skip already processed entries

        user_input = row["user_input"]
        whatsapp_number = row.get("whatsapp_number", "csv_user")  # Get from CSV or default
        
        print(f"Processing [{idx}]: {user_input[:60]}...")

        try:
            result = chat.process_and_store_message(user_input, whatsapp_number)
            df.at[idx, "response"] = result
        except Exception as e:
            df.at[idx, "response"] = f"error: {str(e)}"

        # Save after each update to avoid losing progress
        write_response(df)

        # Optional delay to avoid rate limiting
        time.sleep(4)


if __name__ == "__main__":
    # Choose mode
    print("Choose mode:")
    print("1. Interactive Console")
    print("2. Batch Process CSV")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        interactive_console()
    elif choice == "2":
        batch_process_csv()
    else:
        print("Invalid choice. Starting interactive console...")
        interactive_console()