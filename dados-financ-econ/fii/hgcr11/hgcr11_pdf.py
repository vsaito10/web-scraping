import fitz  
import requests


class HGCR11:
    def dados_hgcr(self):
        # Dados do 'meta' (Fetch/XHR -> Copy as cURL -> Entrei em um conversor de cURL e fiz a cópia)
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'pt-BR,pt;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://realestate.patria.com',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        json_data = {
            'year': '2024',
            'categories': [
                'hgcr_cshg_recebiveis_imobiliarios_fii_relatorios_ao_investidor',
                'hgcr_cshg_recebiveis_imobiliarios_fii_apresentacoes',
                'hgcr_cshg_recebiveis_imobiliarios_fii_informe_contabil_mensal',
                'hgcr_cshg_recebiveis_imobiliarios_fii_informe_trimestral',
                'hgcr_cshg_recebiveis_imobiliarios_fii_informe_anual',
                'hgcr_cshg_recebiveis_imobiliarios_fii_demonstracoes_financeiras',
            ],
            'language': 'pt_BR',
            'published': True,
        }

        response = requests.post(
            'https://apicatalog.mziq.com/filemanager/company/8700340f-de5f-46d7-bbc7-83b2105cdd34/filter/categories/year/meta',
            headers=headers,
            json=json_data,
        )

        # JSON
        self.json_hgcr = response.json()

    def download_pdf(self):
        # URL do pdf mais recente - sempre é o primeiro
        url_download =  self.json_hgcr['data']['document_metas'][0]['file_url']
        response = requests.get(url_download)

        # Selecionando a data do último pdf -> '2024-12-31'
        self.data_arquivo = self.json_hgcr['data']['document_metas'][0]['file_date'][0:10]

        # Caminho do arquivo pdf
        self.path_pdf = f'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//fii/hgcr11//hgcr11_{self.data_arquivo}.pdf'

        # Download do arquivo pdf
        if response.status_code == 200:
            with open(self.path_pdf, 'wb') as f:
                f.write(response.content)
            print('Arquivo PDF baixado com sucesso.')
        else:
            print('Erro ao baixar o arquivo PDF.')
    
    def download_planilha(self):
        doc = fitz.open(self.path_pdf)
        links = []

        for page in doc:
            for link in page.get_links():
                if 'uri' in link:
                    links.append(link['uri'])
        
        # Dentro do pdf possui várias URLs
        # Filtrando a URL que contêm a string 'mziq' -> ex: 'https://api.mziq.com/mzfilemanager/v2/d/8700340f-de5f-46d7-bbc7-83b2105cdd34/95a59e26-70b1-d5a5-cee7-b1f74278759f?origin=2'
        url_planilha = [url for url in links if 'mziq' in url][0]
        response = requests.get(url_planilha)
        
        # Caminho do arquivo pdf
        self.path_planilha = f'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//fii/hgcr11//hgcr11_{self.data_arquivo}.xlsx'

        # Download da planilha
        if response.status_code == 200:
            with open(self.path_planilha, 'wb') as f:
                f.write(response.content)
            print('Planilha baixada com sucesso.')
        else:
            print('Erro ao baixar a planilha.')

def main():
    hgcr11 = HGCR11()
    hgcr11.dados_hgcr()
    hgcr11.download_pdf()
    hgcr11.download_planilha()


if __name__ == "__main__":
    main()