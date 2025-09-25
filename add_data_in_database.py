from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, Date, Enum, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import update
import enum
from datetime import datetime, timedelta
from termcolor import cprint

# Define SQLite connection string
DATABASE_URL = "sqlite:///financial_bot.db"

# Create engine and base class
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

print("Database connection established successfully!")

# Enum for transaction_type
class TransactionType(enum.Enum):
    Debit = 'Debit'
    Credit = 'Credit'

# Users table
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    whatsapp_number = Column(String(20), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# User_Interactions table
class UserInteraction(Base):
    __tablename__ = 'user_interactions'
    interaction_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    message_text = Column(Text, nullable=False)
    transaction_type = Column(Enum(TransactionType))
    amount = Column(DECIMAL(12, 2))
    category_name = Column(String(100))
    subcategory_name = Column(String(100))
    transaction_date = Column(Date)
    processed_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User")

# Create tables (optional)
def create_tables():
    Base.metadata.create_all(engine)

# Add a new user
def add_user(whatsapp_number):
    session = SessionLocal()
    try:
        # Check if user already exists
        existing_user = session.query(User).filter_by(whatsapp_number=whatsapp_number).first()
        if existing_user:
            print(f"User already exists: ID = {existing_user.user_id}")
            return existing_user.user_id

        # If not, create new user
        user = User(whatsapp_number=whatsapp_number)
        session.add(user)
        session.commit()
        print(f"New user created: ID = {user.user_id}")
        return user.user_id
    except Exception as e:
        session.rollback()
        print(f"Error adding user: {e}")
    finally:
        session.close()


# Add a user interaction
def add_interaction(user_id, message_text, transaction_type=None, amount=None,
                    category_name=None, subcategory_name=None, transaction_date=None):
    session = SessionLocal()
    try:
        interaction = UserInteraction(
            user_id=user_id,
            message_text=message_text,
            transaction_type=transaction_type,
            amount=amount,
            category_name=category_name,
            subcategory_name=subcategory_name,
            transaction_date=transaction_date
        )
        session.add(interaction)

        # Update user's updated_at timestamp manually
        session.query(User).filter(User.user_id == user_id).update(
            {"updated_at": func.now()}
        )
        
        session.commit()
        print(f"Interaction added successfully for user_id {user_id}")
    except Exception as e:
        session.rollback()
        print(f"Error adding interaction: {e}")
    finally:
        session.close()

def get_user_financial_data(user_id, start_date, end_date):
    session = SessionLocal()
    try:
        # Convert string inputs to date objects if necessary
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Query interactions between the dates for the given user
        interactions = (
            session.query(UserInteraction)
            .filter(
                UserInteraction.user_id == user_id,
                UserInteraction.transaction_date.between(start_date, end_date)
            )
            .order_by(UserInteraction.transaction_date.desc())
            .all()
        )

        # Convert each row into a dictionary
        transactions = [
            {
                'interaction_id': t.interaction_id,
                'user_id': t.user_id,
                'message_text': t.message_text,
                'transaction_type': t.transaction_type.value if t.transaction_type else None,
                'amount': float(t.amount) if t.amount is not None else 0.0,
                'category_name': t.category_name,
                'subcategory_name': t.subcategory_name,
                'transaction_date': t.transaction_date.strftime('%Y-%m-%d') if t.transaction_date else None,
                'processed_at': t.processed_at.strftime('%Y-%m-%d %H:%M:%S') if t.processed_at else None
            }
            for t in interactions
        ]

        # Compute totals
        total_expenses = sum(t['amount'] for t in transactions if t['transaction_type'] == 'Debit')
        total_income = sum(t['amount'] for t in transactions if t['transaction_type'] == 'Credit')

        # Category-wise expense breakdown
        category_totals = {}
        for t in transactions:
            if t['transaction_type'] == 'Debit':
                category = t['category_name'] or "Uncategorized"
                category_totals[category] = category_totals.get(category, 0.0) + t['amount']

        # Days between
        days = (end_date - start_date).days + 1

        return {
            'transactions': transactions,
            'category_breakdown': category_totals,
            'period_days': days,
            'total_expenses': round(total_expenses, 2),
            'total_income': round(total_income, 2)
        }

    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return None
    finally:
        session.close()




# Example usage
if __name__ == "__main__":
    create_tables()  # Create tables if they don't exist
    user_id = add_user("1234567890")
    print(user_id)
    interactions = get_user_financial_data(1, "2025-06-15", "2025-06-21")
    cprint(interactions, "green")
