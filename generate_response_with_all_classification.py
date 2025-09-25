# from dotenv import load_dotenv
# import os
# import pandas as pd
# import time
# from datetime import datetime

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# from config import GEMINI_MODEL
# import json
# import re
# from termcolor import cprint
# from csv_operation import read_queries, write_response
# from datetime import date, timedelta
# import sys
# from termcolor import cprint

# # Import database functions
# from add_data_in_database import get_user_financial_data, add_user, add_interaction, TransactionType
# from weekly_report import WeeklyReport
# from transaction_history import TransactionHistory

# class GeminiChat:
#     def __init__(self):
#         load_dotenv()
#         self.api_key = os.getenv("GEMINI_API_KEY")
#         os.environ["GOOGLE_API_KEY"] = self.api_key  # Required by LangChain for Gemini
#         self.model_name = GEMINI_MODEL

#         self.chat_model = ChatGoogleGenerativeAI(
#             model=self.model_name,
#             temperature=0.7,
#             max_tokens=512
#         )
#         self.today = date.today()
#         print(self.today)

#         self.weekReport_obj = WeeklyReport(self.chat_model)
#         self.transactionHistory_obj = TransactionHistory(self.chat_model)

#     def extract_json(self, text):
#         try:
#             cleaned_text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE).strip()
#             match = re.search(r'\{[\s\S]*\}', cleaned_text)
#             if match:
#                 json_str = match.group(0)
#                 obj = json.loads(json_str)
#                 return obj
#             else:
#                 print("No valid JSON object found.")
#         except Exception as e:
#             print(f"Failed to extract JSON: {e}")
#             print(f"Raw Gemini output:\n{text}")
#         return None

#     def get_response(self, user_message: str) -> str:
#         today_date = "2025-05-31"

#         system_prompt = f"""
#     You are an intelligent assistant for a financial tracker bot.

#     Today's date is {self.today}.

#     Classify the user message into one of the following intents:
#     1. `greeting`: Greetings, thanks, or social niceties.
#     2. `transaction`: Reports one or more completed financial activities.
#     3. `transaction_history`: Questions about spending, budgeting, or advice.
#     4. `out_of_context`: Irrelevant to finance or the bot.

#     First detect the language of the user message. Then generate the response in that same language (do NOT guess or change it).
#     Always ensure the `response` field is in the same language as the original user message. If the user speaks in English, respond in English. If the user speaks in another language, match it exactly.
#     Return ONLY the JSON object as per the intent structure.
#     Your reply should be short, natural, and human-like.

#     Return ONLY one JSON object in the format below:

#     - For `greeting`, `information`, or `out_of_context`:
#     {{
#         "intent": "greeting" | "information" | "out_of_context",
#         "response": "<reply in user's language>",
#         "translated_message": "<user message translated to English>"
#     }}

#     - For `transaction`:
#     {{
#         "intent": "transaction",
#         "response": "<acknowledgment in user's language>",
#         "translated_message": "<user message translated to English>",
#         "transaction": [
#             {{
#                 "transaction_type": "Debit" or "Credit",
#                 "amount": number or null,
#                 "category_name": general purpose (e.g. Food, Transport),
#                 "subcategory_name": specific use (e.g. Taxi, Groceries),
#                 "transaction_date": "{today_date}"
#             }},
#             ...
#         ]
#     }}

#     - For `transaction_history`, if the message includes a time duration (e.g., "last month", "last week", "last to last week", etc.), include the start and end date:
#     {{
#         "intent": "transaction_history",
#         "response": "<reply in user's language>",
#         "translated_message": "<user message translated to English>",
#         "start_date": "YYYY-MM-DD",  # Start of the period
#         "end_date": "YYYY-MM-DD"     # End of the period
#     }}

#     Ensure:
#     - All transaction fields are in English.
#     - The "translated_message" is a faithful English translation of the user input.
#     - Return only the JSON object. No markdown or explanation.
#     """

#         messages = [
#             SystemMessage(content=system_prompt),
#             HumanMessage(content=user_message)
#         ]

