import requests
from io import StringIO
import requests
import pandas as pd


# Global Supply Chain Pressure Index (GSCPI)
# A URL do 'gscpi_interactive_data.csv' foi encontrada na aba 'GSCPI' (https://www.newyorkfed.org/research/policy/gscpi#/interactive) 
# 'Network' -> 'Fetch/XHR' -> 'gscpi_interactive_data.csv' -> 'Copy as cURL (cdm)' -> Insomnia
url = 'https://www.newyorkfed.org/medialibrary/research/interactives/data/gscpi/gscpi_interactive_data.csv'

payload = ""
headers = {
    'cookie': 'shell%23lang=en; sxa_site=nyfrbpublic',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

response = requests.request('GET', url, data=payload, headers=headers)

gscpi_table = response.text

# Criando um DataFrame a partir do texto
df = pd.read_csv(
    StringIO(gscpi_table),
    header=0
)

# Transformando o df em um arquivo csv
df.to_csv('C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//gscpi//gscpi.csv')