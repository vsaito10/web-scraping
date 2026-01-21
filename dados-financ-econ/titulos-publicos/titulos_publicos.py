import os
import requests
from time import sleep

class WebScrapingTitulosPublicos:
    def __init__(self):

        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//titulos-publicos//dados'

    def download_arquivo(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            nome_arquivo = os.path.join(self.download_directory, os.path.basename(url))
            with open(nome_arquivo, 'wb') as f:
                f.write(response.content)

    def loop_download_arquivo(self):
        # Lista com as URLs dos downloads dos arquivos. Esses links são do site https://www.tesourodireto.com.br/titulos/historico-de-precos-e-taxas.htm
        links = [
            'https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/2025/NTN-B_2025.xls',
            'https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/2025/NTN-B_Principal_2025.xls',
            'https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/2025/LTN_2025.xls',
        ]

        for link in links:
            self.download_arquivo(link)
            sleep(5)  # Intervalo entre downloads


def main():
    titulos_publicos = WebScrapingTitulosPublicos()
    titulos_publicos.loop_download_arquivo()


if __name__ == "__main__":
    main()
