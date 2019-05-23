from db import db

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
	def find_by_name(cls, name):
		try:
			return cls.query.filter_by(name=name).first()
		except:
			return {"message": "couldnt query"}, 500	
	def save_to_db(self):
		try:
			db.session.add(self)
			db.session.commit()
		except:
			return {"message": "couldnt reach database"},500


