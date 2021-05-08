db.createCollection('invites')
db.invites.createIndex({"email": 1, "is_deleted": 1})
db.invites.createIndex({"email": 1, "org_id": 1, "is_deleted": 1}, {"unique": true})
db.invites.createIndex({"org_id": 1})