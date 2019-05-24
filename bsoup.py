import requests
import re
import numpy as np
from bs4 import BeautifulSoup
import time
import json
from models.artigo import ArtigoModel

class Bsoup():

	def import_artigos():
		try:
			r_livro1 = requests.get('http://www.fazenda.rj.gov.br/sefaz/content/conn/UCMServer/path/Contribution%20Folders/site_fazenda/legislacao/tributaria/decretos/2000/ricms/livro%20I/livro_I.html?lve') 
			livro1 = BeautifulSoup(r_livro1.text, 'html.parser')
			time.sleep(2)
		except:
			return {"message": "Could not get a response from URL"},500


		content = livro1.find("div", attrs={'class': 'bea-portal-window-content'})

		# finds all paragraphs
		paragraph = livro1.find_all('p')

		# creates a list with every paragraph
		arts2 = []
		for p in paragraph:
			arts2.append(p.text)

		# from list to a single string
		art = ' '.join(arts2)

		# splits article by article
		artigo = re.split('Art[.]', art)

		###### Formats name of file
		titulo = artigo[0]
		# Removes edges withespaces
		titulo = titulo.strip()														
		titulo = titulo.replace(' ', '_')
		del artigo[0]

		nb_artigos = len(artigo)

		name = []
		for i in range(nb_artigos-1):
			name.append(titulo + str(i) + '.json')


		##### Structures the format of files
		artigo = [item.replace('º','') for item in artigo]
		# Removes edges withespaces
		artigo = [item.strip() for item in artigo]
		# Splits the first space of the name 
		artigo = [item.split(' ',1) for item in artigo]

		# Creates lists 
		data1 = [line[0]  for line in artigo]
		data2 = [line[1]  for line in artigo]



		# # Saves the articles in the database and in the json file
		for i in range(nb_artigos-1):
			with open('ICMS\%s' %name[i], 'w', encoding='utf8') as write_file:
				data = {"artigo" : data1[i], "texto" : data2[i]}
				json.dump(data, write_file, indent=1, ensure_ascii=False)

		return data1, data2, nb_artigos

		# 	if ArtigoModel.find_by_name(data1[i]):
		# 		return {"message": "Um artigo com esse nome já existe."}
		# 	else:
		# 		a = ArtigoModel(data1[i], data2[i])
		# 		a.save_to_db()


	