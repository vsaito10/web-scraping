from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep


class YieldCurveFedNy:

    def __init__(self):
        # Diretório do download do arquivo 
        self.path_download = r"C:\Users\vitor\projetos_python\python_b3\web-scraping\dados-financ-econ\yield-curve-leading-indicator"

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
        self.driver.get('https://www.newyorkfed.org/research/capital_markets/ycfaq#/interactive')
        sleep(2)

    def download_planhilha(self):
        # Clicando nos botões de download
        botao = self.driver.find_element(By.XPATH, '//*[@id="archiveButton"]')
        botao.click()

        botao_download = self.driver.find_element(By.XPATH, '//*[@id="dropDownMenue"]/span[2]/a')
        botao_download.click()
        sleep(5)

    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    contratos_aberto = YieldCurveFedNy()
    contratos_aberto.acessar_site()     
    contratos_aberto.download_planhilha()     
    contratos_aberto.fechar_site()


if __name__ == "__main__":
    main()
