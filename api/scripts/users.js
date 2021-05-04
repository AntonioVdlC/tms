db.createCollection('users')
db.users.createIndex({"email": 1}, {unique: true})
db.users.createIndex({"email": 1, "is_deleted": 1})
db.users.createIndex({"_id": 1, "is_deleted": 1})