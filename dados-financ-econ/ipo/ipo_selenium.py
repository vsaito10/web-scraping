from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
import os


class IpoB3:
    def __init__(self):
        options = Options()

        # Diretório do download do arquivo 
        self.path_download = 'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//ipo'

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
        self.driver.get('https://www.b3.com.br/pt_br/produtos-e-servicos/solucoes-para-emissores/ofertas-publicas/estatisticas/')
        sleep(1)

        # Clicando no botão de cookie
        botao_cookie = self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
        sleep(1)

    def download_arquivo(self):

        # Download do arquivo excel
        botao_ano = self.driver.find_element(By.XPATH, '//*[@id="conteudo-principal"]/div[4]/div/div/div/div[1]/div[2]/p/a[2]').click()
        sleep(5)

        # Lista os arquivos dentro do diretório de download
        lista_arquivos = os.listdir(self.path_download)

        # Obtendo o nome do último arquivo baixado no diretório de download
        lista_arquivos.sort(key=lambda x: os.path.getmtime(os.path.join(self.path_download, x)))
        nome_original = os.path.join(self.path_download, lista_arquivos[-1])

        # Novo nome do arquivo
        novo_nome = os.path.join(self.path_download, 'lista_ipo.xlsx')

        # Renomeando o arquivo
        os.rename(nome_original, novo_nome)

    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    ipo = IpoB3()
    ipo.acessar_site()     
    ipo.download_arquivo()
    ipo.fechar_site()

if __name__ == "__main__":
    main()
