#!/usr/bin/env python3
"""
Enhanced Financial Bot with Google Search Grounding and Better Responses
"""

from dotenv import load_dotenv
import os
import pandas as pd
import time
from datetime import datetime, date, timedelta

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from config import GEMINI_MODEL
import json
import re
from termcolor import cprint
from csv_operation import read_queries, write_response

# Import database functions
from add_data_in_database import get_user_financial_data, add_user, add_interaction, TransactionType

# Import Google AI for grounding
import google.generativeai as genai
from google.generativeai import types

class EnhancedFinancialBot:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        os.environ["GOOGLE_API_KEY"] = self.api_key
        self.model_name = GEMINI_MODEL

        # LangChain model for main classification
        self.chat_model = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=0.7,
            max_tokens=512
        )
        
        # Google AI client for grounding
        genai.configure(api_key=self.api_key)
        self.google_client = genai
        
        self.today = date.today()
        print(f"Bot initialized for date: {self.today}")

        # Initialize chat history storage for each user
        self.chat_histories = {}
        self.max_history_length = 20

    def get_chat_history(self, user_id: int):
        """Get chat history for a specific user"""
        return self.chat_histories.get(user_id, [])

    def add_to_chat_history(self, user_id: int, message):
        """Add a message to user's chat history"""
        if user_id not in self.chat_histories:
            self.chat_histories[user_id] = []
        
        self.chat_histories[user_id].append(message)
        
        if len(self.chat_histories[user_id]) > self.max_history_length:
            self.chat_histories[user_id] = self.chat_histories[user_id][-self.max_history_length:]

    def clear_chat_history(self, user_id: int):
        """Clear chat history for a specific user"""
        if user_id in self.chat_histories:
            del self.chat_histories[user_id]
            return "Chat history cleared, buddy! 🧹 Fresh start!"
        return "No chat history to clear, buddy! 📝"

    def get_chat_summary(self, user_id: int) -> str:
        """Get a summary of recent chat history"""
        chat_history = self.get_chat_history(user_id)
        
        if not chat_history:
            return "No chat history found, buddy! This is a fresh conversation. 💬"
        
        user_messages = [msg.content for msg in chat_history if isinstance(msg, HumanMessage)]
        ai_messages = [msg.content for msg in chat_history if isinstance(msg, AIMessage)]
        
        return f"Chat Summary:\n📝 Total messages: {len(chat_history)}\n👤 Your messages: {len(user_messages)}\n🤖 My responses: {len(ai_messages)}\n💬 Last message: {chat_history[-1].content[:100]}..."

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
            print(f"Raw output:\n{text}")
        return None

    def classify_user_intent(self, user_message: str, user_id: int):
        """Classify user intent and extract relevant information"""
        
        # Get chat history for context
        chat_history = self.get_chat_history(user_id)
        
        # Create context from recent chat history
        history_context = ""
        if chat_history:
            history_context = "\n\nRECENT CONVERSATION HISTORY (for context):\n"
            for msg in chat_history[-10:]:  # Last 10 messages for context
                if isinstance(msg, HumanMessage):
                    history_context += f"User: {msg.content}\n"
                elif isinstance(msg, AIMessage):
                    # Truncate long AI responses for context
                    content = msg.content[:200] + "..." if len(msg.content) > 200 else msg.content
                    history_context += f"Assistant: {content}\n"
        
        system_prompt = f"""
You are an intelligent classifier for a financial tracker bot.

Today's date is {self.today}.

IMPORTANT: Use the conversation history below to understand context and follow-up questions.
{history_context}

Classify the user message into one of the following intents:
1. `greeting`: Greetings, thanks, or social niceties.
2. `transaction`: Reports one or more completed financial activities (I spent, I earned, I paid, etc.).
3. `transaction_history`: Questions about personal spending, transaction data, financial reports.
4. `financial_info`: General financial questions that require web search (crypto rates, stock prices, market info, financial advice, definitions).
5. `follow_up`: Questions that refer to previous conversation (like "what about last month?", "show me more", "explain that", "what do you mean?").
6. `out_of_context`: Completely irrelevant to finance.

IMPORTANT CLASSIFICATION RULES:
- "I spent/earned/paid/bought" = transaction
- "What did I spend", "show my expenses", "my transactions" = transaction_history  
- "What is crypto", "gold rate", "stock price", "financial advice" = financial_info
- "What about...", "show me more", "explain", "what do you mean" = follow_up
- Weather, sports, general knowledge = out_of_context

For transaction_history: Extract date ranges from the message:
- If user mentions specific dates/ranges, extract them
- If no date mentioned, set both start_date and end_date as null (fetch ALL transactions)
- "this week" = last 7 days, "this month" = current month, etc.

For follow_up: Identify what the user is referring to based on conversation history.

Return ONLY a JSON object:

For greeting/out_of_context:
{{
    "intent": "greeting" | "out_of_context",
    "response": "Brief response"
}}

For transaction:
{{
    "intent": "transaction",
    "transactions": [
        {{
            "transaction_type": "Debit" | "Credit",
            "amount": number,
            "category_name": "Food" | "Transport" | "Entertainment" | etc,
            "subcategory_name": "specific item/service",
            "transaction_date": "{self.today.strftime('%Y-%m-%d')}"
        }}
    ]
}}

For transaction_history:
{{
    "intent": "transaction_history",
    "query_type": "expenses" | "income" | "report" | "category_wise" | "general",
    "start_date": "YYYY-MM-DD" | null,
    "end_date": "YYYY-MM-DD" | null,
    "category_filter": "Food" | "Transport" | etc | null
}}

For follow_up:
{{
    "intent": "follow_up",
    "reference_type": "previous_data" | "previous_question" | "clarification" | "continuation",
    "context_needed": "brief description of what user is referring to"
}}

For financial_info:
{{
    "intent": "financial_info",
    "search_query": "reformulated search query for web search"
}}

Return only JSON, no explanation.
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]

        try:
            response = self.chat_model.invoke(messages)
            return self.extract_json(response.content)
        except Exception as e:
            print(f"Classification error: {e}")
            return {"intent": "out_of_context", "response": "Sorry, I had trouble understanding that."}

    def search_financial_info(self, query: str) -> str:
        """Use Google Search grounding for financial information"""
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(
                f"Answer this financial question with current information: {query}. Provide a comprehensive but concise answer."
            )
            
            if response and response.text:
                return response.text
            else:
                return "I couldn't find information about that right now. Please try again later."
                
        except Exception as e:
            print(f"Search error: {e}")
            return "I'm having trouble accessing current information right now. Please try again later."

    def handle_follow_up(self, user_id: int, follow_up_info: dict, original_query: str) -> str:
        """Handle follow-up questions based on conversation history"""
        
        chat_history = self.get_chat_history(user_id)
        
        if not chat_history:
            return "Hey buddy! 🤔 I don't see any previous conversation to refer to. Could you be more specific about what you're asking?"
        
        # Get recent conversation for context
        recent_context = ""
        for msg in chat_history[-6:]:  # Last 6 messages
            if isinstance(msg, HumanMessage):
                recent_context += f"User: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                recent_context += f"Assistant: {msg.content}\n"
        
        # Generate contextual response
        prompt = f"""
