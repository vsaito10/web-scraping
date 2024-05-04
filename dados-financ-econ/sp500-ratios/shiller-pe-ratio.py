from bs4 import BeautifulSoup
import os
import requests


class ShillerPE:
    def __init__(self):
        # Diretório do download do arquivo
        self.download_directory = 'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//sp500-ratios//'

        # URL
        self.url = 'https://shillerdata.com/'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'close'
        }

        # Fazendo a requisição HTTP para obter o conteúdo da página
        response = requests.get(self.url, headers=self.headers)

        # Criando o objeto BeautifulSoup para analisar o conteúdo HTML da página
        self.soup = BeautifulSoup(response.content, 'html.parser')

    def download_planilha(self):
        # Tabela 
        planilha = self.soup.find_all('div', class_='x-el x-el-div c1-1 c1-2 c1-1k c1-1t c1-1u c1-54 c1-1e c1-1w c1-1x c1-55 c1-1z c1-b c1-c c1-22 c1-23 c1-56 c1-25 c1-d c1-57 c1-58 c1-e c1-f c1-g')
        
        # Lista para guardar os hrefs
        href_links = [] 
        for item in planilha:
            for link in item.find_all('a'):
                href = link.get('href')
                href_links.append(href)

        # O 'href_links' vai conter dois links - o link da planilha é o segundo
        # String do href -> '//img1.wsimg.com/blobby/go/e5e77e0b-59d1-44d9-ab25-4763ac982e53/downloads/ie_data.xls?ver=1714742730434'
        link_planilha = href_links[1]
        link_planilha = 'https:' + href_links[1]

        # Descobrindo a posição da string '?'
        posicao_interrogacao = link_planilha.find('?')

        # Filtrando a string do link de download da planilha -> 'https://img1.wsimg.com/blobby/go/e5e77e0b-59d1-44d9-ab25-4763ac982e53/downloads/ie_data.xls'
        link_planilha_final = link_planilha[:posicao_interrogacao]

        # Requisição para o link de download da planilha
        response = requests.get(link_planilha_final, headers=self.headers)

        # Fazendo o download do arquivo
        if response.status_code == 200:
            # Nome do arquivo
            nome_arquivo = os.path.basename(link_planilha_final)
            
            # Caminho completo do arquivo 
            novo_caminho = os.path.join(self.download_directory, nome_arquivo)

            with open(novo_caminho, 'wb') as f:
                f.write(response.content)

            # Renomeando o arquivo para 'shiiler-pe.xls'
            novo_nome_arquivo = os.path.join(self.download_directory, 'shiller_pe.xls')
            os.rename(novo_caminho, novo_nome_arquivo)


def main():
    shiller_pe = ShillerPE()
    shiller_pe.download_planilha()


if __name__ == "__main__":
    main()