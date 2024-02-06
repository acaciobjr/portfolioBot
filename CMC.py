from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from forex_python.converter import CurrencyRates
from tabulate import tabulate
#from selenium.common.exceptions import NoSuchElementException
#from selenium.common.exceptions import TimeoutException
import time

informacoes_usuario = {}
continuar = True
while continuar:
    moeda = input("Digite o nome da moeda (ou 'sair' para encerrar): ")    
    if moeda.lower() == 'sair':
        continuar = False
        break
    quantidade = float(input(f"Digite a quantidade de {moeda} que você possui: "))    
    informacoes_usuario[moeda] = quantidade

print("O portfolio é:")
print(informacoes_usuario)

c = CurrencyRates()
taxa_dolar_real = c.get_rate('USD', 'BRL')

driver = webdriver.Chrome()
driver.get("https://coinmarketcap.com/")
driver.maximize_window()
time.sleep(8)

cabecalho = ["Nome da Moeda", "Quantidade", "Preço em Dólar", "total em dolar", "total em real"]
tabela = []

for moeda, quantidade in informacoes_usuario.items():
    
    xpathBusca = ["//html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[3]/div/div[2]/div[3]/div/div[1]",
                  "//html/body/div[1]/div[2]/div/div[1]/div/div[1]/div/div[3]/div/div[2]/div[3]/div/div[1]"]
    for xpath in xpathBusca:
        try:            
            pesquisa = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))
            pesquisa.click()
            print('abrindo pesquisa')
            time.sleep(4)            
            break
        except Exception as e:
            print(f'1-botão de pesquisa não achado Erro: {str(e)}')
            continue
          
    input = "//html/body/div[1]/div[2]/div/div[1]/div/div[1]/div/div[3]/div/div[2]/div[4]/div/div/div/div/div[1]/div[1]/div[1]"
    print('procurando input pesquisa')
    try:
        pesquisai = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, input))
        )
        #pesquisai.click()
        time.sleep(5)
        primeira_chave = moeda
        print('tentando enviar pesquisa')
        pesquisai.send_keys(moeda)
    except Exception as m:
        print(f'2-espaço de input não achado Erro: {str(m)}')
        break
    time.sleep(6)
    buscaResult = "//html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[3]/div/div[2]/div[4]/div/div/div/div/div[2]/div[2]/div[1]/a[1]/div"
    pesquisa2 = WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.XPATH, buscaResult))
    )
    print('tentando clicar moeda buscada')
    pesquisa2.click()
    time.sleep(10)
    try:
        print('buscando preço')
        imgPreco = "//*[@id='section-coin-overview']/div[2]/span"
        imgPreco2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, imgPreco)))
        preco2 = imgPreco2.text
        print(f'preço de {primeira_chave} é {preco2}')
    except StaleElementReferenceException:
        print('preço não achado')

    primeiraQuantidade = quantidade   
    valor = preco2.replace('$', '')
    valorDolar = float(valor)
    montante = primeiraQuantidade * valorDolar
    print(f'Seu montante para {primeira_chave} é de ${montante}')
    moeda = primeira_chave
    quantidade = primeiraQuantidade
    preço_em_dólar = valorDolar
    total_em_dólar = round(montante, 2)
    total_em_real = montante * taxa_dolar_real
    linha_atual = [moeda, quantidade, preço_em_dólar, total_em_dólar, total_em_real]
    tabela.append(linha_atual)

#fora do for
tabela2 = tabulate(tabela,headers=cabecalho,tablefmt="grid")
print(tabela2)

#loading...
