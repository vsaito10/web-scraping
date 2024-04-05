from bs4 import BeautifulSoup  
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


class WebScrapingSP500EY:
    def __init__(self):
        self.driver = webdriver.Firefox()  

    def acessar_site(self):
        self.driver.get('https://www.multpl.com/s-p-500-earnings-yield/table/by-month')

    def web_scraping_table(self):
        table_element = self.driver.find_element(By.XPATH, '//*[@id="_table"]')  

        soup = BeautifulSoup(table_element.get_attribute('innerHTML'), 'html.parser')

        # Extraindo a tabela
        data = []
        for row in soup.find_all('tr'):
            row_data = []
            for cell in row.find_all('td'):  
                row_data.append(cell.text.strip())  
            if row_data: 
                data.append(row_data)

        # Transformando em df
        df = pd.DataFrame(data)

        # Selecionando as principais colunas
        df = df[[0, 1]]
        # Renomeando as colunas do df
        df = df.rename(columns={0: 'Date', 1: 'EY'})
        # Transformando em datetime
        df['Date'] = pd.to_datetime(df['Date'])
        # Formatando a data
        df['Date'] = df['Date'].dt.strftime('%m-%d-%Y')
        # Transformando a coluna 'Date' no index
        df = df.set_index('Date')
        # Retirando a string '†\n' e '%'
        df['EY'] = df['EY'].str.replace('†\n', '').str.replace('%', '')
        # Transformando o dtype em float
        df['EY'] = df['EY'].astype(float)
        # Invertendo as linhas do df
        df = df[::-1]
        # Transformando em um arquivo csv
        df.to_csv('C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//sp500-ratios//sp500_ey.csv')

    def fechar_site(self):
        self.driver.quit()

def main():
    sp500_ey = WebScrapingSP500EY()
    sp500_ey.acessar_site()
    sp500_ey.web_scraping_table()
    sp500_ey.fechar_site()


if __name__ == "__main__":
    main()