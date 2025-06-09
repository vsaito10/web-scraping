import pandas as pd
from curl_cffi import requests

"""
URL: https://br.investing.com/economic-calendar/baker-hughes-u.s.-rig-count-1652
"""

class RigCounts:
    def __init__(self):
        # Configuração dos headers para a requisição HTTP
        self.headers = {
            'sec-ch-ua-platform': '"Windows"',
            'Referer': 'https://br.investing.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile': '?0',
        }

    # Buscando os dados da contagem de sondas via requisição HTTP
    def fetch_data(self):
        # Fazendo a requisição GET para a URL da contagem de sondas
        response = requests.get(f'https://sbcharts.investing.com/events_charts/eu/1652.json', headers=self.headers, impersonate='chrome')
        return response.json()

    # Processando os dados da contagem de sondas
    def process_data(self, data):
        # Criando um DataFrame a partir dos dados JSON
        df = pd.DataFrame(data['attr'])
        # Convertendo a coluna 'timestamp' de milissegundos para datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        # Formatando a data para o formato 'YYYY-MM-DD'
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d')
        # Convertendo a coluna 'timestamp' para o tipo datetime 
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d')
        # Selecionando as colunas principais
        df = df[['timestamp', 'actual']]
        # Definindo a coluna 'timestamp' como índice do DataFrame
        df = df.set_index('timestamp')
        return df

    # Salvando o DataFrame em um arquivo CSV
    def save_to_csv(self, df, file_name):
        df.to_csv(file_name, sep=';')

    # Executando o fluxo completo
    def run(self, base_path):
        # Definindo o nome do arquivo CSV 
        file_name = f'{base_path}/rig_counts.csv'
        # Buscando os dados da contagem de sondas
        data = self.fetch_data()
        # Processando os dados e transformando em DataFrame
        df = self.process_data(data)
        # Salvando o DataFrame em um arquivo CSV
        self.save_to_csv(df, file_name)
        print(f'Arquivo salvo como: {file_name}')


if __name__ == "__main__":
    # Caminho onde o arquivo será salvo
    base_path = 'C:/Users/vitor/projetos_python/python_b3/web-scraping/dados-alternativos/rig-counts'
    
    rig_counts = RigCounts()
    rig_counts.run(base_path)