#         while True:
#             try:
#                 response = self.chat_model.invoke(messages)
#                 response_text = response.content.strip()
#                 extracted_data = self.extract_json(response_text)
#                 return extracted_data
#             except Exception as e:
#                 if "ResourceExhausted" in str(e):
#                     print("Rate limit hit. Waiting 60 seconds before retrying...")
#                     time.sleep(60)
#                 else:
#                     return f"error: {str(e)}"

#     def check_and_run_report_condition(self, user_id: int, user_message: str = None):
#         today = date.today()
#         is_sunday = today.weekday() == 6  # Sunday = 6
#         is_first = today.day == 1

#         if is_sunday:
#             # Get the date of the previous Sunday (7 days ago)
#             last_sunday = today - timedelta(days=7)
#             last_saturday = last_sunday + timedelta(days=6)
            
#             report = self.weekReport_obj.generate_report(user_id, last_sunday, last_saturday)
#             return report
#             # return True

#         # elif is_first:
#         #     # Get the previous month's start and end date
#         #     first_day_of_current_month = today.replace(day=1)
#         #     last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
#         #     first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
#         #     run_monthly_report(user_id, start_date=first_day_of_previous_month, end_date=last_day_of_previous_month)
#         #     return True

#         elif user_message.lower() == "report":
#             start_date = "2025-07-05"
#             end_date = "2025-07-11"
#             print("------------------ date ------------------")
#             print(start_date)
#             print(end_date)
#             report = self.weekReport_obj.generate_report(user_id, start_date, end_date)
#             return report
#             # return True

#         return False

#     def process_and_store_message(self, user_message: str, user_id: int):

#         ai_response = self.get_response(user_message)
#         cprint(ai_response, "blue")

#         if isinstance(ai_response, str) and ai_response.startswith("error:"):
#             translated_msg = ai_response.get("translated_message", user_message)
#             # add_interaction(user_id, translated_msg)
#             return ai_response

#         if ai_response is None:
#             translated_msg = ai_response.get("translated_message", user_message)
#             # add_interaction(user_id, translated_msg)
#             return "Failed to process message"

         
#         if ai_response["intent"] == "greeting":
#             if "response" in ai_response:
#                 cprint(f"Gemini Response: {ai_response['response']}", "cyan")
#             return ai_response['response']

#         elif ai_response["intent"] == "transaction":
#             if "response" in ai_response:
#                 cprint(f"Gemini Response: {ai_response['response']}", "cyan")
#             if "transaction" in ai_response:
#                 transactions = ai_response["transaction"]
#                 for transaction in transactions:
#                     transaction_type_enum = None
#                     if transaction.get("transaction_type"):
#                         if transaction["transaction_type"] == "Debit":
#                             transaction_type_enum = TransactionType.Debit
#                         elif transaction["transaction_type"] == "Credit":
#                             transaction_type_enum = TransactionType.Credit

#                     transaction_date = None
#                     if transaction.get("transaction_date"):
#                         try:
#                             transaction_date = datetime.strptime(
#                                 transaction["transaction_date"], "%Y-%m-%d"
#                             ).date()
#                         except ValueError:
#                             print(f"Invalid date format: {transaction['transaction_date']}")

#                     translated_msg = ai_response.get("translated_message", user_message)
#                     add_interaction(
#                         user_id=user_id,
#                         message_text=translated_msg,
#                         transaction_type=transaction_type_enum,
#                         amount=transaction.get("amount"),
#                         category_name=transaction.get("category_name"),
#                         subcategory_name=transaction.get("subcategory_name"),
#                         transaction_date=transaction_date
#                     )

#                 return f"Stored {len(transactions)} transaction(s) successfully!"
#             else:
#                 intent_type = list(ai_response.keys())[0] if ai_response else "unknown"
#                 return f"Message processed as: {intent_type} (not stored)"

#         elif ai_response["intent"] == "transaction_history":
#             # if "response" in ai_response:
#             #     cprint(f"Gemini Response: {ai_response['response']}", "cyan")
            
#             start_date = ai_response.get("start_date")
#             end_date = ai_response.get("end_date")
#             result = self.transactionHistory_obj.generate_report(user_id, start_date, end_date, ai_response["translated_message"])
#             return result
#         elif ai_response["intent"] == "out_of_context":
#             if "response" in ai_response:
#                 cprint(f"Gemini Response: {ai_response['response']}", "cyan")

