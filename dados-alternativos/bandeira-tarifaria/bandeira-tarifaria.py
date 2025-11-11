import requests
import pandas as pd


# URL ANEEL
# Estou puxando os 200 primeiros resultados - essa base de dados começa em '2015-01-01'
url = 'https://dadosabertos.aneel.gov.br/api/3/action/datastore_search?resource_id=0591b8f6-fe54-437b-b72b-1aa2efd46e42&limit=200'

# Headers
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'close'
}

# Tempo do timeout 
timeout_segundos = 60 

try:
    response = requests.get(url, headers=headers, timeout=timeout_segundos) 
    response.raise_for_status() 
    data = response.json()
    
    # Transformando em um df
    df_bandeira_tarifaria = pd.DataFrame(data['result']['records'])

    # Selecionando as principais colunas
    df_bandeira_tarifaria = df_bandeira_tarifaria[['DatCompetencia', 'NomBandeiraAcionada', 'VlrAdicionalBandeira']]

    # Transformando o dtype das colunas
    df_bandeira_tarifaria['DatCompetencia'] = pd.to_datetime(df_bandeira_tarifaria['DatCompetencia'], format='%Y-%m-%d')
    df_bandeira_tarifaria['VlrAdicionalBandeira'] = df_bandeira_tarifaria['VlrAdicionalBandeira'].str.replace(',', '.').astype(float)

    # Transformando a coluna 'DatCompetencia' como index do df
    df_bandeira_tarifaria = df_bandeira_tarifaria.set_index('DatCompetencia')

    # Transformando em um arquivo csv
    df_bandeira_tarifaria.to_csv('C://Users//vitor//projetos_python//python_b3//web-scraping//dados-alternativos//bandeira-tarifaria//bandeira_tarifaria.csv', sep=';')

except requests.exceptions.Timeout:
    print(f'Erro: A requisição expirou (Timeout após {timeout_segundos} segundos).')
except requests.exceptions.RequestException as e:
    print(f'Erro durante a requisição: {e}')

    