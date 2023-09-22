import os
import requests
from time import sleep


class AtasCopom:
    def __init__(self):
        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3//historico-arquivos//minutes-pdf'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'close'
        }

    def baixar_arquivos(self, num_ata):
        # Lista que armazena as URLs das atas do COPOM
        self.url = f'https://www.bcb.gov.br/content/copom/copomminutes/MINUTES%20{num_ata}.pdf'

        response = requests.get(self.url, headers=self.headers)

        if response.status_code == 200:
            # Transformando o nome do arquivo 'MINUTES%20256.pdf' para 'minutes_256.pdf'
            nome_arquivo = os.path.basename(self.url).lower().replace("%20", "_")
            print(f'Baixando arquivo: {nome_arquivo}')
            nome_arquivo = os.path.join(self.download_directory, nome_arquivo)
            with open(nome_arquivo, 'wb') as f:
                f.write(response.content)
        else:
            print(f'Falha ao baixar {self.url}, status code: {response.status_code}')

        sleep(2)


def main():
    atas = AtasCopom()
    atas.baixar_arquivos(num_ata=256)


if __name__ == "__main__":
    main()
