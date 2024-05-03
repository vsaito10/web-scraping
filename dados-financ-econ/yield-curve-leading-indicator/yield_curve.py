from datetime import datetime
from io import StringIO
import requests
import pandas as pd

# The Yield Curve as a Leading Indicator - FED NY
# A URL do 'yield.csv' foi encontrada na aba 'Charts' (https://www.newyorkfed.org/research/capital_markets/ycfaq#/interactive) 
# 'Network' -> 'Fetch/XHR' -> 'yield.csv' -> 'Copy as cURL (cdm)' -> Insomnia
url = 'https://www.newyorkfed.org/medialibrary/media/research/capital_markets/yield/assets/data/yield.csv'

payload = ""

headers = {
    'cookie': 'shell%23lang=en; sxa_site=nyfrbpublic',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

response = requests.request('GET', url, data=payload, headers=headers)

yield_text = response.text

# Criando um DataFrame a partir do texto
df = pd.read_csv(
    StringIO(yield_text),
    header=0
)

# Retirando os NaN
df = df.dropna()

# A coluna 'Date' contém dois tipos de formatos de datas -> '31-Jan-60' e '	9/30/2023'
# Separando os dfs
filt = df['Date'].str.contains('-')
filt2 = df['Date'].str.contains('/')

df2 = df.loc[filt]
df3 = df.loc[filt2]

# Fazendo uma copia do df
df2 = df2.copy()
df3 = df3.copy()

def converter_data(data_inicial):
    """
    Função para converter a data de "28-Feb-17" para "02/28/17".
    """
    data_objeto = datetime.strptime(data_inicial, '%d-%b-%y')
    data_formatada = data_objeto.strftime('%m/%d/%y')
    
    return data_formatada

def converter_data2(data_inicial):
    """
    Função para converter a data de "9/30/2023" para "9/30/23".
    """
    data_objeto = datetime.strptime(data_inicial, '%m/%d/%Y')
    data_formatada = data_objeto.strftime('%m/%d/%y')
    
    return data_formatada

# Aplicando a função na coluna 'Date'
df2['Date'] = df2.loc[:, 'Date'].apply(converter_data)
df3['Date'] = df3.loc[:, 'Date'].apply(converter_data2)

# Concatenando os dois dfs
df_yield_curve = pd.concat([df2, df3])

# Transformando em float
df_yield_curve['Rec_prob'] = df_yield_curve['Rec_prob'].str.replace('%', '')
df_yield_curve['Rec_prob'] = df_yield_curve['Rec_prob'].astype(float)

# Selecionando a última data lançada
ultima_data = df_yield_curve['Date'].iloc[-1]
ultima_data = ultima_data.replace('/', '')

# Transformando em um arquivo csv
df_yield_curve.to_csv(f'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//yield-curve-leading-indicator//{ultima_data}_yield_curve.csv')