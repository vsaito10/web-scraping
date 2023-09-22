from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import os
import re
import requests
import glob


class AtasCopom:
    def __init__(self):
        options = Options()
        self.path_download = r"C:\Users\vitor\projetos_python\python_b3\historico-arquivos\minutes-pdf"
        #options.add_argument("--headless")
        options.add_argument("--incognito")
        options.set_preference("browser.download.folderList", 2)  # Personalizado
        options.set_preference("browser.download.dir", self.path_download)
        options.set_preference("browser.download.useDownloadDir", True)  # Usar o diretório de download especificado
        options.set_preference("browser.download.viewableInternally.enabledTypes", "")  # Evitar que o Firefox visualize o arquivo
        options.set_preference("pdfjs.disabled", True)  # Desativar visualização interna de PDF
        options.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")  # Desativar visualização interna de PDF

        self.driver = webdriver.Firefox(options=options)

    def download_arquivo(self, num_ata_inicial, num_ata_final):
        # Url p/ extrair as datas de publicações p/ criar as urls de cada ata p/ download dos pdfs
        url = "https://www.bcb.gov.br/api/servico/sitebcb/copomminutes/ultimas"

        querystring = {"quantidade":"1000","filtro":""}
        payload = ""
        headers = {"sec-ch-ua": "^\^Chromium^^;v=^\^116^^, ^\^Not"}

        r = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        data = r.json()

        # Número da ata inicial
        n_ata_inicial = num_ata_inicial
        # Número da ata final
        n_ata_final = num_ata_final

        # Lista com as datas de publicações de todas as atas
        lst_data_pub = []
        for i in range(n_ata_final - n_ata_inicial + 1):
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
            sleep(1)

            while True:
                try:
                    # Clicando no botão de cookie
                    botao_cookie = self.driver.find_element(By.XPATH, '/html/body/app-root/bcb-cookies/div/div/div/div/button[2]')
                    botao_cookie.click()
                    sleep(2)
                except:
                    pass

                try:
                    # Clicando no botão de download
                    botao_download = self.driver.find_element(By.XPATH, '//*[@id="publicacao"]/div[1]/div/div/div/div[1]/div[2]/download/div/div/a')
                    # Usando JavaScript para acionar o download diretamente
                    self.driver.execute_script("arguments[0].click();", botao_download)                            
                    sleep(5)    
                    break  
                except:
                    pass

    def renomear_arquivos(self):
        # Listando todos os arquivos na pasta de download
        arquivos = glob.glob(os.path.join(self.path_download, '*.pdf'))

        # Colocando os nomes dos arquivos em letras minúsculas e trocando o espaço em branco por underline
        for arquivo in arquivos:
            novo_nome_arquivo = os.path.basename(arquivo).replace(' ', '_').lower()
            caminho_novo = os.path.join(self.path_download, novo_nome_arquivo)
            os.rename(arquivo, caminho_novo)

        print("Arquivos renomeados com sucesso.")

    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    atas = AtasCopom()
    atas.download_arquivo(num_ata_inicial=220, num_ata_final=231)
    atas.renomear_arquivos()
    atas.fechar_site()


if __name__ == "__main__":
    main()
