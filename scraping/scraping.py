"""
Busca os dados do site fundamentus e salva em CSV.
"""
import pandas as pd

import requests
from bs4 import BeautifulSoup

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

class Scraping:
    """responsavel por puchar as informações da internet
    """
    def scraping(self):
        """
        Pucha dados da internet e salva em CSV
        """

        # -> usando selenium
        # # configurar o chrome
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # # webscrapping da tabela
        # driver.get("https://www.fundamentus.com.br/resultado.php")
        # localTabela = "/html/body/div[1]/div[2]/table"
        # tabela = driver.find_element("xpath", localTabela)
        # # tratamento da tabela
        # html_tabela = tabela.get_attribute("outerHTML")

        # -> Puchar site usando requests e bs4
        headers = {
            'User-Agent'        : 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
            'Accept'            : '*/*',
            'Accept-Language'   : 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'DNT'               : '1',
            'Connection'        : 'close'
        }
        link = 'https://www.fundamentus.com.br/resultado.php'
        requisicao = requests.get(link, headers=headers, timeout=5).text
        soup = BeautifulSoup(requisicao, "html.parser")
        table = soup.find('table')

        # Criando tabela
        tabela = pd.read_html(str(table), thousands=".", decimal=",")[0]

        # # filtrar colunas
        # # tabela = tabela[["Papel", "Cotação", "EV/EBIT", "ROIC", "Liq.2meses", "Div.Yield"]]

        # tratamento de dados das colunas principais
        tabela["ROIC"] = tabela["ROIC"].str.replace("%", "")
        tabela["ROIC"] = tabela["ROIC"].str.replace(".", "")
        tabela["ROIC"] = tabela["ROIC"].str.replace(",", ".")
        tabela["ROIC"] = tabela["ROIC"].astype(float)
        tabela["Div.Yield"] = tabela["Div.Yield"].str.replace("%", "")
        tabela["Div.Yield"] = tabela["Div.Yield"].str.replace(".", "")
        tabela["Div.Yield"] = tabela["Div.Yield"].str.replace(",", ".")
        tabela["Div.Yield"] = tabela["Div.Yield"].astype(float)
        tabela["Div.Yield"] = round(tabela["Div.Yield"] / 100, 2)

        # print(tabela)

        # Salvando arquivo CSV
        tabela.to_csv("CSV/data_base.csv", index=False)


# scraping()
