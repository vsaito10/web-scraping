import requests
import json
import pandas as pd
from datetime import datetime


class WebScrapingNivelReservatorios:

    def __init__(self):
        url = "https://tr.ons.org.br/Content/Get/SituacaoDosReservatorios"

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "pt-BR,pt;q=0.5",
            "Connection": "keep-alive",
            "Origin": "https://www.ons.org.br",
            "Referer": "https://www.ons.org.br/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "sec-ch-ua": "^\^Not/A",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\^Windows^^"
        }

        response = requests.request("GET", url, headers=headers)
        self.data = json.loads(response.text)

    def extract(self):
        # Selecionando as regiões
        self.regiao_norte = self.data[1]['Subsistema']
        self.regiao_nordeste = self.data[3]['Subsistema']
        self.regiao_sul = self.data[7]['Subsistema']
        self.regiao_sudeste = self.data[19]['Subsistema']

        # Selecionando as porcentagens dos níveis dos reservatórios
        self.nivel_norte = self.data[1]['SubsistemaValorUtil']
        self.nivel_nordeste = self.data[3]['SubsistemaValorUtil']
        self.nivel_sul = self.data[7]['SubsistemaValorUtil']
        self.nivel_sudeste = self.data[19]['SubsistemaValorUtil']

        # Selecionando a data da última atualização
        self.data_atualizacao = self.data[0]['Data']

    def transform(self):
        # Transformando em datetime a data de atualização
        data_atualizacao = pd.to_datetime(self.data_atualizacao)

        # Juntando os dados em duas listas
        regioes = [
            self.regiao_sudeste,
            self.regiao_sul,
            self.regiao_nordeste,
            self.regiao_norte
        ]

        niveis_reservatorios = [
            self.nivel_sudeste,
            self.nivel_sul,
            self.nivel_nordeste,
            self.nivel_norte
        ]
        # Juntando as duas listas
        dados_reservatorios = dict(zip(regioes, niveis_reservatorios))
        # Transformando em df
        df_reservatorios = pd.DataFrame(
            dados_reservatorios, index=[data_atualizacao])
        # Retirando o horário deixando apenas a data
        df_reservatorios.index = df_reservatorios.index.date
        # Formatando a data de 'ano-mes-dia' para 'dia-mes-ano'
        df_reservatorios.index = df_reservatorios.index.map(
            lambda x: x.strftime('%d-%m-%Y')
        )
        # Retirando os espaços em branco nos nomes da coluna e colocando em letra minúscula
        df_reservatorios.columns = df_reservatorios.columns.str.replace(
            ' ', '').str.lower()
        # Transformando os números em porcentagem
        self.df_reservatorios = df_reservatorios.applymap(
            lambda x: f"{x:.2f}%"
        )

    def load(self):
        # Atualizando o arquivo csv com os novos dados (todo dia esse site é atualizado)
        try:
            nivel_reservatorios_final = pd.read_csv(
                'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-alternativos//nivel-reservatorios//nivel_reservatorios_final.csv',
                sep=';',
                index_col='Unnamed: 0'
            )
        except FileNotFoundError:
            print("O arquivo csv não foi encontrado.")

        # Concatenando o DataFrame existente com os novos dados
        nivel_reservatorios_final = pd.concat([
            nivel_reservatorios_final,
            self.df_reservatorios
        ])

        nivel_reservatorios_final.to_csv(
            'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-alternativos//nivel-reservatorios//nivel_reservatorios_final.csv',
            sep=';'
        )


def main():
    nivel_reservatorios = WebScrapingNivelReservatorios()
    nivel_reservatorios.extract()
    nivel_reservatorios.transform()
    nivel_reservatorios.load()


if __name__ == "__main__":
    main()
