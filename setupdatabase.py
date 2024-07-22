from main import app, db

with app.app_context():
    # Drop the existing table if it exists
    db.drop_all()
    # Create the tables again
    db.create_all()