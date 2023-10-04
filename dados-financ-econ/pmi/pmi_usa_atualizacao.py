from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import re


"""
URLS:
PMI Serviços - https://br.investing.com/economic-calendar/services-pmi-1062
PMI Industrial - https://br.investing.com/economic-calendar/manufacturing-pmi-829
PMI ISM Não-Manufatura - https://br.investing.com/economic-calendar/ism-non-manufacturing-pmi-176
PMI ISM Industrial - https://br.investing.com/economic-calendar/ism-manufacturing-pmi-173

Neste código:
- Preciso mudar a URL do PMI
- Olhar como está o layout da tabela, se o último PMI lançado está na penúltima ou antepenúltima linha
- se o último PMI lançado está na última linha - df = df.iloc[:-1]
- se o último PMI lançado está na penúltima linha - df = df.iloc[:-2]
- se o último PMI lançado está na antepenúltima linha - df = df.iloc[:-3]
"""

class WebScrapingAtualizacaoPMI:
    def __init__(self):
        options = Options()
        options.add_argument("--incognito")
        self.driver = webdriver.Firefox(options=options)

    def acessar_site(self, url_pmi: str):
        url = url_pmi
        self.tipo_pmi = re.search(r"-(\d+)$", url).group(1)
        self.driver.get(url)
        sleep(2)

    def web_scraping_tabela(self, filename: str):
        # Obtendo o conteúdo da página após a interação com o Selenium
        html_content = self.driver.page_source

        # Criando o objeto BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Encontrando o título do PMI
        title = soup.find('h1', class_='ecTitle float_lang_base_1 relativeAttr')
        text_title = title.text.strip().lower()
        # Procurando as palavras 'serviços', 'industrial', 'pmi', 'ism' e 'não-manufatura'. Retorna uma lista
        match = re.findall(r"\b(serviços|industrial|pmi|ism|não-manufatura)\b", text_title)
        # Substituindo a palavra 'serviços' por 'servicos'
        if 'serviços' in match:
            match[1] = match[1].replace('ç', 'c')
        # Substituindo a palavra 'não-manufatura' por 'nao_manufatura'
        elif 'não-manufatura' in match:
            match[2] = match[2].replace('ã', 'a').replace('-', '_')
        # Juntando as palavras ('services_pmi' ou 'manufacturing_pmi' ou 'pmi_industrial_ism' ou 'pmi_ism_nao_manufatura')
        text_title = "_".join(match).lower()

        # ID da tabela
        table_id = f'eventHistoryTable{self.tipo_pmi}'

        # Encontrando a tabela desejada usando o ID da tabela
        table = soup.find('table', id=table_id)

        # Criando o dataframe
        data = []
        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:
                cells = row.find_all('td')
                if cells:
                    data_row = {
                        'Lançamento': cells[0].text.strip(),
                        'Hora': cells[1].text.strip(),
                        'Atual': cells[2].text.strip(),
                        'Projeção': cells[3].text.strip(),
                        'Anterior': cells[4].text.strip()
                    }
                    data.append(data_row)
                else:
                    print("Sem células na linha")
        else:
            print("Tabela não encontrada no HTML")

        # Criando o df
        df = pd.DataFrame(data)
        # Invertendo as ordens das linhas (primeira linha que são os dados mais recentes vão ser as últimas linhas)
        df = df[::-1]
        # Renomeando as colunas
        df = df.rename(columns={'Lançamento': 'Lancamento',
                                'Projeção': 'Projecao'})
        # Transformandos os nomes da colunas em minúsculas
        df.columns = df.columns.str.lower()
        # Retirando os meses em parênteses
        df['lancamento'] = df['lancamento'].str.extract(r'(\d{2}\.\d{2}\.\d{4})(?:\s+\(.*\))?')
        # Trocando os '.' por '-' na data
        df['lancamento'] = df['lancamento'].str.replace('.', '-')
        # Trocando a posição do dia e mês para ficar na formatação (mês/dia/ano)
        df['lancamento'] = df['lancamento'].str.replace(r'(\d+)-(\d+)-(\d+)', r'\2-\1-\3', regex=True)
        # Transformando em datetime
        df['lancamento'] = pd.to_datetime(df['lancamento'], format='%m-%d-%Y')
        # Selecionando apenas as colunas mais importantes
        df = df[['lancamento', 'atual', 'projecao', 'anterior']]

        # A posição do dado mais recente muda entre 'PMI' (última linha) e 'PMI ISM' (penúltima linha)
        if (self.tipo_pmi == '176') or (self.tipo_pmi == '173'):
            ultimo_dado = df.iloc[-1]

        elif (self.tipo_pmi == '1062') or (self.tipo_pmi == '829'):
            ultimo_dado = df.iloc[-2]

        # Criando um df apenas com o dado mais recente - para ficar no mesmo formato da tabela eu tenho que transpor (T)
        df_ultimo_dado = pd.DataFrame(ultimo_dado).T
        # Definindo coluna 'lancamento' como o index do df
        df_ultimo_dado = df_ultimo_dado.set_index('lancamento')
        # Selecionando apenas a data retirando o horário (00:00:00)
        df_ultimo_dado.index = df_ultimo_dado.index.date
        # Renomeando o nome do index para 'Unnamed: 0'
        df_ultimo_dado.index.name = 'Unnamed: 0'

        # Substituindo as 'vírgulas' dos números por 'ponto'
        df_ultimo_dado['atual'] = df_ultimo_dado['atual'].str.replace(',', '.')
        df_ultimo_dado['projecao'] = df_ultimo_dado['projecao'].str.replace(',', '.')
        df_ultimo_dado['anterior'] = df_ultimo_dado['anterior'].str.replace(',', '.')
        
        # Abrindo o arquivo completo para atualizá-lo
        df_completo = pd.read_csv(
            f'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//pmi//atualizado//{filename}.csv', 
            sep=';',
            index_col='Unnamed: 0'
        )
        # Concatenando os dois dfs
        df_completo = pd.concat([df_completo, df_ultimo_dado], axis=0)
        # Transformando em um arquivo csv
        df_completo.to_csv(
            f'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//pmi//atualizado//{filename}.csv', 
            sep=';'
        )
             
    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    pmi = WebScrapingAtualizacaoPMI()
    pmi.acessar_site(url_pmi='https://br.investing.com/economic-calendar/services-pmi-1062')
    pmi.web_scraping_tabela(filename='pmi_servicos')
    pmi.fechar_site()


if __name__ == "__main__":
    main()
