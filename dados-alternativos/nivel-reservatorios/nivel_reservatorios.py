import requests
import json
import pandas as pd
from datetime import datetime


class WebScrapingNivelReservatorios:
  def __init__(self):
    # URL
    url = "https://tr.ons.org.br/Content/Get/SituacaoDosReservatorios"

    response = requests.request("GET", url)
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
    regioes = [self.regiao_sudeste,
               self.regiao_sul,
               self.regiao_nordeste,
               self.regiao_norte
    ]

    niveis_reservatorios = [self.nivel_sudeste,
                            self.nivel_sul,
                            self.nivel_nordeste,
                            self.nivel_norte
    ]
    # Juntando as duas listas
    dados_reservatorios = dict(zip(regioes, 
                                   niveis_reservatorios))
    
    # Transformando em df
    df_reservatorios = pd.DataFrame(dados_reservatorios, 
                                    index=[data_atualizacao])
    
    # Retirando o horário deixando apenas a data
    df_reservatorios.index = df_reservatorios.index.date

    # Formatando a data de 'ano-mes-dia' para 'dia-mes-ano'
    df_reservatorios.index = df_reservatorios.index.map(
        lambda x: x.strftime('%d-%m-%Y'))
    
    # Retirando os espaços em branco nos nomes da coluna
    # e colocando em letra minúscula
    df_reservatorios.columns = (df_reservatorios
        .columns
        .str
        .replace(' ', '').str.lower()
    )
    # Colocandos os números com duas casas decimais
    self.df_reservatorios = df_reservatorios.applymap(
        lambda x: f"{x:.2f}")

  def load(self):
    self.df_reservatorios.to_csv(
      'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-alternativos//nivel-reservatorios//nivel_reservatorios.csv', 
      sep=';'
  )

def main():
  nvl_res = WebScrapingNivelReservatorios()
  nvl_res.extract()
  nvl_res.transform()
  nvl_res.load()


if __name__ == "__main__":
  main()

