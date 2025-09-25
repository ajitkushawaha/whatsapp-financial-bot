#!/usr/bin/env python3
"""
Test Enhanced Financial Bot
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_financial_bot import EnhancedFinancialBot
from add_data_in_database import add_user

def test_enhanced_bot():
    print("🧪 Testing Enhanced Financial Bot...")
    
    # Initialize bot
    bot = EnhancedFinancialBot()
    
    # Test user
    whatsapp = "+919876543210"
    user_id = add_user(whatsapp)
    print(f"Test User ID: {user_id}")
    
    # Test conversations with context
    test_conversations = [
        # Basic interaction
        ("Hello!", "Should greet"),
        
        # Add transaction
        ("I spent 500 rupees on groceries today", "Should record transaction"),
        
        # Ask about spending
        ("What did I spend today?", "Should show today's spending"),
        
        # Follow-up question
        ("What about this week?", "Should understand follow-up context"),
        
        # Financial info with search
        ("What is the current gold rate?", "Should search for gold rate"),
        
        # Another transaction
        ("I earned 2000 rupees from freelancing", "Should record income"),
        
        # Follow-up on income
        ("Show me more details about my income", "Should provide income details"),
        
        # Chat history test
        ("What have we discussed so far?", "Should reference chat history"),
        
        # Out of context
        ("What's the weather like?", "Should redirect to finance topics"),
    ]
    
    print("\n" + "="*60)
    print("🧪 TESTING CONVERSATIONS WITH CONTEXT")
    print("="*60)
    
    for i, (user_msg, expected) in enumerate(test_conversations, 1):
        print(f"\n[Test {i}] User: {user_msg}")
        print(f"Expected: {expected}")
        print("-" * 40)
        
        try:
            response = bot.process_message(user_msg, whatsapp)
            print(f"Bot: {response[:200]}...")
            
            # Show chat history length
            history_len = len(bot.get_chat_history(user_id))
            print(f"📊 Chat history: {history_len} messages")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)
    
    # Test chat history features
    print(f"\n🔍 Testing Chat History Features:")
    print("Chat Summary:", bot.get_chat_summary(user_id))
    
    print("\nClearing history...")
    clear_result = bot.clear_chat_history(user_id)
    print(clear_result)
    
    print("After clear:", bot.get_chat_summary(user_id))

if __name__ == "__main__":
    test_enhanced_bot()
