import requests
from bs4 import BeautifulSoup
import os


class VGIR11:
    def __init__(self):
        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//fii//vgir11'
                                     
        # URL
        self.url = 'https://valorainvest.com.br/fundo/vgir11/'

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
        # Tabela excel dos relatórios do VGIR11
        planilha = self.soup.find('div', id='relatorios')

        # Selecionando todos os links dentro dessa 'div'
        links = []
        for a in planilha.find_all('a', href=True):
            links.append(a['href'])

        # Link da planilha mais atual - sempre é a primeira
        self.link_planilha = links[0]

        # Requisição para o link de download da planilha
        response = requests.get(self.link_planilha, headers=self.headers)

       # Fazendo o download do arquivo
        if response.status_code == 200:
            # Nome do arquivo
            nome_arquivo = os.path.basename( self.link_planilha)
            # Caminho completo do arquivo 
            novo_caminho = os.path.join(self.download_directory, nome_arquivo)

            with open(novo_caminho, 'wb') as f:
                f.write(response.content)

def main():
    vgir11 = VGIR11()
    vgir11.baixar_arquivo()


if __name__ == "__main__":
    main()
