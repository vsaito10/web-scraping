import os
import requests
from time import sleep

"""
Exceções encontradas no padrão da URL
Fiz o webscraping das atas 232 até a 256 - as atas '234' e '235' possuem um padrão diferente da URL do download do PDF
Ata 234 -> https://www.bcb.gov.br/content/copom/copomminutes/234th%20Copom%20Minutes.pdf
Ata 235 -> https://www.bcb.gov.br/content/copom/copomminutes/235th%20Meeting%20-%20December%208-9,%202020.pdf
"""

class AtasCopom:
    def __init__(self):
        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3//historico-arquivos//atas-pdf'

        # Lista que armazena as URLs das atas do COPOM
        self.lista_urls = [
            f'https://www.bcb.gov.br/content/copom/copomminutes/MINUTES%20{num_ata}.pdf' for num_ata in range(232, 257)]

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
                nome_arquivo = os.path.basename(
                    url).lower().replace("%20", "_")
                print(f'Baixando arquivo: {nome_arquivo}')
                nome_arquivo = os.path.join(
                    self.download_directory, nome_arquivo)
                with open(nome_arquivo, 'wb') as f:
                    f.write(response.content)
            else:
                print(
                    f'Falha ao baixar {url}, status code: {response.status_code}')

            sleep(3.5)


def main():
    proxy_rate = AtasCopom()
    proxy_rate.baixar_arquivos()


if __name__ == "__main__":
    main()
