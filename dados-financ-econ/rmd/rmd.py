from bs4 import BeautifulSoup
import os
import re
import requests

class Rmd:
    def __init__(self):
        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//rmd'

        # URL
        self.url = 'https://www.tesourotransparente.gov.br/ckan/dataset/emissoes-e-resgates-divida-publica-federal/resource/bf69babd-ac07-40ce-90ff-c8e07ec8c8bf'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'close'
        }

        # Fazendo a requisição HTTP para obter o conteúdo da página
        response = requests.get(self.url, headers=self.headers)

        # Criando o objeto BeautifulSoup para analisar o conteúdo HTML da página
        self.soup = BeautifulSoup(response.content, 'html.parser')
        
    def baixar_arquivo(self):
        # Href da planilha
        planilha = self.soup.find('a', class_='btn btn-primary resource-url-analytics resource-type-None')
        if planilha:
            link_planilha = planilha['href']
        else:
            print('Link não encontrado')

        # Requisição para o link de download da planilha
        response = requests.get(link_planilha, headers=self.headers)

        # Fazendo o download do arquivo
        if response.status_code == 200:
            nome_arquivo = os.path.basename(link_planilha)
            
            # Renomeando o arquivo de '1.1.xlsx' para 'rmd_1.1.xlsx'
            novo_nome = re.sub(r'1.1', 'rmd_1.1', nome_arquivo)
            novo_caminho = os.path.join(self.download_directory, novo_nome)

            with open(novo_caminho, 'wb') as f:
                f.write(response.content)


def main():
    rmd = Rmd()
    rmd.baixar_arquivo()

if __name__ == "__main__":
    main()
