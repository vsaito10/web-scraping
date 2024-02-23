import requests
from bs4 import BeautifulSoup
import re
import os


class WebScrapingProxyRate:
    def __init__(self):
        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3\web-scraping//dados-financ-econ//proxy-rate'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'close'
        }

        # Site do FED San Francisco
        url = 'https://www.frbsf.org/research-and-insights/data-and-indicators/proxy-funds-rate/'

        # Solicitando o HTTP GET do site do FED San Francisco
        response = requests.get(url, headers=self.headers)

        # HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Usando o regex para encontrar o link da planilha
        link_pattern = re.compile(r'/wp-content/uploads/proxy-funds-rate-data\.xlsx\?(\d+)')
        link = soup.find('a', href=link_pattern)
        # Selecionando o href -> '/wp-content/uploads/proxy-funds-rate-data.xlsx?20240105'
        href = link.get('href')

        # URL do download da planilha do Proxy Rate
        self.url_planilha = f'https://www.frbsf.org/{href}'

    def baixar_arquivo(self):
        response_planilha = requests.get(self.url_planilha, headers=self.headers)
        if response_planilha.status_code == 200:
            nome_arquivo = os.path.basename(self.url_planilha).split("?")[0]  # Obtém o nome do arquivo sem a parte da URL após o "?" -> 'proxy-funds-rate-data.xlsx'
            nome_arquivo = os.path.join(self.download_directory, nome_arquivo)
            with open(nome_arquivo, 'wb') as f:
                f.write(response_planilha.content)


def main():
    proxy_rate = WebScrapingProxyRate()
    proxy_rate.baixar_arquivo()


if __name__ == "__main__":
    main()
