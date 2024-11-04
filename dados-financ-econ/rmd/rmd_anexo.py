from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep


class AnexoRmd:
    def __init__(self):
        # Diretório do download do arquivo 
        self.path_download = r"C:\Users\vitor\projetos_python\python_b3\web-scraping\dados-financ-econ\rmd"

        options = Options()
        #options.add_argument("--headless")
        options.set_preference("browser.download.folderList", 2)  
        options.set_preference("browser.download.dir", self.path_download)
        options.set_preference("browser.download.useDownloadDir", True) 
        options.set_preference("browser.download.viewableInternally.enabledTypes", "")  
        options.set_preference("pdfjs.disabled", True)  
        options.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")  

        self.driver = webdriver.Firefox(options=options)

    def acessar_site(self, ano, mes):
        self.driver.get(f'https://www.tesourotransparente.gov.br/publicacoes/relatorio-mensal-da-divida-rmd/{ano}/{mes}')
        sleep(2)

    def download_planhilha(self):
        # Clicando nos botões de cookies e download
        botao_cookie = self.driver.find_element(By.XPATH, '//*[@id="lgpd-cookie-banner-janela"]/div[2]/button[2]')
        botao_cookie.click()

        botao_planilha = self.driver.find_element(By.XPATH, '//*[@id="publicacao"]/div/div[2]/section/ul/li[1]/a[1]')
        botao_planilha.click()
        sleep(5)

    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    anexo_rmd = AnexoRmd()
    anexo_rmd.acessar_site(ano='2024', mes='8')     # Os meses de 1 (Jan) a 9 (Set) não precisa colocar o '0' na frente
    anexo_rmd.download_planhilha()     
    anexo_rmd.fechar_site()


if __name__ == "__main__":
    main()
