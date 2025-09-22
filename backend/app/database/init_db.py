from sqlalchemy.orm import Session
from app.database.config import SessionLocal, create_tables
from app.models.models import Company, User
from app.auth.auth import get_password_hash

def init_database():
    create_tables()
    
    db = SessionLocal()
    try:
        existing_company = db.query(Company).filter(Company.name == "Demo Company").first()
        if not existing_company:
            demo_company = Company(
                name="Demo Company",
                settings='{"evaluation_weights": {"skills": 0.4, "experience": 0.4, "education": 0.2}}'
            )
            db.add(demo_company)
            db.commit()
            db.refresh(demo_company)
            
            admin_user = User(
                email="admin@demo.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                role="admin",
                company_id=demo_company.id
            )
            
            recruiter_user = User(
                email="recruiter@demo.com",
                hashed_password=get_password_hash("recruiter123"),
                full_name="Recruiter User",
                role="recruiter",
                company_id=demo_company.id
            )
            
            db.add(admin_user)
            db.add(recruiter_user)
            db.commit()
            
            print("Database initialized with demo data")
            print("Admin user: admin@demo.com / admin123")
            print("Recruiter user: recruiter@demo.com / recruiter123")
        else:
            print("Database already initialized")
    
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()