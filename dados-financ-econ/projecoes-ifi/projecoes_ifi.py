import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from datetime import datetime


class WebScrapingProjecoesIFI:
    def __init__(self):
        # URL
        self.url = 'https://www12.senado.leg.br/ifi'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'close'
        }

    def web_scraping_data(self):
        # Fazendo a requisição HTTP para obter o conteúdo da página
        response = requests.get(self.url, headers=self.headers)

        # Criando o objeto BeautifulSoup para analisar o conteúdo HTML da página
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrando os elementos textuais
        elements_str = soup.find_all(
            'div', class_='col-xs-8 linha-simples-titulo'
        )
        # Encontrando os elementos numéricos
        elements_num = soup.find_all(
            'div', class_='col-xs-1 linha-simples-dado'
        )
        # Encontrando a data que a tabela foi atualizada
        data_atualizada = soup.find_all('ul', class_='projecoes-ul-linha')

        # Criando uma lista dos dados extraidos p/ transformar em um df. Listas que possuem uma condição que não extrai vazios
        list_txt = [element.text.strip()
                    for element in elements_str if element.text.strip()]
        list_num = [element.text.strip()
                    for element in elements_num if element.text.strip()]
        list_data_atualizada = [element.text.strip(
        ) for element in data_atualizada if element.text.strip()]

        # Selecionando apenas parte útil da string 'Última atualização: 25/05/2023 (RAF nº 76)'
        data_atualizacao = re.findall(
            r'\d{2}/\d{2}/\d{4}', list_data_atualizada[0])
        data_atualizacao = data_atualizacao[0]

        # Formatando a data '25/05/2023' para '20230525'
        data_obj = datetime.strptime(data_atualizacao, '%d/%m/%Y')
        # Data da última atualização p/ nomear o arquivo csv
        data_formatada = data_obj.strftime('%Y%m%d')
        # Data da última atualização p/ servir como index do df
        data_formatada_index = data_obj.strftime('%Y-%m-%d')
        # Criando uma lista com a data atualizada repitida 13 vezes
        lista_datas = [data_formatada_index for _ in range(13)]
        # Transformando a lista em um array NumPy
        array_datas = np.array(lista_datas)
        # Criando a matriz com 13 linhas e 1 coluna
        matriz_datas = array_datas.reshape(13, 1)
        lista_data_1d = matriz_datas.ravel()
        # Criando um df da data de atualização
        df_data_formatada = pd.DataFrame(lista_data_1d)

        # Criando o df dos tópicos
        df_topics = pd.DataFrame(list_txt, columns=['Topics'])

        # Criando o df dos números
        # Retorna os dados de 2023 e 2024 em apenas uma coluna -> Dados de 2023 (index pares) e 2024 (index ímpares)
        df_nums = pd.DataFrame(list_num, columns=['Num'])
        # Selecionando apenas as linhas que estão em um index par
        values_2023 = [df_nums['Num'][i]
                       for i in range(len(df_nums)) if i % 2 == 0]
        # Selecionando apenas as linhas que estão em um index ímpares
        values_2024 = [df_nums['Num'][i]
                       for i in range(len(df_nums)) if i % 2 != 0]
        # Criando um df com os dados númericos das projeções dos anos
        df_nums = pd.DataFrame({'2023': values_2023, '2024': values_2024})
        # Excluindo a primeira linha que são os anos (2023 e 2024)
        df_nums = df_nums.drop(df_nums.index[0])
        # O index atual desse df é de 1 a 13. Resetando o index para ficar igual ao index do df_topics (0 a 12) p/ fazer o merge
        df_nums = df_nums.reset_index(drop=True)

        # Mesclando os tres dfs
        df_projecoes_ifi = pd.merge(df_topics.merge(
            df_nums, left_index=True, right_index=True), df_data_formatada, left_index=True, right_index=True)
        # Renomeando a coluna 0 para 'Data'
        df_projecoes_ifi = df_projecoes_ifi.rename(columns={0: 'Data'})
        # Colocando a coluna 'Data' como index do df
        df_projecoes_ifi = df_projecoes_ifi.set_index('Data')

        # Tranformando em arquivo csv
        df_projecoes_ifi.to_csv(
            f'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//projecoes-ifi//projecoes_ifi_{data_formatada}.csv',
            sep=';'
        )


def main():
    ifi = WebScrapingProjecoesIFI()
    ifi.web_scraping_data()


if __name__ == "__main__":
    main()
