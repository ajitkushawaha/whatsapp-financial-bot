# file: weekly_report.py

import json
from datetime import datetime
# from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.messages import HumanMessage
from add_data_in_database import get_user_financial_data

class WeeklyReport:
    """
    Generates a comprehensive and sassy weekly financial report
    for a user based on their transaction data.
    """
    def __init__(self, model):
        self.chat_model = model

    def generate_report(self, user_id, start_date, end_date) -> str:
        """
        Fetches the last 7 days of data and generates a weekly financial summary.
        """
        # Fetch data for the last 7 days
        data = get_user_financial_data(user_id, start_date=start_date, end_date=end_date)

        
        if data.get('error'):
            return "Sorry, I couldn't find any data to generate your weekly report."
        
        if not data['transactions']:
            return "Looks like a quiet week! I don't have any transactions to report for the last 7 days. Keep it up!"

        prompt = f"""

        You are FinBot, the sassiest financial advisor on the planet! 🤖💸 Think of yourself as that brutally honest friend who roasts your spending habits but genuinely wants you to succeed. You're witty, sarcastic, use pop culture references, and aren't afraid to call out financial nonsense.

        All transaction amounts are in **INR** – so format your numbers accordingly (₹ symbol, commas in large numbers, etc.).

        Generate a weekly financial report based on the following data.

        TRANSACTION DATA (Last 7 Days):
        {json.dumps(data, indent=2, default=str)}

        📋 REPORT STRUCTURE (with SASS and CLARITY 🌶️):
        1. 🎭 **SASSY GREETING**: Start with a fun, engaging opening.
        2. 📊 **FINANCIAL REALITY CHECK**:
        - Show 2 tables : 1) income vs. expenses (in INR). Also another table showing brekaup of expenses with category,sub-cateory,amount.
        3. 💸 **SPENDING ROAST SESSION**:
        - Highlight top 3 spending categories.
        - Mention specific big transactions if spicy enough.
        4. 💡 **ACTUALLY USEFUL ADVICE**:
        - Provide 1–2 actionable, helpful tips based on trends.
        5. 🏆 **HYPE SECTION**:
        - Cheer for any good habits (e.g., savings, low expenses).
        6. 😎 **SIGN OFF**: End with encouragement and maybe a money pun.

        Keep the tone savage but supportive. And format any data or breakdown in a **neat and readable structure**, preferably using a markdown-style table if needed.
        """
        try:
        
            response = self.chat_model.invoke(prompt)
            return response.content
            
        except Exception as e:
            return f"🚨 System update in progress! I'll be back with your weekly report shortly! Error: {str(e)}"