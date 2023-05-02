from app import app
from models import db, User

db.drop_all()
db.create_all()

u1 = User(
    username="bob",
    password="123",
    email="bob@example.com",
    first_name="bob",
    last_name="example"
)

u2 = User(
    username="alice",
    password="456",
    email="alice@example.com",
    first_name="alice",
    last_name="example"
)

db.session.add_all([u1, u2])
db.session.commit()