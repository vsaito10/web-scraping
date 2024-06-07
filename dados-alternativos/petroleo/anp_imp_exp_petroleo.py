import os
import requests
import warnings


# Ignorar avisos de SSL
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

class ImpExpPetroleoANP:
    def __init__(self):

        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-alternativos//petroleo'
        
        url = 'https://dados.gov.br/api/publico/conjuntos-dados/importacoes-e-exportacoes'

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "pt-BR,pt;q=0.8",
            "priority": "u=1, i",
            "referer": "https://dados.gov.br/dados/conjuntos-dados/importacoes-e-exportacoes",
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
        # ['https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/ie/petroleo/importacoes-exportacoes-petroleo-2000-2024.csv', 
        #  'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/ie/gn/importacao-gas-natural-2000-2024.csv', 
        #  'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/ie/derivados/importacoes-exportacoes-derivados-2000-2024.csv', 
        #  'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/ie/etanol/importacoes-exportacoes-etanol-2012-2024.csv']

        # A planilha "Importações e exportações de petróleo (metros cúbicos) 2000-2024" é a primeira da lista
        link_imp_exp_petroleo = lst_link_planilhas[0]

        # Fazendo o download da planilha
        response = requests.get(link_imp_exp_petroleo, verify=False)
        if response.status_code == 200:
            nome_arquivo = os.path.join(self.download_directory, os.path.basename(link_imp_exp_petroleo))
            with open(nome_arquivo, 'wb') as f:
                f.write(response.content)


def main():
    exp_imp_petroleo = ImpExpPetroleoANP()
    exp_imp_petroleo.download_arquivo()


if __name__ == "__main__":
    main()