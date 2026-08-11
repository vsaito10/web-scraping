import os
from datetime import datetime
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

# Fuso da B3 (horário de Brasília), usado para determinar a "data de hoje"
TZ_SAO_PAULO = ZoneInfo('America/Sao_Paulo')


class IpoB3:
    def __init__(self):
        # Diretório do download do arquivo (mesma pasta deste script)
        self.download_directory = os.path.dirname(os.path.abspath(__file__))

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

        # Tabela excel dos IPOs: pega todos os links '.xlsx' da página
        ipos_links = [
            link.get('href')
            for link in self.soup.find_all('a')
            if link.get('href') and link.get('href').lower().endswith('.xlsx')
        ]

        if not ipos_links:
            raise ValueError('Nenhum link .xlsx encontrado na página da B3 (a estrutura do site pode ter mudado).')

        # String do href -> "../../../../../data/files/DC/E0/7E/D6/16EAE8100E866AE8AC094EA8/Ofertas%20Publicas%20_Imprensa_%20-%20Marco.24%20_SITE_.xlsx"
        link_planilha = ipos_links[-1]

        # Resolvendo o caminho relativo ('../../../data/files/...') contra a URL da página
        link_planilha = urljoin(self.url, link_planilha)

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

            # Obtendo a data em que foi feito o download e formantando a data
            data_hoje = datetime.now(tz=TZ_SAO_PAULO).date()
            data_formatada = data_hoje.strftime("%Y%m%d")

            # Renomeando o arquivo para 'ipo.xlsx'
            novo_nome_arquivo = os.path.join(self.download_directory, f'lista_ipo_{data_formatada}.xlsx')
            os.rename(novo_caminho, novo_nome_arquivo)

            
def main():
    ipo = IpoB3()
    ipo.baixar_arquivo()


if __name__ == "__main__":
    main()