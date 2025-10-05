from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep


class AtasCopom:
    def __init__(self):
        # Diretório do download do arquivo 
        self.path_download = r'C:\Users\vitor\projetos_python\python_b3\historico-arquivos\minutes-pdf'

        options = Options()
        #options.add_argument("--headless")
        options.set_preference('browser.download.folderList', 2)  
        options.set_preference('browser.download.dir', self.path_download)
        options.set_preference('browser.download.useDownloadDir', True) 
        options.set_preference('browser.download.viewableInternally.enabledTypes', '')  
        options.set_preference('pdfjs.disabled', True)  
        options.set_preference('plugin.disable_full_page_plugin_for_types', 'application/pdf')  

        self.driver = webdriver.Firefox(options=options)

    def acessar_site(self, url_path):
        url = url_path
        self.driver.get(url)
        sleep(1)

        # Clicando no botão de cookie
        botao_cookie = self.driver.find_element(By.XPATH, '/html/body/app-root/bcb-cookie-bar/div/div/div[2]/button[3]').click()
        sleep(1)

        # Clicando no botão de download
        botao_download = self.driver.find_element(By.XPATH, '//*[@id="publicacao"]/div[1]/div/div/div/div[1]/div[2]/download/div/a')
        # Usando JavaScript para acionar o download diretamente
        self.driver.execute_script('arguments[0].click();', botao_download)                            
        sleep(10)            

        print('Arquivo baixado com sucesso!')
        
    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    atas = AtasCopom()
    atas.acessar_site(url_path='https://www.bcb.gov.br/en/publications/copomminutes/17092025')
    atas.fechar_site()


if __name__ == '__main__':
    main()

