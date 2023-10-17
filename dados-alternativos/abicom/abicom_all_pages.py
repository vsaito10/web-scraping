from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from time import sleep


"""
Faz o scraping de todas as imagens de todas as páginas do relatório da Abicom.
"""

class RelatorioAbicom:
    def __init__(self):
        options = Options()
        #options.add_argument('--headless') # Executar em modo headless (sem abrir o navegador)
        options.add_argument('--no-sandbox')  # Evitar erro de sandbox
        options.add_argument('--disable-dev-shm-usage') # Evitar erro de uso de memória
        options.add_argument('--disable-gpu')  # Desabilitar a GPU

        self.driver = webdriver.Firefox(options=options)
        self.url = 'https://abicom.com.br/categoria/ppi/'

        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }

        response = requests.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(response.content, 'html.parser')

    def acessar_site(self):
        self.driver.get(self.url)
        sleep(2)    

    def salvar_imagem(self):
        while True:            
            try:
                # Descobrindo quantas imagens tem na página p/ fazer a iteração
                num_images = self.soup.find_all('img', {'class':'card-img-top'})

                # Lista das imagens e das datas de publicações
                lst_imagem = []
                lst_data = []
                # A primeira imagem do site sempre começa em 1 e o nº máximo são de 9 imagens em uma página
                # Apenas a última página tem menos de 9 imagens, senão eu poderia ter feito um loop for fixo com 'range(1, 10)'  
                for i in range(1, len(num_images)+1):
                    # Imagem do relatório da Abicom
                    imagem = self.driver.find_element(By.XPATH, f'//*[@id="page"]/article/div/div/div/div/div/div[{i}]/a/img')
                    lst_imagem.append(imagem)

                    # Data de quando a imagem foi publicada
                    data = self.driver.find_element(By.XPATH, f'//*[@id="page"]/article/div/div/div/div/div/div[{i}]/a/div/h5').text
                    # Selecionando apenas a data da string ('PPI - 16/10/2023' -> '16/10/2023')
                    padrao = r'\d{2}/\d{2}/\d{4}'
                    correspondencia = re.findall(padrao, data)
                    # Transformando o formato da data de '16/10/2023' para '20231016'
                    data_original = correspondencia[0]
                    data_formatada = datetime.strptime(data_original, "%d/%m/%Y").strftime("%Y%m%d")
                    lst_data.append(data_formatada)

                # Iterando sobre a 'lst_imagem' para tirar o screenshot das imagens dessa lista
                for i, imagem in enumerate(lst_imagem):
                    arquivo_imagem = f'C://Users//vitor//projetos_python//python_b3//historico-arquivos//imagem-abicom//{lst_data[i]}_abicom.png'
                    imagem.screenshot(arquivo_imagem)

                # Botão 'próxima página'
                botao_prox_pag = self.driver.find_element(By.CSS_SELECTOR, 'a.next.page-numbers')
                if botao_prox_pag:
                    botao_prox_pag.click()
                    sleep(5)

                    # Atualizando a instância BeautifulSoup para a nova página 
                    response = requests.get(self.url, headers=self.headers)
                    self.soup = BeautifulSoup(response.content, 'html.parser')

            except:
                break

    def fechar_site(self):
        # Fechando o driver
        self.driver.quit()


def main():
    abicom = RelatorioAbicom()
    abicom.acessar_site()
    abicom.salvar_imagem()
    abicom.fechar_site()


if __name__ == "__main__":
    main()