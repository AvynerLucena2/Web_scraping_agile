from app import app
from db import db
from es import es


db.init_app(app)

@app.before_first_request
def create_tables():
	db.create_all()

	try:
		es.indices.create(index='icms_', body='{"mappings": {"properties" : {"name" : {"type":"text"},"texto" : {"type" : "text", "analyzer" : "brazilian"}}}}')
	except:
		return {"message": "Couldn't creat icms index"}