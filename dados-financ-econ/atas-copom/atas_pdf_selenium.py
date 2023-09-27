from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import os
import re
import requests


class AtasCopom:
    def __init__(self):

        # Diretório do download do arquivo 
        self.path_download = r"C:\Users\vitor\projetos_python\python_b3\historico-arquivos\minutes-pdf"

        options = Options()
        #options.add_argument("--headless")
        options.set_preference("browser.download.folderList", 2)  
        options.set_preference("browser.download.dir", self.path_download)
        options.set_preference("browser.download.useDownloadDir", True) 
        options.set_preference("browser.download.viewableInternally.enabledTypes", "")  
        options.set_preference("pdfjs.disabled", True)  
        options.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")  

        self.driver = webdriver.Firefox(options=options)

    def download_arquivo(self, pos_ata_inicial: int, pos_ata_final: int):
        """
        Download do arquivo PDF da ata do COPOM.
        Primeiro, extraio as datas de publições das atas para montar as URLs de cada ata específica.
        Para fazer o download de múltiplos PDFs, eu tenho que iterar sobre um range entre as posições das atas.
                
        Parameters:
        'pos_ata_inicial' (int): posição da ata na lista das publicações das datas ('lst_data_pub').
        'pos_ata_final' (int): posição da ata na lista das publicações das datas ('lst_data_pub').

        NOTE: 
        - Olhar o Jupyter notebook 'atas_pdf_selenium_apoio' para saber qual é a posição específica de uma ata;
        - EXCEÇÕES AO PADRÃO DA URL -> 'https://www.bcb.gov.br/en/publications/copomminutes/{data_pub}': 
            - A ata 223 possui um padrão diferente de URL -> 'https://www.bcb.gov.br/en/publications/copomminutes/minutes223'. 

        """

        # Url p/ extrair as datas de publicações que serão usadas para criar as urls de cada ata
        url = "https://www.bcb.gov.br/api/servico/sitebcb/copomminutes/ultimas"

        querystring = {"quantidade":"1000","filtro":""}
        payload = ""
        headers = {"sec-ch-ua": "^\^Chromium^^;v=^\^116^^, ^\^Not"}

        r = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        data = r.json()

        # Posição da ata inicial
        posicao_ata_inicial = pos_ata_inicial
        # Posição da ata final
        posicao_ata_final = pos_ata_final

        # Lista com as datas de publicações de todas as atas
        lst_data_pub = []
        for i in range(pos_ata_inicial, pos_ata_final+1):
            data_pub = data['conteudo'][i]['DataReferencia']
            lst_data_pub.append(data_pub)

        # Usando regex para encontrar todas as datas no formato 'yyyy-mm-dd' na lista
        padrao_data = r'\d{4}-\d{2}-\d{2}'
        lst_data_pub = re.findall(padrao_data, ' '.join(lst_data_pub))
        # Removendo os traços '-' de cada data
        lst_data_pub = [data.replace('-', '') for data in lst_data_pub]
        # Revertendo a ordem das datas para 'ddmmyyyy'
        lst_data_pub = [data[6:] + data[4:6] + data[:4] for data in lst_data_pub]

        # Criando a lista que contém as urls
        lst_url = []
        for date_minute in lst_data_pub:
            url = f'https://www.bcb.gov.br/en/publications/copomminutes/{date_minute}'
            lst_url.append(url)

        # Iterando sobre as urls para fazer o download dos pdfs
        for url in lst_url:
            self.driver.get(url)
            self.driver.implicitly_wait(2)
            sleep(1)

            while True:
                try:
                    # Clicando no botão de cookie
                    botao_cookie = self.driver.find_element(By.XPATH, '/html/body/app-root/bcb-cookies/div/div/div/div/button[2]')
                    botao_cookie.click()
                    sleep(1)
                except:
                    pass

                try:
                    # Clicando no botão de download
                    botao_download = self.driver.find_element(By.XPATH, '//*[@id="publicacao"]/div[1]/div/div/div/div[1]/div[2]/download/div/div/a')
                    # Usando JavaScript para acionar o download diretamente
                    self.driver.execute_script("arguments[0].click();", botao_download)                            
                    sleep(10)    

                    break  
                except:
                    pass

    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    atas = AtasCopom()
    atas.download_arquivo(pos_ata_inicial=46, pos_ata_final=57)
    atas.fechar_site()


if __name__ == "__main__":
    main()

