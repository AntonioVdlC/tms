db.createCollection('projects')
db.projects.createIndex({"org_id": 1})