You are a friendly financial assistant. The user is asking a follow-up question.

USER'S FOLLOW-UP QUESTION: "{original_query}"

RECENT CONVERSATION:
{recent_context}

Based on the conversation history, provide a helpful response that:
1. Addresses the user as "buddy"
2. References the previous conversation appropriately
3. Provides the information they're looking for
4. Is conversational and engaging
5. Uses emojis and friendly tone

If they're asking for more details about previous data, provide it.
If they're asking for clarification, explain clearly.
If they're asking for related information, provide it.
"""

        try:
            response = self.chat_model.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            return "Hey buddy! 😅 I can see you're referring to our previous chat, but I'm having trouble processing that right now. Could you be more specific about what you need?"

    def generate_transaction_history_response(self, user_id: int, query_info: dict, original_query: str) -> str:
        """Generate quirky buddy-style response for transaction history"""
        
        start_date = query_info.get("start_date")
        end_date = query_info.get("end_date")
        
        # If no dates specified, fetch ALL transactions (use a very old start date)
        if not start_date or not end_date:
            end_date = self.today.strftime("%Y-%m-%d")
            start_date = "2020-01-01"  # Very old date to get all transactions
        
        # Get financial data
        data = get_user_financial_data(user_id, start_date, end_date)
        
        if not data or not data['transactions']:
            return "Hey buddy! 👋 Looks like your wallet has been pretty quiet - no transactions found in that period. Time to get out there and spend some money! 💸 (Just kidding, saving is good too! 😄)"
        
        # Create clean table format
        if data['transactions']:
            # Format transactions into a clean table
            table_rows = []
            for transaction in data['transactions']:
                date_str = transaction['transaction_date'].strftime('%d/%m/%Y') if hasattr(transaction['transaction_date'], 'strftime') else str(transaction['transaction_date'])
                amount_str = f"₹{transaction['amount']}"
                if transaction['transaction_type'] == 'Credit':
                    amount_str = f"+{amount_str}"
                else:
                    amount_str = f"-{amount_str}"
                
                table_rows.append(f"{date_str} | {transaction['category_name']} | {transaction['subcategory_name']} | {amount_str}")
            
            transactions_table = "\n".join(table_rows)
        else:
            transactions_table = "No transactions found"
        
        # Generate response using AI with formatted data
        prompt = f"""You are a friendly financial assistant. Address the user as "buddy" and be conversational.

