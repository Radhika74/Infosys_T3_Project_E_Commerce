from . import db

db.drop_all()
print("deleted")
db.create_all()
print("created new table")