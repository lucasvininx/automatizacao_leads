import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random
import re

# Configurações de proxies
proxies = [
    'http://proxy_ip1:proxy_port1',
    'http://proxy_ip2:proxy_port2',
    # Adicione mais proxies se tiver
]

# Função para alternar proxies
def get_random_proxy():
    return random.choice(proxies)

# Função para configurar o Selenium
def configurar_selenium(proxy=None):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")

    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    service = Service('C:\\Users\\teste\\Desktop\\chromedriver-win64\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

# Cria o DataFrame vazio para usarmos
df_final = pd.DataFrame({
    'razao_social': ['EXPEDITO APARECIDO DITOS'],
    'cnpj': ['46.835.567/0001-89']
})

print('Iniciando raspagem de dados...')

# Loop que faz a paginação
for i in range(1):
    data = {
        "query": {
            "termo": [],
            "atividade_principal": [],
            "natureza_juridica": [],
            "uf": [],
            "municipio": [],
            "bairro": [],
            "situacao_cadastral": "ATIVA",
            "cep": [],
            "ddd": []
        },
        "range_query": {
            "data_abertura": {
                "lte": None,
                "gte": "2024-07-01"
            },
            "capital_social": {
                "lte": None,
                "gte": None
            }
        },
        "extras": {
            "somente_mei": False,
            "excluir_mei": True,
            "com_email": True,
            "incluir_atividade_secundaria": False,
            "com_contato_telefonico": False,
            "somente_fixo": False,
            "somente_celular": False,
            "somente_matriz": False,
            "somente_filial": False
        },
        "page": i
    }

    print(f'Raspando página {i} ', end='')

    proxy = get_random_proxy()
    driver = configurar_selenium(proxy)

    url = 'https://casadosdados.com.br/solucao/cnpj/pesquisa-avancada'
    driver.get(url)

    time.sleep(random.uniform(3, 5))

    page_content = driver.page_source

    df_provisorio = pd.DataFrame({
        'razao_social': ['SUPERMERCADOS BH COMERCIO DE ALIMENTOS S/A'],
        'cnpj': ['43.853.977/0001-64']
    })
    df_final = pd.concat([df_final, df_provisorio], axis=0)

    print(f'- OK')

    time.sleep(random.uniform(3, 7))

    driver.quit()

print('Raspagem inicial feita com sucesso!')

print('Iniciando extração dos dados adicionais...')

print("Colunas do DataFrame df_final:")
print(df_final.columns)

print("Primeiras linhas do DataFrame df_final:")
print(df_final.head())

if 'razao_social' in df_final.columns and 'cnpj' in df_final.columns:
    url = []
    for razao_social, cnpj in zip(df_final['razao_social'], df_final['cnpj']):
        nome_fantasia = re.sub(r'[^\w\s]', '', razao_social).replace(' ', '-').lower()
        url.append(f'https://casadosdados.com.br/solucao/cnpj/{nome_fantasia}-{cnpj}')
else:
    print("Colunas 'razao_social' e/ou 'cnpj' não encontradas no DataFrame.")
    url = []

lista_email = []
lista_tel = []
lista_socio1 = []
lista_socio2 = []
lista_socio3 = []
lista_socio4 = []
lista_socio5 = []
lista_capital_social = []

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

for indice, link in enumerate(url):
    if link:
        proxy = get_random_proxy()
        driver = configurar_selenium(proxy)

        print(f'Empresa {indice + 1}/{len(df_final)} ', end='')

        try:
            driver.get(link)
            time.sleep(random.uniform(3, 5))

            try:
                email = driver.find_element(By.XPATH, '//*[@id="__nuxt"]id("__nuxt")/DIV[1]/SECTION[4]/DIV[2]/DIV[1]/DIV[1]/DIV[19]').text
                lista_email.append(email.lower())
            except:
                lista_email.append('')

            try:
                tel = driver.find_element(By.XPATH, '//*[@id="__nuxt"]id("__nuxt")/DIV[1]/SECTION[4]/DIV[2]/DIV[1]/DIV[1]/DIV[20]').text
                lista_tel.append(tel)
            except:
                lista_tel.append('')

            try:
                socio1 = driver.find_element(By.XPATH, '//*[@id="__nuxt"]id("__nuxt")/DIV[1]/SECTION[4]/DIV[2]/DIV[1]/DIV[1]/DIV[24]').text
                lista_socio1.append(socio1)
            except:
                lista_socio1.append('')

            try:
                socio2 = driver.find_element(By.XPATH, '//*[@id="__nuxt"]id("__nuxt")/DIV[1]/SECTION[4]/DIV[2]/DIV[1]/DIV[1]/DIV[24]').text
                lista_socio2.append(socio2)
            except:
                lista_socio2.append('')

            try:
                socio3 = driver.find_element(By.XPATH, '//*[@id="__nuxt"]id("__nuxt")/DIV[1]/SECTION[4]/DIV[2]/DIV[1]/DIV[1]/DIV[24]').text
                lista_socio3.append(socio3)
            except:
                lista_socio3.append('')

            try:
                socio4 = driver.find_element(By.XPATH, '//*[@id="__nuxt"]id("__nuxt")/DIV[1]/SECTION[4]/DIV[2]/DIV[1]/DIV[1]/DIV[24]').text
                lista_socio4.append(socio4)
            except:
                lista_socio4.append('')

            try:
                socio5 = driver.find_element(By.XPATH, '//*[@id="__nuxt"]id("__nuxt")/DIV[1]/SECTION[4]/DIV[2]/DIV[1]/DIV[1]/DIV[24]').text
                lista_socio5.append(socio5)
            except:
                lista_socio5.append('')

            try:
                capital_social = driver.find_element(By.XPATH, '//*[@id="__nuxt"]id("__nuxt")/DIV[1]/SECTION[4]/DIV[2]/DIV[1]/DIV[1]/DIV[10]').text
                if is_number(capital_social):
                    lista_capital_social.append(capital_social)
                else:
                    lista_capital_social.append('')
            except:
                lista_capital_social.append('')

            print(f'- OK')
        except Exception as e:
            print(f'Erro ao acessar a URL {link}: {e}')
        finally:
            driver.quit()

        time.sleep(random.uniform(3, 7))

print('Dados adicionais extraídos com sucesso!')

# Verificar comprimento das listas
print(f'Comprimento das listas:')
print(f' lista_email: {len(lista_email)}')
print(f' lista_tel: {len(lista_tel)}')
print(f' lista_socio1: {len(lista_socio1)}')
print(f' lista_socio2: {len(lista_socio2)}')
print(f' lista_socio3: {len(lista_socio3)}')
print(f' lista_socio4: {len(lista_socio4)}')
print(f' lista_socio5: {len(lista_socio5)}')
print(f' lista_capital_social: {len(lista_capital_social)}')

# Garantir que todas as listas têm o mesmo comprimento
max_length = max(len(lista_email), len(lista_tel), len(lista_socio1), len(lista_socio2), len(lista_socio3), len(lista_socio4), len(lista_socio5), len(lista_capital_social))
for lista in [lista_email, lista_tel, lista_socio1, lista_socio2, lista_socio3, lista_socio4, lista_socio5, lista_capital_social]:
    while len(lista) < max_length:
        lista.append('')

# Criar DataFrame com os dados extraídos
df_dados_extraidos = pd.DataFrame({
    'email': lista_email,
    'telefone': lista_tel,
    'socio1': lista_socio1,
    'socio2': lista_socio2,
    'socio3': lista_socio3,
    'socio4': lista_socio4,
    'socio5': lista_socio5,
    'capital_social': lista_capital_social
})

# Salvar o DataFrame em um arquivo Excel
nome_arquivo = 'dados_extraidos_'
for i in range(5):
    try:
        df_dados_extraidos.to_excel(f'C:\\Users\\teste\\Desktop\\web-dev\\Leads Autmatizado\\{nome_arquivo}{i}.xlsx', index=False)
        print(f'Arquivo "{nome_arquivo}{i}.xlsx" salvo com sucesso.')
        break
    except Exception as e:
        print(f'Erro ao salvar o arquivo: {e}')
        continue
