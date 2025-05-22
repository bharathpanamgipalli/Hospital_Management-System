from app import app, db
from models import User

with app.app_context():
    # Create the database tables
    db.create_all()

    # Create a default user
    admin = User(username="admin", password="admin123", role="admin")
    db.session.add(admin)
    db.session.commit()
    print("✅ Default user 'admin' created with password 'admin123'")
