from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
import os


class ClassificacaoRiscoBR:
    def __init__(self):
        options = Options()

        # Diretório do download do arquivo 
        self.path_download = r'C:\Users\vitor\projetos_python\python_b3\web-scraping\dados-financ-econ\classificacao-risco-br'

        options = Options()
        #options.add_argument("--headless")
        options.set_preference("browser.download.folderList", 2)  
        options.set_preference("browser.download.dir", self.path_download)
        options.set_preference("browser.download.useDownloadDir", True) 
        options.set_preference("browser.download.viewableInternally.enabledTypes", "")  
        options.set_preference("pdfjs.disabled", True)  
        options.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")  

        self.driver = webdriver.Firefox(options=options)

    def acessar_site(self):
        self.driver.get('https://sisweb.tesouro.gov.br/apex/f?p=2810:2:0:&minimal=full&font=opensans')
        sleep(1)

    def download_arquivo(self):
        # Download do arquivo excel
        botao_download = self.driver.find_element(By.XPATH, '//*[@id="B203132468640086541"]').click()
        sleep(5)

        # Lista os arquivos dentro do diretório de download
        lista_arquivos = os.listdir(self.path_download)

        # Obtendo o nome do último arquivo baixado no diretório de download
        lista_arquivos.sort(key=lambda x: os.path.getmtime(os.path.join(self.path_download, x)))
        nome_original = os.path.join(self.path_download, lista_arquivos[-1])

        # Obtendo a data em que foi feito o download e formantando a data
        data_hoje = datetime.now().date()
        data_formatada = data_hoje.strftime("%Y%m%d")

        # Novo nome do arquivo
        novo_nome = os.path.join(self.path_download, f'classificacao_risco_br_{data_formatada}.csv')

        # Renomeando o arquivo
        os.rename(nome_original, novo_nome)

    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    classificacao_risco = ClassificacaoRiscoBR()
    classificacao_risco.acessar_site()     
    classificacao_risco.download_arquivo()
    classificacao_risco.fechar_site()

if __name__ == "__main__":
    main()