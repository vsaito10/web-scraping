from bs4 import BeautifulSoup
import pandas as pd
import re
import requests


class AbrasMercado:
    def __init__(self):
        # URL
        self.url = 'https://www.abras.com.br/economia-e-pesquisa/abrasmercado/historico'

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
        
    def scraping_tabela(self):

        # Tabelas da abrasmercado
        tabelas = self.soup.find_all('table')

        # Scraping das tabelas
        dados = []
        ano_atual = None  # Variável para armazenar o ano atual

        for tabela in tabelas:
            for linha in tabela.find_all('tr'):
                colunas = linha.find_all('td')

                # Verifica se o td tem colspan="3" -> isso indica que é um novo ano
                if len(colunas) == 1 and colunas[0].has_attr('colspan'):
                    ano_atual = colunas[0].text.strip()  # Armazena o ano atual
                    continue  # Pula para a próxima linha
                
                if len(colunas) == 3:  # Linha com os dados do mês
                    mes = colunas[0].text.strip()
                    mes_ano = f'{mes}/{ano_atual}' if ano_atual else mes  # Concatena com o ano correto
                    indice = colunas[1].text.strip()  
                    variacao = colunas[2].text.strip()

                    dados.append([mes_ano, indice, variacao])

        # Transformando em um self.df
        self.df = pd.DataFrame(dados, columns=['data', 'valor', 'pct_change'])

    def formatando_tabela(self):
        # As 8 primeiras linhas (header original e jan/2001 a jul/2001) não possuem dados
        self.df = self.df.iloc[8:]

        # Removendo as linhas que possuem a string 'Valor em R$'
        self.df =self.df.drop(self.df.loc[self.df['valor'] == 'Valor em R$'].index)

        # Removendo a coluna 'pct_change'
        self.df = self.df.drop(['pct_change'], axis=1)

        def corrigir_ano_duplicado(data):
            """
            Corrige as strings dos anos duplicados.

            Args:
                data: A string da data a ser corrigida.

            Returns:
                A string da data corrigida.
            """
            # Encontra todos os padrões de ano duplicado (ex: 'Janeiro/2024/2024' -> 'Janeiro/2024')
            padrao = r'/\d{4}/\d{4}'
            
            # Se um padrão for encontrado, remove a segunda ocorrência do ano
            if re.search(padrao, data):
                data = re.sub(r'/\d{4}', '', data, count=1)
            return data

        # Aplicando a função na coluna 'data' 
        self.df['data'] = self.df['data'].apply(corrigir_ano_duplicado)

        # Dicionário dos meses
        dict_ano = {
        'Janeiro': '01',
        'Fevereiro': '02',
        'Março': '03',
        'Abril': '04',
        'Maio': '05',
        'Junho': '06',
        'Julho': '07',
        'Agosto': '08',
        'Setembro': '09',
        'Outubro': '10',
        'Novembro': '11',
        'Dezembro': '12'
        }

        # Substituindo a string do mês pelo seu número
        self.df['data'] = self.df['data'].replace(dict_ano, regex=True)

        # Formatando as colunas
        self.df['valor'] = self.df['valor'].str.replace(',', '.').astype(float)
        self.df['data'] = self.df['data'].str.replace('/', '-')
        self.df['data'] = pd.to_datetime(self.df['data'], format='%m-%Y')

        # Calculando a variação percentual
        self.df['pct_change'] = self.df['valor'].pct_change()
        
        # Transformando a coluna 'data' no index 
        self.df = self.df.set_index('data')

        # Última data
        last_year = self.df.index[-1].year
        last_month = str(self.df.index[-1].month).zfill(2)  
        last_date = f'{last_year}{last_month}'

        # Transformando em um arquivo csv
        self.df.to_csv(
            f'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-alternativos//abrasmercado//abrasmercado_{last_date}.csv', 
            sep=';'
        )

def main():
    abrasmercado = AbrasMercado()
    abrasmercado.scraping_tabela()
    abrasmercado.formatando_tabela()


if __name__ == "__main__":
    main()