USER QUERY: "{original_query}"

TRANSACTION SUMMARY:
- Total transactions: {len(data['transactions'])}
- Total expenses: ₹{data['total_expenses']}
- Total income: ₹{data['total_income']}
- Net amount: ₹{data['total_income'] - data['total_expenses']}

TRANSACTION TABLE (Date | Category | Description | Amount):
{transactions_table}

Generate a response that:
1. Starts with "Hey buddy!" 
2. Summarizes their financial activity
3. Shows the transaction table exactly as formatted above
4. Adds encouraging insights
5. Uses emojis and friendly tone
6. Keep it organized and easy to read

Format the table with proper spacing and alignment.
"""

        try:
            response = self.chat_model.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            return f"Hey buddy! 😅 Here's your financial summary:\n\n📊 Transactions: {len(data['transactions'])}\n💸 Expenses: ₹{data['total_expenses']}\n💰 Income: ₹{data['total_income']}\n\n📋 Recent Transactions:\nDate | Category | Description | Amount\n{transactions_table}"

    def process_message(self, user_message: str, whatsapp_number: str = None):
        """Process user message and return appropriate response"""
        
        # Get or create user
        if whatsapp_number:
            user_id = add_user(whatsapp_number)
        else:
            user_id = add_user("console_user")
        
        if user_id is None:
            return "Sorry buddy, I'm having trouble setting up your account right now."

        # Add user message to chat history
        self.add_to_chat_history(user_id, HumanMessage(content=user_message))

        # Classify the intent
        classification = self.classify_user_intent(user_message, user_id)
        
        if not classification:
            return "Sorry buddy, I didn't quite get that. Can you try rephrasing?"

        intent = classification.get("intent")
        
        if intent == "greeting":
            response = classification.get("response", "Hey buddy! How can I help you with your finances today? 💰")
            
        elif intent == "out_of_context":
            response = "Hey buddy! I'm your financial assistant. I can help with tracking expenses, income, and answering financial questions. Try asking about your spending or financial topics! 📊"
            
        elif intent == "transaction":
            # Store transactions
            transactions = classification.get("transactions", [])
            stored_count = 0
            
            for transaction in transactions:
                try:
                    add_interaction(
                        user_id=user_id,
                        message_text=user_message,
                        transaction_type=TransactionType.Debit if transaction["transaction_type"] == "Debit" else TransactionType.Credit,
                        amount=transaction["amount"],
                        category_name=transaction["category_name"],
                        subcategory_name=transaction["subcategory_name"],
                        transaction_date=datetime.strptime(transaction["transaction_date"], "%Y-%m-%d").date()
                    )
                    stored_count += 1
                except Exception as e:
                    print(f"Error storing transaction: {e}")
            
            if stored_count > 0:
                # Generate personalized response using LLM
                total_amount = sum(transaction['amount'] for transaction in transactions)
                transaction_types = [transaction['subcategory_name'] for transaction in transactions]
                is_income = any(transaction['transaction_type'] == 'Credit' for transaction in transactions)
                
                # Determine transaction context from user message
                user_context = user_message.lower()
                
                prompt = f"""You are a friendly financial assistant. The user just recorded a transaction.

