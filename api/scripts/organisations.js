db.createCollection('organisations')
db.projects.createIndex({"members.id": 1}, {"unique": true})