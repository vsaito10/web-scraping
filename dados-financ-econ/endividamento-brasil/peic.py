import requests
from bs4 import BeautifulSoup
import os
import re


class PesquisaPeic:
    def __init__(self):
        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//endividamento-brasil'

        # URL
        self.url = 'https://www.fecomercio.com.br/pesquisas/indice/peic'

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
        # Tabela excel da pesquisa PEIC
        planilha = self.soup.find_all('a', class_='download')
        # Extraindo apenas o link de download da planilha excel que está dentro de 'href' -> 'https://www.fecomercio.com.br/upload/file/2023/10/06/peic_link_download_202309.xlsx'
        self.link_planilha = planilha[0].get('href')
        
        # Requisição para o link de download da planilha
        response = requests.get(self.link_planilha, headers=self.headers)

        # Fazendo o download do arquivo
        if response.status_code == 200:
            nome_arquivo = os.path.basename(self.link_planilha)
            
            # Renomeando o arquivo de 'peic_link_download_202309.xlsx' para 'peic_202309.xlsx'
            novo_nome = re.sub(r'peic_link_download_', 'peic_', nome_arquivo)
            novo_caminho = os.path.join(self.download_directory, novo_nome)

            with open(novo_caminho, 'wb') as f:
                f.write(response.content)
            

def main():
    peic = PesquisaPeic()
    peic.baixar_arquivo()


if __name__ == "__main__":
    main()
