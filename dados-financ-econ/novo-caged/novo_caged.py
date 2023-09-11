from bs4 import BeautifulSoup
import requests
import re
import os


class WebScrapingCaged:

    def formatando_data(self):
        url = 'http://pdet.mte.gov.br/novo-caged'
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Procurando o texto com a data de lançamento do Novo Caged
        data = soup.find('h2', class_='outstanding-title').text

        # Selecionando apenas a data com regex
        padrao = r"\w+ - (.*)"
        data_completa = re.findall(padrao, data)[0]

        # Tranformando a str 'Abril de 2023' para 'abril_2023'
        self.data_formatada = data_completa.replace(' de ', '_').lower()

        # Selecionando apenas o mês e o ano separadamente
        padrao = r'(\w+)'  # Separa a string em ['Abril', 'de', '2023']
        mes = re.findall(padrao, data_completa)[0]
        self.ano = re.findall(padrao, data_completa)[2]

        # Dicionário de correspondência entre nomes dos meses e os seus números
        meses_para_numeros = {
            'Janeiro': '01',
            'Fevereiro': '02',
            'Março': '03',
            'Abril': '04',
            'Maio': '05',
            'Junho': '06',
            'Julho': '07',
            'Agosto': '08',
            'Setembro': '09',
            'Outubro': '10',
            'Novembro': '11',
            'Dezembro': '12'
        }

        # Obter o número correspondente usando o dicionário
        self.numero_mes = meses_para_numeros[mes]

    def download_arquivo(self):
        url_download = f'http://pdet.mte.gov.br/images/Novo_CAGED/{self.ano}/{self.ano}{self.numero_mes}/3-tabelas.xlsx'
        response = requests.get(url_download)

        if response.status_code == 200:
            with open('C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//novo-caged//3-tabelas.xlsx', 'wb') as f:
                f.write(response.content)
            print("Arquivo baixado com sucesso.")
        else:
            print("Erro ao baixar o arquivo.")


def main():
    caged = WebScrapingCaged()
    caged.formatando_data()
    caged.download_arquivo()


if __name__ == "__main__":
    main()
