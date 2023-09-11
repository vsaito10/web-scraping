from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd


class WebScrapingIntervalosInflacao:
    def __init__(self):

        self.service = Service(GeckoDriverManager().install())
        options = Options()
        options.add_argument("--headless")  # Executar em modo headless (sem abrir o navegador)
        options.add_argument("--no-sandbox")  # Evitar erro de sandbox
        options.add_argument("--disable-dev-shm-usage")  # Evitar erro de uso de memória
        options.add_argument("--disable-gpu")  # Desabilitar a GPU
        self.driver = webdriver.Firefox(service=self.service, options=options)

    def acessar_site(self):
        self.driver.get(
            'https://www.bcb.gov.br/controleinflacao/historicometas')
        self.driver.implicitly_wait(3)

    def web_scraping_table(self):

        # Descobrindo o nº de linhas da tabela. Somo mais 1, porque a 1º sublista é vazia
        rows = self.driver.find_elements(
                By.XPATH, f'/html/body/app-root/app-root/div/div/main/dynamic-comp/div/div[7]/div/div/table/tbody/tr')
        len_tabela = len(rows)+1

        # Iterando sobre as linhas da tabela, retorna uma lista com várias sublistas
        data_rows = []
        for i in range(len_tabela):
            rows = self.driver.find_elements(
                By.XPATH, f'/html/body/app-root/app-root/div/div/main/dynamic-comp/div/div[7]/div/div/table/tbody/tr[{i}]')

            col_texts = [col_element.text for col_element in rows]
            data_rows.append(col_texts)

        # Removendo as sublistas vazias.
        lista_row = [dado_row[0] for dado_row in data_rows if dado_row]

        # Separando o conteúdo de cada sublista e sem vazios - ex: ['1999', 'Resolução CMN nº 2.615', '30/6/1999', '8', '2', '6-10', '8,94']
        lista_dados = [list(filter(None, string.split('\n')))
                       for string in lista_row]

        # Descobrindo qual é a maior lista
        maior_lista = max(lista_dados, key=len)

        # Definindo o número de colunas do df
        num_colunas = len(maior_lista)

        # Preenchendo as sublistas com vazios para as listas terem o mesmo número de elementos
        lista_dados = [sublista + [''] *
                       (num_colunas - len(sublista)) for sublista in lista_dados]

        # # Criando o dataframe - nomes das colunas vão de 0 a 12
        df = pd.DataFrame(lista_dados)
        
        # Retirando o '*' dos anos de 2003 e 2004
        df[0] = df[0].str.strip().str.replace('*', '')

        # Em 2003, a coluna 'Inflação efetiva' tem o valor duplicado '9.3'. Por isso eu retirar a último coluna
        df = df.drop(12, axis=1)

        # Arrumando as linhas dos anos 2003 e 2004
        # Concatenando as normas
        norma = df.apply(lambda row: row[1] + ' e ' + row[2], axis=1)
        norma_2003 = norma[4]
        norma_2004 = norma[5]

        # Concatenando as datas
        data = df.apply(lambda row: row[3] + ' e ' + row[4], axis=1)
        data_2003 = data[4]
        data_2004 = data[5]

        # Concatenando as metas
        meta = df.apply(lambda row: row[5] + ' e ' + row[6], axis=1)
        meta_2003 = meta[4]
        meta_2004 = meta[5]

        # Concatenando os intervalos
        intervalo = df.apply(lambda row: row[7] + ' e ' + row[8], axis=1)
        intervalo_2003 = intervalo[4]
        intervalo_2004 = intervalo[5]

        # Concatenando as tolerâncias
        tolerancia = df.apply(lambda row: row[9] + ' e ' + row[10], axis=1)
        tolerancia_2003 = tolerancia[4]
        tolerancia_2004 = tolerancia[5]

        # Substituindo os valores das linhas de 2003 e 2004
        df.iloc[4, 1] = norma_2003
        df.iloc[5, 1] = norma_2004

        df.iloc[4, 2] = data_2003
        df.iloc[5, 2] = data_2004

        df.iloc[4, 3] = meta_2003
        df.iloc[5, 3] = meta_2004

        df.iloc[4, 4] = intervalo_2003
        df.iloc[5, 4] = intervalo_2004

        df.iloc[4, 5] = tolerancia_2003
        df.iloc[5, 5] = tolerancia_2004

        df.iloc[4, 6] = df.iloc[4, 11]
        df.iloc[5, 6] = df.iloc[5, 11]

        # Como ocorreu as substituições dos anos de 2003 e 2004, retirando as últimas colunas
        df = df.drop([7, 8, 9, 10, 11], axis=1)

        # Arrumando as linhas dos anos 2000 e 2001
        df.iloc[1] = df.iloc[1].shift(2)
        df.iloc[2] = df.iloc[2].shift(2)

        df.iloc[1, 0] = '2000'
        df.iloc[2, 0] = '2001'

        df.iloc[1, 1] = 'Resolução CMN nº 2.615'
        df.iloc[2, 1] = 'Resolução CMN nº 2.615'

        df.iloc[1, 2] = '30/6/1999'
        df.iloc[2, 2] = '30/6/1999'

        # Preenchendo os vazios com 0
        df.iloc[24, 6] = 0
        df.iloc[25, 6] = 0
        df.iloc[26, 6] = 0

        # Renomeando as colunas
        df = df.rename(columns={
            0: 'ano',
            1: 'norma',
            2: 'data',
            3: 'meta',
            4: 'tamanho_intervalo',
            5: 'intervalo_tolerancia',
            6: 'inflacao_efetiva'
        })

        # Selecionando apenas as colunas principais
        df = df[['ano', 'tamanho_intervalo']]

        # Retirando um dos intervalos dos anos de 2002 e 2003. Trocando a vírgula por ponto
        df['tamanho_intervalo'] = df['tamanho_intervalo'].str.replace('2 e ', '').str.replace('2,5 e ', '').str.replace(',', '.')

        # Transformando os dtypes
        df['ano'] = pd.to_datetime(df['ano'])
        df['tamanho_intervalo'] = df['tamanho_intervalo'].astype(float)

        # Transformando a coluna 'ano' no index do dataframe
        df = df.set_index('ano')

        # Transformando
        df.to_excel('C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//intervalos-ipca//df_intervalo_ipca.xlsx')
 

    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    intervalos_ipca = WebScrapingIntervalosInflacao()
    intervalos_ipca.acessar_site()
    intervalos_ipca.web_scraping_table()
    intervalos_ipca.fechar_site()


if __name__ == "__main__":
    main()