#             return ai_response['response']


# if __name__ == "__main__":
#     chat = GeminiChat()

#     print("=== Financial Tracker Chat (Database Enabled) ===")
#     print("Type 'exit' or 'quit' to stop")

#     whatsapp_number = input("Enter your WhatsApp number (optional, press Enter to skip): ").strip()
#     if not whatsapp_number:
#         whatsapp_number = "console_user"

#     print(f"\n--- Chat started for user: {whatsapp_number} ---\n")

#     user_id = add_user(whatsapp_number)
#     if user_id is None:
#         print("❌ Failed to get or create user. Exiting.")
#         sys.exit(1)

#     # report = chat.check_and_run_report_condition(user_id, "report")
#     # if report:
#     #     print(report)
#     #     sys.exit(0)

#     while True:
#         user_input = input("You: ").strip()
#         if user_input.lower() in {"exit", "quit"}:
#             print("👋 Exiting the chat. Goodbye!")
#             break

#         if not user_input:
#             continue

#         result = chat.process_and_store_message(user_input, user_id)
#         cprint(f"Result: {result}", "green")



""" chat history """

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
from datetime import date, timedelta
import sys
from termcolor import cprint

# Import database functions
from add_data_in_database import get_user_financial_data, add_user, add_interaction, TransactionType
from weekly_report import WeeklyReport
from transaction_history import TransactionHistory

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
        self.today = date.today()
        print(self.today)

        self.weekReport_obj = WeeklyReport(self.chat_model)
        self.transactionHistory_obj = TransactionHistory(self.chat_model)
        
        # Initialize chat history storage for each user
        self.chat_histories = {}  # {user_id: [messages]}
        self.max_history_length = 20  # Keep last 20 messages to avoid token limits

    def get_chat_history(self, user_id: int):
        """Get chat history for a specific user"""
        return self.chat_histories.get(user_id, [])

    def add_to_chat_history(self, user_id: int, message):
        """Add a message to user's chat history"""
        if user_id not in self.chat_histories:
            self.chat_histories[user_id] = []
        
        self.chat_histories[user_id].append(message)
        
        # Keep only the last N messages to avoid token limit issues
        if len(self.chat_histories[user_id]) > self.max_history_length:
            self.chat_histories[user_id] = self.chat_histories[user_id][-self.max_history_length:]

    def clear_chat_history(self, user_id: int):
        """Clear chat history for a specific user"""
        if user_id in self.chat_histories:
            del self.chat_histories[user_id]

    def extract_json(self, text):
        try:
            cleaned_text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE).strip()
            match = re.search(r'\{[\s\S]*\}', cleaned_text)
            if match:
                json_str = match.group(0)
                obj = json.loads(json_str)
                return obj
            else:
                print("No valid JSON object found.")
        except Exception as e:
            print(f"Failed to extract JSON: {e}")
            print(f"Raw Gemini output:\n{text}")
        return None

    def get_response(self, user_message: str, user_id: int) -> str:
        today_date = self.today.strftime("%Y-%m-%d")

        # Get chat history for context
        chat_history = self.get_chat_history(user_id)
        
        # Create context from chat history
        history_context = ""
        if chat_history:
            history_context = "\n\nCONVERSATION HISTORY (for context):\n"
            for msg in chat_history[-10:]:  # Last 10 messages for context
                if isinstance(msg, HumanMessage):
                    history_context += f"User: {msg.content}\n"
                elif isinstance(msg, AIMessage):
                    history_context += f"Assistant: {msg.content}\n"

        system_prompt = f"""
    You are an intelligent assistant for a financial tracker bot.

    Today's date is {self.today}.

    Classify the user message into one of the following intents:
    1. `greeting`: Greetings, thanks, or social niceties.
    2. `transaction`: Reports one or more completed financial activities.
    3. `transaction_history`: Questions about spending, budgeting, financial advice, or requests for transaction data.
    4. `out_of_context`: Irrelevant to finance or the bot (like questions about bitcoin, weather, etc.).

    IMPORTANT CLASSIFICATION RULES:
    - Questions about "what transactions", "show expenses", "spending report" = transaction_history
    - Questions about cryptocurrency, general knowledge, non-finance topics = out_of_context
    - "I spent/earned/paid" statements = transaction
    - Greetings, thanks = greeting

    For transaction_history queries, automatically determine reasonable date ranges:
    - "this week" or "recent" or "latest" = last 7 days
    - "this month" = current month
    - "last month" = previous month
    - If no timeframe specified, default to last 30 days

    Return ONLY one JSON object in the format below:

    - For `greeting`, `out_of_context`:
    {{
        "intent": "greeting" | "out_of_context",
        "response": "<reply in user's language>",
        "translated_message": "<user message translated to English>"
    }}

    - For `transaction`:
    {{
        "intent": "transaction",
        "response": "<acknowledgment in user's language>",
        "translated_message": "<user message translated to English>",
        "transaction": [
            {{
                "transaction_type": "Debit" or "Credit",
                "amount": number or null,
                "category_name": general purpose (e.g. Food, Transport),
                "subcategory_name": specific use (e.g. Taxi, Groceries),
                "transaction_date": "{today_date}"
            }}
        ]
    }}

    - For `transaction_history`:
    {{
        "intent": "transaction_history",
        "response": "<reply in user's language>",
        "translated_message": "<user message translated to English>",
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD"
    }}

    Return only the JSON object. No markdown or explanation.
    """

        # Build messages with history
        messages = [SystemMessage(content=system_prompt)]
        
        # Add recent chat history for better context (last 6 messages)
        recent_history = chat_history[-6:] if len(chat_history) > 6 else chat_history
        messages.extend(recent_history)
        
        # Add current user message
        messages.append(HumanMessage(content=user_message))

        while True:
            try:
                response = self.chat_model.invoke(messages)
                response_text = response.content.strip()
                extracted_data = self.extract_json(response_text)
                return extracted_data
            except Exception as e:
                if "ResourceExhausted" in str(e):
                    print("Rate limit hit. Waiting 60 seconds before retrying...")
                    time.sleep(60)
                else:
                    return f"error: {str(e)}"

    def check_and_run_report_condition(self, user_id: int, user_message: str = None):
        today = date.today()
        is_sunday = today.weekday() == 6  # Sunday = 6
        is_first = today.day == 1
        print("------------------ date ------------------")
        print(today)

        if is_sunday:
            # Get the date of the previous Sunday (7 days ago)
            last_sunday = today - timedelta(days=7)
            last_saturday = last_sunday + timedelta(days=6)
            
            report = self.weekReport_obj.generate_report(user_id, last_sunday, last_saturday)
            return report

        elif user_message and user_message.lower() == "report":
            start_date = "2025-07-05"
            end_date = "2025-07-11"
            print("------------------ date ------------------")
            print(start_date)
            print(end_date)
            report = self.weekReport_obj.generate_report(user_id, start_date, end_date)
            return report

        return False

    def get_last_ai_response(self, user_id: int):
        """Get the last AI response from chat history"""
        chat_history = self.get_chat_history(user_id)
        for msg in reversed(chat_history):
            if isinstance(msg, AIMessage):
                return msg.content
        return "I don't have any previous response to repeat."

    def process_and_store_message(self, user_message: str, user_id: int):
        # Add user message to chat history
        self.add_to_chat_history(user_id, HumanMessage(content=user_message))

        ai_response = self.get_response(user_message, user_id)
        cprint(ai_response, "blue")

        if isinstance(ai_response, str) and ai_response.startswith("error:"):
            error_msg = f"Sorry, I encountered an error: {ai_response}"
            self.add_to_chat_history(user_id, AIMessage(content=error_msg))
            return error_msg

        if ai_response is None:
            error_msg = "Failed to process message"
            self.add_to_chat_history(user_id, AIMessage(content=error_msg))
            return error_msg

        response_text = ""

        if ai_response["intent"] == "greeting":
            if "response" in ai_response:
                cprint(f"Gemini Response: {ai_response['response']}", "cyan")
                response_text = ai_response['response']

        elif ai_response["intent"] == "contextual_query":
            if "response" in ai_response:
                cprint(f"Contextual Response: {ai_response['response']}", "cyan")
                response_text = ai_response['response']
                
                # Handle specific contextual actions
                context_action = ai_response.get("context_action", "general_context")
                if context_action == "repeat_last":
                    last_response = self.get_last_ai_response(user_id)
                    if last_response and last_response != response_text:
                        response_text = f"{response_text}\n\nHere's what I said before:\n{last_response}"

        elif ai_response["intent"] == "transaction":
            if "response" in ai_response:
                cprint(f"Gemini Response: {ai_response['response']}", "cyan")
                response_text = ai_response['response']
                
            if "transaction" in ai_response:
                transactions = ai_response["transaction"]
                for transaction in transactions:
                    transaction_type_enum = None
                    if transaction.get("transaction_type"):
                        if transaction["transaction_type"] == "Debit":
                            transaction_type_enum = TransactionType.Debit
                        elif transaction["transaction_type"] == "Credit":
                            transaction_type_enum = TransactionType.Credit

                    transaction_date = None
                    if transaction.get("transaction_date"):
                        try:
                            transaction_date = datetime.strptime(
                                transaction["transaction_date"], "%Y-%m-%d"
                            ).date()
                        except ValueError:
                            print(f"Invalid date format: {transaction['transaction_date']}")

                    translated_msg = ai_response.get("translated_message", user_message)
                    add_interaction(
                        user_id=user_id,
                        message_text=translated_msg,
                        transaction_type=transaction_type_enum,
                        amount=transaction.get("amount"),
                        category_name=transaction.get("category_name"),
                        subcategory_name=transaction.get("subcategory_name"),
                        transaction_date=transaction_date
                    )

                success_msg = f"Stored {len(transactions)} transaction(s) successfully!"
                response_text = f"{response_text}\n{success_msg}" if response_text else success_msg

        elif ai_response["intent"] == "transaction_history":
            start_date = ai_response.get("start_date")
            end_date = ai_response.get("end_date")
            
            # If no dates provided, default to last 30 days
            if not start_date or not end_date:
                end_date = self.today.strftime("%Y-%m-%d")
                start_date = (self.today - timedelta(days=30)).strftime("%Y-%m-%d")
            
            result = self.transactionHistory_obj.generate_report(user_id, start_date, end_date, ai_response["translated_message"])
            response_text = result

        elif ai_response["intent"] == "out_of_context":
            if "response" in ai_response:
                cprint(f"Gemini Response: {ai_response['response']}", "cyan")
                response_text = ai_response['response']

        # Add AI response to chat history
        if response_text:
            self.add_to_chat_history(user_id, AIMessage(content=response_text))

        return response_text


