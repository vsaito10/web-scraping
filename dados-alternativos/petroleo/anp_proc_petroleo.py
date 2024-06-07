import os
import requests
import warnings


# Ignorar avisos de SSL
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

class ProcessamentoPetroleoANP:
    def __init__(self):

        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-alternativos//petroleo'
        
        url = 'https://dados.gov.br/api/publico/conjuntos-dados/processamento-de-petroleo-e-producao-de-derivados'

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "pt-BR,pt;q=0.7",
            "priority": "u=1, i",
            "referer": "https://dados.gov.br/dados/conjuntos-dados/processamento-de-petroleo-e-producao-de-derivados",
            "^sec-ch-ua": "^\^Brave^^;v=^\^125^^, ^\^Chromium^^;v=^\^125^^, ^\^Not.A/Brand^^;v=^\^24^^^",
            "sec-ch-ua-mobile": "?0",
            "^sec-ch-ua-platform": "^\^Windows^^^",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }

        response = requests.request('GET', url, headers=headers, verify=False)

        # Transformando em json
        self.data = response.json()

    def download_arquivo(self):
        # Iterando sobre o arquivo json para pegar os links de download das planilhas
        lst_link_planilhas = []
        for resource in self.data['resources']:
            if resource['format'] == 'CSV':
                links = resource['url']
                lst_link_planilhas.append(links)

        # A 'lst_link_planilhas' contém os links:
        # ['https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/pppd/processamento-petroleo-m3-1990-2024.csv',
        #  'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/pppd/producao-derivados-petroleo-por-refinaria-m3-1990-2024.csv',
        #  'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/pppd/producao-gas-combustivel-1000m3-2000-2024.csv',
        #  'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/pppd/producao-derivados-centrais-petroquimicas-m3-2001-2024.csv',
        #  'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/pppd/producao-derivados-xisto-m3-2001-2024.csv',
        #  'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/pppd/producao-derivados-outros-produtores-m3-2001-2024.csv']

        # A planilha "Processamento de Petróleo (metros cúbicos) 1990-2024" é a primeira da lista
        link_proc_petroleo = lst_link_planilhas[0]

        # Fazendo o download da planilha
        response = requests.get(link_proc_petroleo, verify=False)
        if response.status_code == 200:
            nome_arquivo = os.path.join(self.download_directory, os.path.basename(link_proc_petroleo))
            with open(nome_arquivo, 'wb') as f:
                f.write(response.content)


def main():
    processamento_petroleo = ProcessamentoPetroleoANP()
    processamento_petroleo.download_arquivo()


if __name__ == "__main__":
    main()