#!/usr/bin/env python3
"""
Script to populate the financial bot database with realistic transaction data
"""

from add_data_in_database import add_user, add_interaction, TransactionType, create_tables
from datetime import datetime, timedelta, date
import random

def populate_sample_data():
    """
    Add realistic financial transaction data to the database
    """
    
    # Create tables first
    create_tables()
    
    # Create sample users
    users = [
        {"whatsapp": "+919876543210", "name": "Rahul Sharma"},
        {"whatsapp": "+919876543211", "name": "Priya Patel"},
        {"whatsapp": "+919876543212", "name": "Amit Kumar"}
    ]
    
    user_ids = []
    for user in users:
        user_id = add_user(user["whatsapp"])
        user_ids.append(user_id)
        print(f"Created user: {user['name']} (ID: {user_id})")
    
    # Sample transaction data - realistic Indian financial transactions
    transactions = [
        # Recent transactions (last 7 days)
        {
            "user_id": user_ids[0],
            "message": "Paid ₹1200 for groceries at Big Bazaar",
            "transaction_type": TransactionType.Debit,
            "amount": 1200.00,
            "category": "Food",
            "subcategory": "Groceries",
            "days_ago": 1
        },
        {
            "user_id": user_ids[0],
            "message": "Salary credited ₹75000",
            "transaction_type": TransactionType.Credit,
            "amount": 75000.00,
            "category": "Income",
            "subcategory": "Salary",
            "days_ago": 2
        },
        {
            "user_id": user_ids[0],
            "message": "Uber ride to office ₹250",
            "transaction_type": TransactionType.Debit,
            "amount": 250.00,
            "category": "Transport",
            "subcategory": "Taxi",
            "days_ago": 1
        },
        {
            "user_id": user_ids[0],
            "message": "Coffee at Starbucks ₹450",
            "transaction_type": TransactionType.Debit,
            "amount": 450.00,
            "category": "Food",
            "subcategory": "Coffee",
            "days_ago": 3
        },
        {
            "user_id": user_ids[0],
            "message": "Netflix subscription ₹649",
            "transaction_type": TransactionType.Debit,
            "amount": 649.00,
            "category": "Entertainment",
            "subcategory": "Streaming",
            "days_ago": 4
        },
        {
            "user_id": user_ids[1],
            "message": "Bought medicines ₹850",
            "transaction_type": TransactionType.Debit,
            "amount": 850.00,
            "category": "Healthcare",
            "subcategory": "Medicine",
            "days_ago": 2
        },
        {
            "user_id": user_ids[1],
            "message": "Freelance payment received ₹25000",
            "transaction_type": TransactionType.Credit,
            "amount": 25000.00,
            "category": "Income",
            "subcategory": "Freelance",
            "days_ago": 5
        },
        {
            "user_id": user_ids[1],
            "message": "Electricity bill ₹3200",
            "transaction_type": TransactionType.Debit,
            "amount": 3200.00,
            "category": "Utilities",
            "subcategory": "Electricity",
            "days_ago": 6
        },
        {
            "user_id": user_ids[2],
            "message": "Dinner at restaurant ₹2800",
            "transaction_type": TransactionType.Debit,
            "amount": 2800.00,
            "category": "Food",
            "subcategory": "Restaurant",
            "days_ago": 1
        },
        {
            "user_id": user_ids[2],
            "message": "Petrol fill up ₹4500",
            "transaction_type": TransactionType.Debit,
            "amount": 4500.00,
            "category": "Transport",
            "subcategory": "Fuel",
            "days_ago": 3
        },
        
        # Older transactions (last month)
        {
            "user_id": user_ids[0],
            "message": "Amazon shopping ₹5600",
            "transaction_type": TransactionType.Debit,
            "amount": 5600.00,
            "category": "Shopping",
            "subcategory": "Online",
            "days_ago": 15
        },
        {
            "user_id": user_ids[0],
            "message": "Gym membership ₹2000",
            "transaction_type": TransactionType.Debit,
            "amount": 2000.00,
            "category": "Health",
            "subcategory": "Fitness",
            "days_ago": 20
        },
        {
            "user_id": user_ids[1],
            "message": "Mobile recharge ₹399",
            "transaction_type": TransactionType.Debit,
            "amount": 399.00,
            "category": "Utilities",
            "subcategory": "Mobile",
            "days_ago": 12
        },
        {
            "user_id": user_ids[1],
            "message": "Book purchase ₹1200",
            "transaction_type": TransactionType.Debit,
            "amount": 1200.00,
            "category": "Education",
            "subcategory": "Books",
            "days_ago": 18
        },
        {
            "user_id": user_ids[2],
            "message": "Insurance premium ₹8500",
            "transaction_type": TransactionType.Debit,
            "amount": 8500.00,
            "category": "Insurance",
            "subcategory": "Health",
            "days_ago": 25
        },
        {
            "user_id": user_ids[2],
            "message": "Bonus received ₹15000",
            "transaction_type": TransactionType.Credit,
            "amount": 15000.00,
            "category": "Income",
            "subcategory": "Bonus",
            "days_ago": 30
        },
        {
            "user_id": user_ids[0],
            "message": "Movie tickets ₹800",
            "transaction_type": TransactionType.Debit,
            "amount": 800.00,
            "category": "Entertainment",
            "subcategory": "Movies",
            "days_ago": 8
        },
        {
            "user_id": user_ids[1],
            "message": "Swiggy food order ₹650",
            "transaction_type": TransactionType.Debit,
            "amount": 650.00,
            "category": "Food",
            "subcategory": "Delivery",
            "days_ago": 4
        },
        {
            "user_id": user_ids[2],
            "message": "ATM withdrawal ₹5000",
            "transaction_type": TransactionType.Debit,
            "amount": 5000.00,
            "category": "Cash",
            "subcategory": "Withdrawal",
            "days_ago": 7
        },
        {
            "user_id": user_ids[0],
            "message": "Metro card recharge ₹500",
            "transaction_type": TransactionType.Debit,
            "amount": 500.00,
            "category": "Transport",
            "subcategory": "Metro",
            "days_ago": 10
        }
    ]
    
    # Add transactions to database
    today = date.today()
    
    for i, transaction in enumerate(transactions, 1):
        transaction_date = today - timedelta(days=transaction["days_ago"])
        
        add_interaction(
            user_id=transaction["user_id"],
            message_text=transaction["message"],
            transaction_type=transaction["transaction_type"],
            amount=transaction["amount"],
            category_name=transaction["category"],
            subcategory_name=transaction["subcategory"],
            transaction_date=transaction_date
        )
        
        print(f"Added transaction {i}/20: {transaction['message']}")
    
    print(f"\n✅ Successfully added {len(transactions)} transactions to the database!")
    print("🎯 Database is now populated with realistic financial data")
    
    # Show summary
    from add_data_in_database import get_user_financial_data
    
    print("\n📊 SUMMARY OF RECENT TRANSACTIONS (Last 7 days):")
    for user_id in user_ids:
        week_start = today - timedelta(days=7)
        data = get_user_financial_data(user_id, week_start, today)
        if data and data['transactions']:
            print(f"\n👤 User {user_id}:")
            print(f"   💸 Total Expenses: ₹{data['total_expenses']}")
            print(f"   💰 Total Income: ₹{data['total_income']}")
            print(f"   📈 Net: ₹{data['total_income'] - data['total_expenses']}")

if __name__ == "__main__":
    print("🚀 Starting database population...")
    populate_sample_data()