if __name__ == "__main__":
    chat = GeminiChat()

    print("=== Financial Tracker Chat with History (Database Enabled) ===")
    print("Type 'exit' or 'quit' to stop")
    print("Type 'clear' to clear chat history")
    print("Type 'history' to see chat history")

    whatsapp_number = input("Enter your WhatsApp number (optional, press Enter to skip): ").strip()
    if not whatsapp_number:
        whatsapp_number = "console_user"

    print(f"\n--- Chat started for user: {whatsapp_number} ---\n")

    user_id = add_user(whatsapp_number)
    if user_id is None:
        print("❌ Failed to get or create user. Exiting.")
        sys.exit(1)

    report = chat.check_and_run_report_condition(user_id, "report")
    if report:
        print(report)
        sys.exit(0)

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Exiting the chat. Goodbye!")
            break

        if user_input.lower() == "clear":
            chat.clear_chat_history(user_id)
            print("🗑️ Chat history cleared!")
            continue

        if user_input.lower() == "history":
            history = chat.get_chat_history(user_id)
            if history:
                print("\n📝 Chat History:")
                print("-" * 40)
                for i, msg in enumerate(history[-10:], 1):  # Show last 10 messages
                    if isinstance(msg, HumanMessage):
                        print(f"{i}. You: {msg.content}")
                    elif isinstance(msg, AIMessage):
                        print(f"{i}. Bot: {msg.content}")
                print("-" * 40)
            else:
                print("📭 No chat history found.")
            continue

        if not user_input:
            continue

        result = chat.process_and_store_message(user_input, user_id)
        cprint(f"Bot: {result}", "green")