import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class WebScrapingCapitalSocial:
    def __init__(self):
        options = Options()
        # options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

        # Lista para armazenar todos os dados
        self.all_data = []  

    def acessar_site(self):
        self.driver.get('https://sistemaswebb3-listados.b3.com.br/shareCapitalPage/?language=pt-br')
        sleep(5) 

    def scraping_tabela(self):
        while True:
            try:
                # Esperar a tabela ser visível, melhor que sleep fixo
                wait = WebDriverWait(self.driver, 10)
                tabela = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="shareCapitalTable"]')))
                corpo_tabela = tabela.find_element(By.TAG_NAME, 'tbody')
                linhas = corpo_tabela.find_elements(By.TAG_NAME, 'tr')
                
                for linha in linhas:
                    celulas = linha.find_elements(By.TAG_NAME, 'td')
                    dados_linha = {
                        'Nome Do Pregão': celulas[0].text.strip(),
                        'Código': celulas[1].text.strip(),
                        'Denominação Social': celulas[2].text.strip(),
                        'Segmento De Mercado': celulas[3].text.strip(),
                        'Tipo De Capital': celulas[4].text.strip(),
                        'Capital R$': celulas[5].text.strip(),
                        'Aprovado Em': celulas[6].text.strip(),
                        'Qtde Ações Ordinárias': celulas[7].text.strip(),
                        'Qtde Ações Preferenciais': celulas[8].text.strip(),
                        'Qtde Total De Ações': celulas[9].text.strip(),
                    }
                    self.all_data.append(dados_linha)
                
                # Tenta encontrar e clicar no botão de próxima página
                next_button = self.driver.find_element(By.XPATH, '//*[@id="paginator_btn_nextPage"]')
                
                # Verifica se o botão está habilitado
                if 'disabled' in next_button.get_attribute('class'):
                    print('Última página alcançada. Coleta de dados completa.')
                    break  # Sai do loop se o botão estiver desabilitado
                
                next_button.click()
                sleep(3) # Espera a próxima página carregar

            except Exception as e:
                print(f'Ocorreu um erro ou a última página foi alcançada: {e}')
                break # Sai do loop em caso de erro (provavelmente o botão não foi encontrado)

    def salvar_dados(self):
        if self.all_data:
            df = pd.DataFrame(self.all_data)
            df.to_csv(
                'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//capital-social-b3//capital_social.csv',
                sep=';',
                index=False
            )
            print('Dados salvos com sucesso!')
        else:
            print('Nenhum dado para salvar.')

    def fechar_site(self):
        self.driver.quit()


def main():
    capital_social = WebScrapingCapitalSocial()
    capital_social.acessar_site()
    capital_social.scraping_tabela()
    capital_social.salvar_dados()
    capital_social.fechar_site()


if __name__ == "__main__":
    main()