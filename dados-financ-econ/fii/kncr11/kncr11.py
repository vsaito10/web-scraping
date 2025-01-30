from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
import os


class KNCR11:
    def __init__(self):
        options = Options()

        # Diretório do download do arquivo 
        self.path_download = r'C:\Users\vitor\projetos_python\python_b3\web-scraping\dados-financ-econ\fii\kncr11'

        options = Options()
        #options.add_argument('--headless')
        options.set_preference('browser.download.folderList', 2)  
        options.set_preference('browser.download.dir', self.path_download)
        options.set_preference('browser.download.useDownloadDir', True) 
        options.set_preference('browser.download.viewableInternally.enabledTypes', '')  
        options.set_preference('pdfjs.disabled', True)  
        options.set_preference('plugin.disable_full_page_plugin_for_types', 'application/pdf')  

        self.driver = webdriver.Firefox(options=options)

    def acessar_site(self):
        self.driver.get('https://www.kinea.com.br/fundos/fundo-imobiliario-kinea-rendimentos-kncr11/')
        sleep(1)

    def download_arquivo(self):
        # Botão do cookie
        botao_cookie = self.driver.find_element(By.XPATH, '//*[@id="modal-comunicado"]/div/div[2]').click()
        sleep(1)

        # Download do arquivo excel
        botao_download = self.driver.find_element(By.XPATH, '//*[@id="Documentos"]/div/div/div/div[2]/div/div/div/table/tbody/tr[6]/td[3]/div').click()
        sleep(5)

        # Data do arquivo
        data_arquivo = self.driver.find_element(By.XPATH, '//*[@id="Documentos"]/div/div/div/div[2]/div/div/div/table/tbody/tr[6]/td[2]').text

        # Formatando a data do arquivo de '11/2024' para '112024'
        data_arquivo = data_arquivo.replace('/', '')
        print(data_arquivo)

        # Lista os arquivos dentro do diretório de download
        lista_arquivos = os.listdir(self.path_download)

        # Obtendo o nome do último arquivo baixado no diretório de download
        lista_arquivos.sort(key=lambda x: os.path.getmtime(os.path.join(self.path_download, x)))
        nome_original = os.path.join(self.path_download, lista_arquivos[-1])

        # Novo nome do arquivo
        novo_nome = os.path.join(self.path_download, f'kncr11_{data_arquivo}.xlsx')

        # Renomeando o arquivo
        os.rename(nome_original, novo_nome)

    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    kncr11 = KNCR11()
    kncr11.acessar_site()     
    kncr11.download_arquivo()
    kncr11.fechar_site()

if __name__ == "__main__":
    main()