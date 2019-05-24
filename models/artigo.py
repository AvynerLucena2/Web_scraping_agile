from db import db
from es import es


class ArtigoModel(db.Model):
	__tablename__ = 'artigos'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	text = db.Column(db.String(500))



	def __init__(self, name, text):
		self.name = name
		self.text = text

	def json(self):
		return {'name': self.name, 'text': self.text}

	@classmethod
	def find_by_name_db(cls, name):
		try:
			return cls.query.filter_by(name=name).first()
		except:
			return {"message": "couldnt query"}, 500

	@classmethod
	def find_by_name_es(cls, name):
		try:
			search = es.search(index="icms_", body={"query": {"match": {'name': name}}})["hits"]["hits"]
			artigos = []
			for artigo in search:
				artigos.append(artigo["_source"])
			return artigos

		except:
			return {"message": "couldnt query"}, 500

	@classmethod
	def find_by_text_es(cls, text):
		try:
			search = es.search(index="icms_", body={"query": {"match": {'text': text}}})["hits"]["hits"]
			artigos = []
			for artigo in search:
				artigos.append(artigo["_source"])
			return artigos

		except:
			return {"message": "couldn't run the query."}, 500

	@classmethod
	def list_all_es(cls):
		try:
			search = es.search(index="icms_", body={"query": {"match_all": {}}, "size": 1000})["hits"]["hits"]
			artigos = []
			for artigo in search:
				artigos.append(artigo["_source"])
			return artigos

		except:
			return {"message": "couldnt query"}, 500


	def save_to_db(self):
		try:
			db.session.add(self)
			db.session.commit()
		except:
			return {"message": "couldn't reach database."},500
		try:
			es.index(index='icms_', doc_type='_doc', id=self.id, body=self.json())
		except:
			return {"message": "couldn't reach Elasticsearch."},500

	def delete(self):
		db.session.delete(self)
		db.session.commit()

		try:
			es.delete(index='icms_', doc_type='_doc', id=self.id)
		except:
			return {"message": "couldn't delete from elastic."},500


