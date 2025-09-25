# file: transaction_history.py

import json
from add_data_in_database import get_user_financial_data

class TransactionHistory:
    """
    Handles queries about a user's past financial data by fetching
    the data and generating a personalized, conversational response.
    """
    def __init__(self, model):
        self.chat_model = model

    def generate_report(self, user_id, start_date, end_date, query: str) -> str:
        """
        Generates a report based on a specific user query about their financial history.
        """
        user_data = get_user_financial_data(user_id, start_date, end_date)
        print("------------------ date ------------------")
        print(start_date)
        print(end_date)
        
        if user_data.get('error'):
            return "Sorry, I couldn't find any data for your account."

        prompt = f"""
        You are FinBot, a sassy financial advisor who has access to this user's financial history. 
        You're like that friend who remembers EVERYTHING about someone's spending and isn't afraid to bring it up.

        Your personality: Sarcastic but caring, uses emojis and modern slang, playfully calls out patterns, 
        gets excited about good financial behavior, and keeps everything conversational.

        💰 All transaction amounts are in **INR** – use ₹ and format numbers appropriately.

        USER QUERY: "{query}"

        USER'S FINANCIAL DATA (Last 7 days):
        {json.dumps(user_data, indent=2, default=str)}

        🎯 RESPONSE GUIDELINES:
        1. Answer their specific question using the actual data.
        2. Reference specific transactions or categories if relevant (e.g., "Remember that ₹2,499 Amazon splurge? 👀").
        3. Point out patterns you notice ("A coffee addiction is brewing... literally ☕").
        4. Provide context and comparisons ("You spent more on coffee than your Netflix subscription!").
        5. Use **markdown tables or bullet points** if it helps clarity.
        6. Be specific, structured, and funny – while being genuinely helpful.

        End on a high note with a nudge, joke, or simple advice. Keep it spicy and supportive!
        """

        try:
            response = self.chat_model.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Oops! I'm having trouble accessing your financial history right now. Error: {str(e)}"