db.createCollection('invites')
db.invites.createIndex({"email": 1, "is_deleted": 1})