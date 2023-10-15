from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class PesquisaPeic:
    def __init__(self):
        # Diretório do download do arquivo 
        self.path_download = r"C:\Users\vitor\projetos_python\python_b3\web-scraping\dados-financ-econ\endividamento_br"

        options = Options()
        options.set_preference("browser.download.folderList", 2)  
        options.set_preference("browser.download.dir", self.path_download)
        options.set_preference("browser.download.useDownloadDir", True) 
        options.set_preference("browser.download.viewableInternally.enabledTypes", "")  
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

    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    peic = PesquisaPeic()
    peic.acessar_site()
    peic.botao_downlaod()
    peic.fechar_site()


if __name__ == "__main__":
    main()