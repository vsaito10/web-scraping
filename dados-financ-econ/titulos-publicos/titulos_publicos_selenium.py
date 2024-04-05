from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
import requests


class WebScrapingTitulosPublicos:
    def __init__(self):

        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//titulos-publicos//dados'

        self.driver = webdriver.Firefox()

    def acessar_site(self):
        self.driver.get('https://www.tesourodireto.com.br/titulos/historico-de-precos-e-taxas.htm')
        sleep(1)

        # Localize e clique no botão de aceitar cookies
        try:
            botao_cookie = self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
            botao_cookie.click()
        except:
            pass

    def links_planilhas(self):
        # Obtendo o HTML 
        html = self.driver.page_source

        # Analisando o HTML com BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Encontrando todos os elementos <a> dentro da div com a classe 'td-download-docs-box'
        links = soup.find_all('a', class_='td-download-docs-card anual')

        # Iterando sobre os links encontrados e obtenha o atributo 'href' de cada um
        lst_links = []
        for link in links:
            href = link['href']
            lst_links.append(href)

        # Não preciso dos dois primeiros links da lista ('valor-nominal-de-ntn-b' e 'valor-nominal-de-ntn-c')
        self.lst_links = lst_links[2:]

    def download_planilhas(self):
        # Iterando sobre os links das planilhas p/ fazer o seu download
        for link in self.lst_links:
            response = requests.get(link)
            if response.status_code == 200:
                nome_arquivo = os.path.join(self.download_directory, os.path.basename(link))
                with open(nome_arquivo, 'wb') as f:
                    f.write(response.content)
                    sleep(5)

    def fechar_site(self):
        self.driver.quit()


def main():
    titulos_publicos = WebScrapingTitulosPublicos()
    titulos_publicos.acessar_site()
    titulos_publicos.links_planilhas()
    titulos_publicos.download_planilhas()
    titulos_publicos.fechar_site()


if __name__ == "__main__":
    main()

