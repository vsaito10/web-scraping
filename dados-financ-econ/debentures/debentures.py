import datetime
import os
import re
import requests


class Debentures:
    def __init__(self):
        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//debentures'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'close'
        }

    def baixar_arquivo(self):
        # Selecionando a data atual
        data_atual = datetime.date.today()

        # Dia anterior da data atual
        dia = data_atual.day - 1

        # Selecionando o mês -> tenho que substituir o nº do mês pela sua string
        dict_mes = {
            1: 'jan',
            2: 'fev',
            3: 'mar',
            4: 'abr',
            5: 'mai',
            6: 'jun',
            7: 'jul',
            8: 'ago',
            9: 'set',
            10: 'out',
            11: 'nov',
            12: 'dez'
        }

        mes_string = dict_mes[data_atual.month]

        # Selecionando o ano -> 2024 -> quero apenas os dois últimos números (24)
        ano = data_atual.year
        ano_str = str(ano)
        match = re.search(r'\d{2}$', ano_str)
        ano_resumido = match.group()

        # URL do download da planilha - padrão da URL -> 'https://www.anbima.com.br/informacoes/merc-sec-debentures/arqs/d24jul18.xls'
        url_planilha = f'https://www.anbima.com.br/informacoes/merc-sec-debentures/arqs/d{ano_resumido}{mes_string}{dia}.xls'

        # Fazendo o download da URL
        response_planilha = requests.get(url_planilha, headers=self.headers)
        if response_planilha.status_code == 200:
            # Definindo o nome para o arquivo
            nome_arquivo = f'd{ano_resumido}{mes_string}{dia}.xls'
            caminho_completo = os.path.join(self.download_directory, nome_arquivo)
            with open(caminho_completo, 'wb') as f:
                f.write(response_planilha.content)


def main():
    debentures = Debentures()
    debentures.baixar_arquivo()


if __name__ == "__main__":
    main()
