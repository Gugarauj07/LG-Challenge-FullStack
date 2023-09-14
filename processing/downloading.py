import requests
import zipfile
import os

url = 'http://files.grouplens.org/datasets/movielens/ml-25m.zip'

nome_arquivo_zip = 'ml-25m.zip'

response = requests.get(url)
with open(nome_arquivo_zip, 'wb') as arquivo_zip:
    arquivo_zip.write(response.content)

with zipfile.ZipFile(nome_arquivo_zip, 'r') as zip_ref:
    zip_ref.extractall("./")

os.remove(nome_arquivo_zip)

print('Download e extração concluídos.')