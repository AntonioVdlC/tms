db.createCollection('projects')
db.projects.createIndex({"org_id": 1})
db.projects.createIndex({"keys.key": 1}, {"unique": true})
db.projects.createIndex({"keys.key": 1, "keys.is_deleted": 1})