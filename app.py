from flask import Flask 
from flask_restful import Api

from resources.artigoES import ArtigoNome, ArtigoTexto, ListaArtigos, Scraping


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite://data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.secret_key = 'livia'

api = Api(app)

@app.before_first_request
def create_tables():
	db.create_all()
	try:
		es.indices.create(index='icms_', body='{"mappings": {"properties" : {"name" : {"type":"text"},"text" : {"type" : "text", "analyzer" : "brazilian"}}}}')
	except:
		return {"message": "Couldn't creat icms index"}


api.add_resource(ArtigoNome, '/artigo/<string:name>')
api.add_resource(ArtigoTexto, '/artigotexto/<string:text>')
api.add_resource(ListaArtigos, '/artigos')
api.add_resource(Scraping, '/scraping')

if __name__ == '__main__':
	from db import db
	from es import es
	db.init_app(app)
	app.run(port=600, debug=True)