USER'S ORIGINAL MESSAGE: "{user_message}"
TRANSACTION AMOUNT: ₹{total_amount}
TRANSACTION TYPE: {"Income" if is_income else "Expense"}

Generate a natural, engaging response that:
1. Acknowledges what they specifically mentioned (shirt, salary, groceries, etc.)
2. Uses "buddy" to address the user
3. Is enthusiastic and supportive
4. Includes relevant emojis based on the transaction type
5. Keep it brief (1-2 sentences)
6. Celebrates income or acknowledges expenses positively

Examples:
- For "I bought a shirt for 300": "Nice shopping, buddy! 👕 That ₹300 shirt purchase is tracked - hope you look awesome in it! ✨"
- For "I received salary 50000": "Woohoo, payday buddy! � Your ₹50000 salary is logged - time to celebrate! 🎉"
- For "I spent 500 on groceries": "Great job tracking that, buddy! � Your ₹500 grocery expense is saved - keeping that budget on point! 📊"
- For "I earned 2000 from freelancing": "Awesome work, buddy! 💪 That ₹2000 freelancing income is recorded - hustle paying off! 🚀"

Generate a similar enthusiastic response based on their message.
"""

                try:
                    llm_response = self.chat_model.invoke([HumanMessage(content=prompt)])
                    response = llm_response.content
                except Exception as e:
                    print(f"Error generating LLM response: {e}")
                    response = f"Got it, buddy! 📝 I've recorded {stored_count} transaction(s) for you. Your financial tracking game is strong! 💪"
            else:
                response = "Hey buddy, I understood what you wanted to record but had trouble saving it. Can you try again? 🤔"
                
        elif intent == "follow_up":
            response = self.handle_follow_up(user_id, classification, user_message)
            
        elif intent == "transaction_history":
            response = self.generate_transaction_history_response(user_id, classification, user_message)
            
        elif intent == "financial_info":
            search_query = classification.get("search_query", user_message)
            search_result = self.search_financial_info(search_query)
            response = f"Hey buddy! 🔍 Here's what I found:\n\n{search_result}"
            
        else:
            response = "Hey buddy! I'm not sure how to help with that. Try asking about your expenses, income, or financial questions! 💡"

        # Add AI response to chat history
        self.add_to_chat_history(user_id, AIMessage(content=response))
        
        return response


def main():
    """Main interactive function"""
    print("🤖 Enhanced Financial Bot Starting...")
    print("💡 I can help with:")
    print("   • Track expenses: 'I spent 500 rupees on groceries'")
    print("   • Show history: 'What did I spend this month?'") 
    print("   • Financial info: 'What is cryptocurrency?'")
    print("   • Current rates: 'Gold price today'")
    print("   • Follow-ups: 'Show me more', 'What about last month?'")
    print("   • Commands: 'clear' (clear history), 'history' (show summary)")
    print()
    
    # Initialize the bot
    bot = EnhancedFinancialBot()
    
    # Get user info
    print("👤 User Setup:")
    whatsapp = input("Enter your WhatsApp number (or press Enter for demo): ").strip()
    
    if not whatsapp:
        whatsapp = "+919876543210"  # Use demo user
        print(f"Using demo user: {whatsapp}")
    
    user_id = add_user(whatsapp)
    print(f"✅ User ID: {user_id}")
    print()
    
    cprint("🚀 Enhanced Financial Bot Ready! Type 'exit' to quit", "green", attrs=["bold"])
    print("="*60)
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                cprint("👋 See you later, buddy! Keep those finances in check! 💰", "cyan")
                break
            
            if user_input.lower() == 'clear':
                response = bot.clear_chat_history(user_id)
                cprint(response, "green")
                continue
                
            if user_input.lower() == 'history':
                response = bot.get_chat_summary(user_id)
                cprint(response, "blue")
                continue
                
            if not user_input:
                continue
                
            # Process the message
            print("🤖 Bot: ", end="")
            response = bot.process_message(user_input, whatsapp)
            cprint(response, "yellow")
            
        except KeyboardInterrupt:
            cprint("\n👋 See you later, buddy! Keep those finances in check! 💰", "cyan")
            break
        except Exception as e:
            cprint(f"❌ Error: {e}", "red")

if __name__ == "__main__":
    main()
