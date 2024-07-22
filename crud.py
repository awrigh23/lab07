from main import db,Users
from main import app

with app.app_context():
    new_user = Users('Joe,','John')

    db.session.add(new_user)
    db.session.commit()


    all_users = Users.query.all()
    print(all_users)
