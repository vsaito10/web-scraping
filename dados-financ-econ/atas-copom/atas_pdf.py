# import os
# import requests

# class AtasCopom:
#     def __init__(self):
#         # Diretório do download do arquivo
#         self.download_directory = 'C://Users//vitor//projetos_python//python_b3\web-scraping//dados-financ-econ//atas-copom'
        
#         # URL do download do arquivo. Esse link é do site https://www.frbsf.org/economic-research/indicators-data/proxy-funds-rate/
#         self.url = 'https://www.bcb.gov.br/content/copom/copomminutes/MINUTES%20256.pdf'
                    
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.5',
#             'DNT': '1',
#             'Connection': 'close'
#         }

#     def baixar_arquivo(self):
#         response = requests.get(self.url, headers=self.headers)
#         if response.status_code == 200:
#             # Transformando o nome do arquivo 'MINUTES%20256.pdf' para 'minutes_256.pdf'
#             nome_arquivo = os.path.basename(self.url).lower().replace("%20", "_")
#             print(nome_arquivo)
#             nome_arquivo = os.path.join(self.download_directory, nome_arquivo)
#             with open(nome_arquivo, 'wb') as f:
#                 f.write(response.content)


# def main():
#     proxy_rate = AtasCopom()
#     proxy_rate.baixar_arquivo()


# if __name__ == "__main__":
#     main()


import os
import requests
from time import sleep

class AtasCopom:
    def __init__(self):
        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//atas-copom//arquivo-pdf'
        
        # Lista que armazena as URLs das atas do COPOM
        self.lista_urls = [f'https://www.bcb.gov.br/content/copom/copomminutes/MINUTES%20{num_ata}.pdf' for num_ata in range(250, 257)]

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'close'
        }

    def baixar_arquivos(self):
        for url in self.lista_urls:

            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                # Transformando o nome do arquivo 'MINUTES%20256.pdf' para 'minutes_256.pdf'
                nome_arquivo = os.path.basename(url).lower().replace("%20", "_")
                print(f'Baixando arquivo: {nome_arquivo}')
                nome_arquivo = os.path.join(self.download_directory, nome_arquivo)
                with open(nome_arquivo, 'wb') as f:
                    f.write(response.content)
            else:
                print(f'Falha ao baixar {url}, status code: {response.status_code}')
            
            sleep(3.5)


def main():
    proxy_rate = AtasCopom()
    proxy_rate.baixar_arquivos()


if __name__ == "__main__":
    main()