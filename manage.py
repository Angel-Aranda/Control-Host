from flask_security import hash_password
from app import app, db, security


with app.app_context():
    
    db.drop_all()
    db.create_all()
    admin_role = security.datastore.find_or_create_role(name="admin", description="Administrator")
    user_role = security.datastore.find_or_create_role(name="user", description="Regular user")
    db.session.commit()

    if not security.datastore.find_user(email="admin@demo.com"):
        security.datastore.create_user(
            email="admin@demo.com",
            password=hash_password("password"),
            roles = ["admin"]
        )

    if not security.datastore.find_user(email="user@demo.com"):
        security.datastore.create_user(
            email="user@demo.com",
            password=hash_password("password"),
            roles = ["user"]
        )


    db.session.commit()