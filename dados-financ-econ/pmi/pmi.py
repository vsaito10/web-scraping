import pandas as pd
from curl_cffi import requests


"""
URLS:
PMI Serviços - https://br.investing.com/economic-calendar/services-pmi-1062
PMI Industrial - https://br.investing.com/economic-calendar/manufacturing-pmi-829
PMI ISM Não-Manufatura - https://br.investing.com/economic-calendar/ism-non-manufacturing-pmi-176
PMI ISM Industrial - https://br.investing.com/economic-calendar/ism-manufacturing-pmi-173
PMI Industrial China - https://br.investing.com/economic-calendar/chinese-manufacturing-pmi-594
PMI Servicos - https://br.investing.com/economic-calendar/chinese-non-manufacturing-pmi-831
"""

class PMI:
    def __init__(self, num_tipo_pmi):
        # Número da URL do site Investing que corresponde com o tipo do PMI
        self.num_tipo_pmi = num_tipo_pmi
        # Obtendo o tipo de PMI correspondente ao número da URL do site Investing
        self.tipo_pmi = self.get_tipo_pmi()
        # Configuração dos headers para a requisição HTTP
        self.headers = {
            'sec-ch-ua-platform': '"Windows"',
            'Referer': 'https://br.investing.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile': '?0',
        }

    # Mapeando o número da URL do site Investing que corresponde com o tipo do PMI
    def get_tipo_pmi(self):
        tipos_pmi = {
            '829': 'pmi_industrial',
            '1062': 'pmi_servicos',
            '173': 'pmi_industrial_ism',
            '176': 'pmi_ism_nao_manufatura',
            '594': 'china_pmi_industrial',
            '831': 'china_pmi_nao_manufatura'
        }

        return tipos_pmi.get(self.num_tipo_pmi, 'tipo_pmi_desconhecido')

    # Buscando os dados do PMI via requisição HTTP
    def fetch_data(self):
        # Fazendo a requisição GET para a URL do PMI
        response = requests.get(f'https://sbcharts.investing.com/events_charts/eu/{self.num_tipo_pmi}.json', headers=self.headers, impersonate='chrome')
        return response.json()

    # Processando os dados do PMI
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
        # Definindo o nome do arquivo CSV usando o tipo do PMI
        file_name = f'{base_path}/{self.tipo_pmi}.csv'
        # Buscando os dados do PMI
        data = self.fetch_data()
        # Processando os dados e transformando em DataFrame
        df = self.process_data(data)
        # Salvando o DataFrame em um arquivo CSV
        self.save_to_csv(df, file_name)
        print(f'Arquivo salvo como: {file_name}')


if __name__ == "__main__":
    # Número da URL do site Investing do PMI
    num_tipo_pmi = '831'
    # Caminho onde o arquivo será salvo
    base_path = 'C:/Users/vitor/projetos_python/python_b3/web-scraping/dados-financ-econ/pmi/atualizado'
    
    pmi = PMI(num_tipo_pmi)
    pmi.run(base_path)