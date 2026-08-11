import base64
import datetime
import json
import os
import time
from zoneinfo import ZoneInfo

import pandas as pd
import requests

# Fuso da B3 (horário de Brasília), usado para determinar a "data de hoje"
TZ_SAO_PAULO = ZoneInfo('America/Sao_Paulo')


class buyback:
    def __init__(self):

        # Data usada na consulta (hoje)
        date_str = datetime.datetime.now(tz=TZ_SAO_PAULO).date().strftime('%Y-%m-%d')

        # Cabeçalhos comuns a todas as requisições
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'pt-BR,pt;q=0.9',
            'referer': 'https://sistemaswebb3-listados.b3.com.br/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
        }

        base_url = 'https://sistemaswebb3-listados.b3.com.br/stockProgramProxy/StockProgramCall/GetListedCompany/'

        # Sessão com "warmup" na home da B3 p/ obter cookies válidos (Cloudflare) automaticamente
        session = requests.Session()
        session.headers.update(headers)
        session.get('https://sistemaswebb3-listados.b3.com.br/', timeout=30)

        # Lista JSON
        self.lst_buyback_json = []

        # Iterando em cada página da B3 fazendo a requisição GET para a URL da B3
        page_number = 1
        while True:
            # O parâmetro da URL é um JSON codificado em base64 (compacto, sem espaços)
            payload = {
                'keyword': '',
                'date': date_str,
                'language': 'pt-br',
                'pageNumber': page_number,
                'pageSize': 20,
            }
            encoded = base64.b64encode(
                json.dumps(payload, separators=(',', ':')).encode()
            ).decode()

            # O Cloudflare da B3 retorna 404 esporádico; tentamos algumas vezes por página
            for _ in range(5):
                response = session.get(base_url + encoded, timeout=30)
                if response.status_code == 200:
                    break
                time.sleep(1)
            else:
                response.raise_for_status()

            buyback = response.json()
            self.lst_buyback_json.append(buyback)

            # Para quando chegar na última página
            if page_number >= buyback['page']['totalPages']:
                break
            page_number += 1
            time.sleep(0.6)

    def process_data(self):
        # Lista dos buybacks
        lst_buyback = []

        # Iterando sobre a lista JSON
        for i in range(len(self.lst_buyback_json)):
            df_buyback_result = pd.DataFrame(self.lst_buyback_json[i]['results'])
            lst_buyback.append(df_buyback_result)

        # Concatenando todos os DataFrames da lista em um único DataFrame
        df_buyback_final = pd.concat(lst_buyback, ignore_index=True)

        # Trocando a string '/' por '-'
        df_buyback_final['aprrovedDate'] = df_buyback_final['aprrovedDate'].str.replace('/', '-')
        df_buyback_final['startDate'] = df_buyback_final['startDate'].str.replace('/', '-')
        df_buyback_final['endDate'] = df_buyback_final['endDate'].str.replace('/', '-')

        # A recompra da OI está com um erro na coluna 'endDate' ('31-12-9999') tenho que retirar do df p/ transformar em datetime
        df_buyback_final = df_buyback_final.query("endDate != '31-12-9999'")

        # Fazendo uma cópia do df
        df_buyback_final =  df_buyback_final.copy()

        # Transformando as colunas em datetime
        df_buyback_final['aprrovedDate'] = pd.to_datetime(df_buyback_final['aprrovedDate'], format='%d-%m-%Y')
        df_buyback_final['startDate'] = pd.to_datetime(df_buyback_final['startDate'], format='%d-%m-%Y')
        df_buyback_final['endDate'] = pd.to_datetime(df_buyback_final['endDate'], format='%d-%m-%Y')

        # Separando a coluna 'quantity' em duas novas colunas ('type_stock' e 'quantity_only') - (ex: '2.000.000 (ON)') -> ('2.000.000') e ('ON')
        df_buyback_final['type_stock'] = df_buyback_final['quantity'].str.extract(r"\((.*?)\)")
        df_buyback_final['quantity_only'] = df_buyback_final['quantity'].str.replace(r"\(.*?\)", "", regex=True)

        # Separando a coluna 'company' em duas novas colunas ('segment' e 'ticker') - (ex: 'VIVARA (NM)') -> ('VIVARA') e ('NM')
        df_buyback_final['segment'] = df_buyback_final['company'].str.extract(r"\((.*?)\)")
        df_buyback_final['ticker'] = df_buyback_final['company'].str.replace(r"\(.*?\)", "", regex=True)

        # Selecionando as principais colunas
        df_buyback_final = df_buyback_final[['startDate', 'endDate', 'ticker', 'quantity_only', 'segment', 'type_stock']]

        # Ordenando o df
        df_buyback_final = df_buyback_final.sort_values(by='startDate')

        # Transformando a coluna 'quantity_only' em int
        df_buyback_final['quantity_only'] = df_buyback_final['quantity_only'].str.replace('.', '').astype(int)

        # Data do dia em que ocorreu o scraping dessa tabela
        data_atual = datetime.datetime.now(tz=TZ_SAO_PAULO).date()
        data_atual_str = data_atual.strftime('%Y-%m-%d')
        data_atual_str = data_atual_str.replace('-', '_')

        # Transformando em um arquivo csv (na mesma pasta deste script)
        output_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(output_dir, f'buyback_{data_atual_str}.csv')
        df_buyback_final.to_csv(output_path, sep=';')


def main():
    buyback_b3 = buyback()
    buyback_b3.process_data()

if __name__ == "__main__":
    main()