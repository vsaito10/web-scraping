from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
import requests


class NovoCaged:
    def __init__(self, mes, ano):
        # Diretório do download do arquivo 
        self.path_download = r'C:\Users\vitor\projetos_python\python_b3\web-scraping\dados-financ-econ\novo-caged'
        
        self.options = Options()
        # options.add_argument("--headless")
        self.options.set_preference('browser.download.folderList', 2)
        self.options.set_preference('browser.download.dir', self.path_download)
        self.options.set_preference('browser.download.useDownloadDir', True)
        self.options.set_preference('browser.helperApps.neverAsk.saveToDisk', 
                                    'application/pdf,application/vnd.ms-excel,application/octet-stream')
        self.options.set_preference('pdfjs.disabled', True)
        
        # URL da página
        self.url = f'https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/novo-caged/novo-caged-{ano}/{mes}'

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
        
        # Pegando o href (link do Google Drive que está a planilha do novo Caged)
        self.link_planilha = self.soup.find('a', class_='external-link').get('href')
        print(self.link_planilha)

    def acessar_site(self):
        # Inicializando o WebDriver
        self.driver = webdriver.Firefox(options=self.options)

        # Acessando o link da planilha no Google Drive
        self.driver.get(self.link_planilha)
        sleep(3)

    def download_arquivo(self):
        # Botão de download da planilha
        download_botao = self.driver.find_element(
            By.XPATH, 
            '//*[@id=":1"]/div/c-wiz/div/c-wiz/div[1]/c-wiz/div[2]/c-wiz/div[1]/c-wiz/c-wiz/div/c-wiz/div/div[1]/div/div[6]/div/span'
        )
        download_botao.click()
        sleep(45)

    def fechar_site(self):
        self.driver.quit()


def main():
    novo_caged = NovoCaged(mes='julho', ano='2024')
    novo_caged.acessar_site()
    novo_caged.download_arquivo()
    novo_caged.fechar_site()

if __name__ == '__main__':
    main()
