from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from time import sleep


"""
Faz o scraping apenas da primeira imagem (mais atualizado) do relatório da Abicom.
"""

class RelatorioAbicom:
    def __init__(self):
        options = Options()
        #options.add_argument('--headless') # Executar em modo headless (sem abrir o navegador)
        options.add_argument('--no-sandbox')  # Evitar erro de sandbox
        options.add_argument('--disable-dev-shm-usage') # Evitar erro de uso de memória
        options.add_argument('--disable-gpu')  # Desabilitar a GPU

        self.driver = webdriver.Firefox(options=options)
        self.url = 'https://abicom.com.br/categoria/ppi/'

        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }

        response = requests.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(response.content, 'html.parser')

    def acessar_site(self):
        self.driver.get(self.url)
        sleep(2)    

    def salvar_imagem(self):
        # Imagem do relatório da Abicom
        imagem = self.driver.find_element(By.XPATH, f'//*[@id="page"]/article/div/div/div/div/div/div[1]/a/img')

        # Data de quando a imagem foi publicada
        data = self.driver.find_element(By.XPATH, f'//*[@id="page"]/article/div/div/div/div/div/div[1]/a/div/h5').text
        # Selecionando apenas a data da string ('PPI - 16/10/2023' -> '16/10/2023')
        padrao = r'\d{2}/\d{2}/\d{4}'
        correspondencia = re.findall(padrao, data)
        # Transformando o formato da data de '16/10/2023' para '20231016'
        data_original = correspondencia[0]
        data_formatada = datetime.strptime(data_original, "%d/%m/%Y").strftime("%Y%m%d")

        # Tirando o screenshot da imagem 
        arquivo_imagem = f'C://Users//vitor//projetos_python//python_b3//historico-arquivos//imagem-abicom//{data_formatada}_abicom.png'
        imagem.screenshot(arquivo_imagem)

    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    abicom = RelatorioAbicom()
    abicom.acessar_site()
    abicom.salvar_imagem()
    abicom.fechar_site()


if __name__ == "__main__":
    main()