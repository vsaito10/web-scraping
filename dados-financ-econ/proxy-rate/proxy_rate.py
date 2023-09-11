import os
import requests

class WebScrapingProxyRate:
    def __init__(self):
        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3\web-scraping//dados-financ-econ//proxy-rate'
        
        # URL do download do arquivo. Esse link é do site https://www.frbsf.org/economic-research/indicators-data/proxy-funds-rate/
        self.url = 'https://www.frbsf.org/wp-content/uploads/sites/4/proxy-funds-rate-data.xlsx?202305052'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'close'
        }

    def baixar_arquivo(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            nome_arquivo = os.path.basename(self.url).split("?")[0]  # Obtém o nome do arquivo sem a parte da URL após o "?" -> 'proxy-funds-rate-data.xlsx'
            nome_arquivo = os.path.join(self.download_directory, nome_arquivo)
            with open(nome_arquivo, 'wb') as f:
                f.write(response.content)


def main():
    proxy_rate = WebScrapingProxyRate()
    proxy_rate.baixar_arquivo()


if __name__ == "__main__":
    main()
