import pandas as pd
import requests


headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'pt-BR,pt;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://www.nfib-sbet.org',
    'Referer': 'http://www.nfib-sbet.org/',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'X-DreamFactory-Application-Name': 'sbet',
}

data = {
    'app_name': 'sbet',
    'params[0][name]': 'minYear',
    'params[0][param_type]': 'IN',
    'params[0][value]': '1986',
    'params[1][name]': 'minMonth',
    'params[1][param_type]': 'IN',
    'params[1][value]': '1',
    'params[2][name]': 'maxYear',
    'params[2][param_type]': 'IN',
    'params[2][value]': '2024',
    'params[3][name]': 'maxMonth',
    'params[3][param_type]': 'IN',
    'params[3][value]': '12',
    'params[4][name]': 'indicator',
    'params[4][param_type]': 'IN',
    'params[4][value]': 'OPT_INDEX',
}

response = requests.post(
    'http://open.api.nfib-sbet.org/rest/sbetdb/_proc/getIndicators2',
    headers=headers,
    data=data,
    verify=False,
)

# Transformando em JSON 
nfib = response.json()

# Convertendo a lista em um DataFrame
df_nfib = pd.DataFrame(nfib)

# Substituindo o '/' por '-'
df_nfib['monthyear'] = df_nfib['monthyear'].str.replace('/', '-')

# Transformando a coluna 'monthyear' em datetime
df_nfib['monthyear'] = pd.to_datetime(df_nfib['monthyear'], format='%Y-%m-%d')

# Data do último lançamento
ultima_data = df_nfib['monthyear'].iloc[0].strftime('%Y-%m-%d').replace('-', '_')

# Transformando em um arquivo excel
df_nfib.to_excel(f'C://Users/vitor/projetos_python/python_b3/web-scraping/dados-financ-econ/nfib/nfib_{ultima_data}.xlsx', index=False)