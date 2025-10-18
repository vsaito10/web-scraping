import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import Optional


class WebScrapingProjecoesIFI:
    def __init__(self):
        # URL
        self.url = 'https://www12.senado.leg.br/ifi'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'close'
        }

        # Mapeando de meses para número
        self.map_meses = {
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

    def _parse_number(self, text: str) -> Optional[float]:
        """Tratando os números da tabela do site do IFI"""
        if text is None:
            return None
        s = str(text).strip()
        # Removendo espaços estranhos
        s = s.replace('\xa0', '').replace('\u200b', '').strip()
        # Permitindo sinais negativos com espaços (ex: ' -87,4' ou '- 87,4')
        s = s.replace('- ', '-').replace(' -', '-')
        # Removendo 'R$' e '%' 
        s = s.replace('R$', '').replace('%', '').strip()
        if s == '':
            return None
        # Quando houver vírgula decimal, removendo pontos de milhares
        if '.' in s and ',' in s:
            s = s.replace('.', '').replace(',', '.')
        else:
            # Se só tiver vírgula, trocando por ponto
            if ',' in s and '.' not in s:
                s = s.replace(',', '.')
            else:
                # Se só tiver pontos e não houver parte decimal curta, removendo pontos (milhares)
                if s.count('.') > 1:
                    s = s.replace('.', '')
                else:
                    # Se houver um ponto e parece decimal (1-3 casas), assumindo decimal
                    if s.count('.') == 1 and re.search(r'\.\d{1,3}$', s):
                        pass
                    else:
                        # Caso ambíguo: removendo pontos
                        s = s.replace('.', '')
        # Limpando possíveis caracteres não numéricos finais
        s = re.sub(r'[^\d\.\-]', '', s)
        try:
            return float(s)
        except Exception:
            return None

    def web_scraping_data(self):
        # Fazendo a requisição HTTP para obter o conteúdo da página
        resp = requests.get(self.url, headers=self.headers, timeout=15)

        # Criando o objeto BeautifulSoup para analisar o conteúdo HTML da página
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Data que tabela foi lançada
        tag = soup.find('h4', class_='ifi-raf')
        texto = tag.get_text(strip=True)
        m = re.search(r'\(([^)]+)\)', texto)  # Exemplo: 'RAF 104 (Setembro de 2025)'
        conteudo = m.group(1)
        partes = conteudo.split(' de ')
        mes_nome, ano = partes
        mes_num = self.map_meses.get(mes_nome.strip(), None)

        # Tabela
        cards = soup.select('div.box')
        rows = []

        # regex para capturar padrões como "2025: 12.671,5" mesmo dentro de tags <strong>
        pattern = re.compile(r'(20\d{2})\s*:\s*([-]?\s*[\d\.,]+)', flags=re.IGNORECASE)

        for card in cards:
            # extrair título e subtítulo (se existirem)
            h4 = card.find('h4')
            title = h4.get_text(strip=True) if h4 else None

            # subtítulo: pegar <p> com style ou o primeiro <p> com texto que não seja get-text vazio
            subtitle = None
            p_style = card.find('p', attrs={'style': True})
            if p_style and p_style.get_text(strip=True):
                subtitle = p_style.get_text(strip=True)

            # procurar todas as ocorrências de "YYYY: valor" dentro do HTML do card
            card_html = str(card)
            matches = pattern.findall(card_html)

            if matches:
                for year_str, val_str in matches:
                    # val_str pode conter espaços: normalizar antes de parsear
                    val_clean = val_str.replace(' ', '')
                    value = self._parse_number(val_clean)
                    rows.append({
                        'indicador': title,
                        'subtitulo': subtitle,
                        'ano': int(year_str),
                        'valor': value
                    })
            else:
                # fallback: procurar no texto plano do card por "20xx" e algum número próximo (heurística)
                text = card.get_text(' ', strip=True)
                # tentar encontrar "2025" e o primeiro número depois dela
                alt_matches = re.findall(r'(20\d{2}).{0,15}?([-]?\s*[\d\.,]+)', text)
                if alt_matches:
                    for year_str, val_str in alt_matches:
                        val_clean = val_str.replace(' ', '')
                        value = self._parse_number(val_clean)
                        rows.append({
                            'indicador': title,
                            'subtitulo': subtitle,
                            'ano': int(year_str),
                            'valor': value
                        })

        # Transformando em um df
        df = pd.DataFrame(rows)

        # Tabela pivot para colunas por ano
        pivot = df.pivot_table(index=['indicador', 'subtitulo'], columns='ano', values='valor', aggfunc='first').reset_index()
        pivot.columns.name = None
        # renomear colunas de anos para 'YYYY'
        new_cols = []
        for c in pivot.columns:
            if isinstance(c, int) or (isinstance(c, str) and c.isdigit()):
                new_cols.append(f"{int(c)}")
            else:
                new_cols.append(c)
        pivot.columns = new_cols

        # Transformando em arquivo csv
        filename = f'C://Users//vitor//projetos_python//python_b3//web-scraping//dados-financ-econ//projecoes-ifi//projecoes_IFI_{mes_num}{ano}.csv'
        pivot.to_csv(filename, index=False, encoding='utf-8-sig')


def main():
    ifi = WebScrapingProjecoesIFI()
    ifi.web_scraping_data()
    

if __name__ == "__main__":
    main()