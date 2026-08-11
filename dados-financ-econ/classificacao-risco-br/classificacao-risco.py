import os
from datetime import datetime
from time import sleep
from zoneinfo import ZoneInfo

from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Fuso da B3 (horário de Brasília), usado para determinar a "data de hoje"
TZ_SAO_PAULO = ZoneInfo('America/Sao_Paulo')

class ClassificacaoRiscoBR:
    def __init__(self):
        options = Options()

        # Diretório do download do arquivo (mesma pasta deste script)
        self.path_download = os.path.dirname(os.path.abspath(__file__))

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
        # Espera explícita: o painel/botão do APEX pode demorar a carregar
        wait = WebDriverWait(self.driver, 20)

        # Localiza o botão pelo texto visível "Download" (cobre <button> e <a>).
        # Mais estável que posição (li[3]) ou ID dinâmico do APEX.
        xpath_botao = (
            "//button[contains(normalize-space(.), 'Download')]"
            " | //a[contains(normalize-space(.), 'Download')]"
        )

        # Espera o botão ficar clicável e rola até ele
        botao_download = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_botao)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_download)

        # Tenta o clique normal; se algo interceptar, cai para o clique via JS
        try:
            botao_download.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            # Algum overlay interceptou o clique -> aciona via JS
            self.driver.execute_script("arguments[0].click();", botao_download)

        sleep(5)

        # Lista apenas os arquivos de planilha baixados (evita renomear o próprio script)
        extensoes_validas = ('.xlsx', '.xls', '.csv', '.ods')
        lista_arquivos = [
            f for f in os.listdir(self.path_download)
            if f.lower().endswith(extensoes_validas)
        ]

        if not lista_arquivos:
            raise FileNotFoundError(
                f'Nenhum arquivo de planilha foi baixado em {self.path_download}. '
                'O download pode ter falhado.'
            )

        # Obtendo o nome do último arquivo baixado no diretório de download
        lista_arquivos.sort(key=lambda x: os.path.getmtime(os.path.join(self.path_download, x)))
        nome_original = os.path.join(self.path_download, lista_arquivos[-1])

        # Obtendo a data em que foi feito o download e formantando a data
        data_hoje = datetime.now(tz=TZ_SAO_PAULO).date()
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