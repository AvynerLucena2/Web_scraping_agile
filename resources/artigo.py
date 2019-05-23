from models.artigo import ArtigoModel
from flask_restful import Resource, reqparse
from bsoup import Bsoup

class Artigo(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('text',
		type=str
	)

	def get(self, name):
		artigo = ArtigoModel.find_by_name(name)
		if artigo:
			return artigo.json()
		return {'message': 'Item not found'}, 404

	def post(self, name):

		if ArtigoModel.find_by_name(name):
			return {"message": "Um artigo com esse nome já existe."}
		else:
			data = Artigo.parser.parse_args()
			artigo = ArtigoModel(name, data['text'])
			artigo.save_to_db()
			return {"message": "O artigo foi adicionado"}
		

class Scraping(Resource):
	def get(self):
		try:
			nome_artigo, texto_artigo, nb_artigos = Bsoup.import_artigos()
		except:
			return {"message": "Nao conseguiu chamar bsoup"}

		for i in range(nb_artigos-1):
			a = ArtigoModel(nome_artigo[i], texto_artigo[i])
			a.save_to_db()

		return {'message': 'Artigos foram importados'}



class ListaArtigos(Resource):
	def get(self):
		return {'artigos': [artigo.json() for artigo in ArtigoModel.query.all()]}

