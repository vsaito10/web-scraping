import requests
from bs4 import BeautifulSoup
import os


class IpoB3:
    def __init__(self):
        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//ipo//'

        # URL
        self.url = 'https://www.b3.com.br/pt_br/produtos-e-servicos/solucoes-para-emissores/ofertas-publicas/estatisticas/'

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

        # Tabela excel dos IPOs (find all 'a' tags within 'div' with class 'content')
        planilha = self.soup.find_all('div', class_='content')

         # Lista para guardar os hrefs
        ipos_links = [] 
        for item in planilha:
            for link in item.find_all('a'):
                href = link.get('href')
                ipos_links.append(href)

        # String do href -> "../../../../../data/files/DC/E0/7E/D6/16EAE8100E866AE8AC094EA8/Ofertas%20Publicas%20_Imprensa_%20-%20Marco.24%20_SITE_.xlsx"
        link_planilha = ipos_links[-1]

        # Removendo a parte inicial da string
        link_planilha = link_planilha.strip('../../../')

        # Adicionando a string que falta p/ formar o link de download
        link_planilha = 'https://www.b3.com.br/' + link_planilha

        # Requisição para o link de download da planilha
        response = requests.get(link_planilha, headers=self.headers)

        # Fazendo o download do arquivo
        if response.status_code == 200:
            # Nome do arquivo
            nome_arquivo = os.path.basename(link_planilha)
            # Caminho completo do arquivo 
            novo_caminho = os.path.join(self.download_directory, nome_arquivo)

            with open(novo_caminho, 'wb') as f:
                f.write(response.content)

            # Renomeando o arquivo para 'ipo.xlsx'
            novo_nome_arquivo = os.path.join(self.download_directory, 'lista_ipo.xlsx')
            os.rename(novo_caminho, novo_nome_arquivo)

            
def main():
    ipo = IpoB3()
    ipo.baixar_arquivo()


if __name__ == "__main__":
    main()