from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import glob
import re


class PesquisaPeic:
    def __init__(self):
        # Diretório do download do arquivo 
        self.path_download = r'C:\Users\vitor\projetos_python\python_b3\web-scraping\dados-financ-econ\endividamento-brasil'

        options = Options()
        options.set_preference('browser.download.folderList', 2)  
        options.set_preference('browser.download.dir', self.path_download)
        options.set_preference('browser.download.useDownloadDir', True) 
        options.set_preference('browser.download.viewableInternally.enabledTypes', '')  
        self.driver = webdriver.Firefox(options=options)

    def acessar_site(self):
        url = 'https://www.fecomercio.com.br/pesquisas/indice/peic'
        self.driver.get(url)
        sleep(1)

    def botao_downlaod(self):
        botao = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/div[1]/div[1]/div[5]/a')
        ))
        botao.click()

    def renomear_arquivo(self):
        # Selecionando apenas o arquivo excel
        padrao = '*.xlsx'
        nome_arquivos = glob.glob(os.path.join(self.path_download, padrao))

        # Renomeando o arquivo do formato "peic_link_download_202309.xlsx" para "peic_202309.xlsx"
        if nome_arquivos:
            nome_arquivo = os.path.basename(nome_arquivos[0])
            novo_nome = re.sub(r'peic_link_download_', 'peic_', nome_arquivo)
            novo_caminho = os.path.join(self.path_download, novo_nome)
            os.rename(nome_arquivos[0], novo_caminho)
            
        else:
            print('Nenhum arquivo .xlsx encontrado na pasta.')

    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    peic = PesquisaPeic()
    peic.acessar_site()
    peic.botao_downlaod()
    peic.renomear_arquivo()
    peic.fechar_site()


if __name__ == "__main__":
    main()