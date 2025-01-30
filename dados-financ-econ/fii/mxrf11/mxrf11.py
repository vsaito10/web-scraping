import json
import requests


class MXRF11:
    def dados_mxrf(self):
        # Dados do 'meta' (Fetch/XHR -> Copy as cURL -> Entrei em um conversor de cURL e fiz a cópia)
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'pt-BR,pt;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.xpasset.com.br',
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
                'regulamento',
                'relatorios_gerenciais',
                'fatos_relevantes',
                'rendimentos_e_amortizacoes',
                'comunicados_ao_mercado',
                'relatorios-tri',
                'apresentacoes_trimestrais',
                'demonstracoes_financeiras',
                'planilha_de_fundamentos',
                'informes',
                'assembleias',
                'outros',
            ],
            'language': 'pt_BR',
            'published': True,
        }

        response = requests.post(
            'https://apicatalog.mziq.com/filemanager/company/15312117-8e09-410c-96b1-c1ba3a159171/filter/categories/year/meta',
            headers=headers,
            json=json_data,
        )

        # JSON
        self.json_mxrf = response.json()

    def download_arquivo(self):
        # Iterando sobre os itens de 'document_metas' e filtrando por 'file_origin' == 'UPLOAD'
        document_metas = self.json_mxrf['data']['document_metas']
        # Lista que contém todos as planilhas de fundamentos do site
        itens_upload = [item for item in document_metas if item.get('file_origin') == 'UPLOAD']

        # Verificando se a lista não está vazia
        if itens_upload:  
            # Selecionando o primeiro item que é a planilha mais atualizada
            primeiro_item = itens_upload[0]

            # O nome do arquivo é "Planilha de Fundamentos - Novembro/2024" selecionando toda a string após o hífen -> "Novembro/2024"
            string_nome_arquivo = primeiro_item['file_name_original']
            indice_hifen = string_nome_arquivo.find('-')
            data_arquivo = string_nome_arquivo[indice_hifen + 1:]

            # Dicionário dos meses do ano
            dict_data = {
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
                'Dezembro': '12',
            }

            # Substituindo o nome do mês pelo número
            for mes, numero in dict_data.items():
                if mes in data_arquivo:
                    data_arquivo = data_arquivo.replace(mes, numero)
                    break
            
            # Retirando o '/' da string ('11/2024' -> '112024')
            data_arquivo = data_arquivo.replace('/', '').strip()

            # URL da planhilha mais recente
            url_download = primeiro_item['file_url']
            response = requests.get(url_download)

            # Download da planilha mais recente
            if response.status_code == 200:
                with open(f'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//fii/mxrf11//mxrf11_{data_arquivo}.xlsx', 'wb') as f:
                    f.write(response.content)
                print('Arquivo baixado com sucesso.')
            else:
                print('Erro ao baixar o arquivo.')
                
        else:
            print("Nenhum item encontrado com 'file_origin' igual a 'UPLOAD'.")

def main():
    mxrf11 = MXRF11()
    mxrf11.dados_mxrf()
    mxrf11.download_arquivo()


if __name__ == "__main__":
    main()
