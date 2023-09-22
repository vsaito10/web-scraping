from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import re


"""
URLs:
PMI Serviços - https://br.investing.com/economic-calendar/services-pmi-1062
PMI Industrial - https://br.investing.com/economic-calendar/manufacturing-pmi-829
PMI ISM Não-Manufatura - https://br.investing.com/economic-calendar/ism-non-manufacturing-pmi-176
PMI ISM Industrial - https://br.investing.com/economic-calendar/ism-manufacturing-pmi-173

Neste código:
- Preciso mudar a URL do PMI
- Olhar como está o layout da tabela no site Investing em relação ao dado mais recente.
- se o último PMI lançado está na primeira linha da tabela - ela é uma tabela completa -> df = df.iloc[:]
- se o último PMI lançado está na segunda linha da tabela - ela possui uma linha em branco -> df = df.iloc[:-1]
- se o último PMI lançado está na terceira linha da tabela - ela possui duas linhas em branco -> df = df.iloc[:-2]

"""
class WebScrapingPMI:
    def __init__(self):
        options = Options()
        options.add_argument("--incognito")
        self.driver = webdriver.Firefox(options=options)

        self.url = 'https://br.investing.com/economic-calendar/services-pmi-1062'
        self.tipo_pmi = re.search(r"-(\d+)$", self.url).group(1)

    def acessar_site(self):
        self.driver.get(self.url)
        sleep(2)

    def botao_propaganda(self):
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="PromoteSignUpPopUp"]/div[2]/i'))
            )
            element.click()
        except:
            pass

    def botao_hist(self):
        while True:
            try:
                xpath_botao_hist = f'//*[@id="showMoreHistory{self.tipo_pmi}"]'
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_botao_hist)))
                element.click()
            except:
                break

    def web_scraping_tabela(self):
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
        df = df.rename(columns={
            'Lançamento': 'lancamento',
            'Hora': 'hora',
            'Atual': 'atual',
            'Projeção': 'projecao',
            'Anterior': 'anterior'
        })
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
        # As tabelas do PMI e PMI ISM são diferentes - o Investing acaba mudando essas tabelas (SEMPRE CONFERIR O LAYOUT DA TABELA) 
        # A PMI ISM é completa não deixa linha em branco com a projeção
        # A PMI deixa uma ou duas linhas em branco com a projeção
        if (self.tipo_pmi == '176') or (self.tipo_pmi == '173'):
            df = df.iloc[:]
            # Definindo coluna 'lancamento' como o index do df
            df = df.set_index('lancamento')
        elif (self.tipo_pmi == '1062') or (self.tipo_pmi == '829'):
            df = df.iloc[:-1]
            # Definindo coluna 'lancamento' como o index do df
            df = df.set_index('lancamento')

        # Substituindo as 'vírgulas' dos números por 'ponto'
        df['atual'] = df['atual'].str.replace(',', '.')
        df['projecao'] = df['projecao'].str.replace(',', '.')
        df['anterior'] = df['anterior'].str.replace(',', '.')

        # Transformando em um arquivo csv
        df.to_csv(f'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//pmi//atualizado//{text_title}.csv', sep=';')
           
    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    pmi = WebScrapingPMI()
    pmi.acessar_site()
    pmi.botao_propaganda()
    pmi.botao_hist()
    pmi.web_scraping_tabela()
    pmi.fechar_site()


if __name__ == "__main__":
    main()

