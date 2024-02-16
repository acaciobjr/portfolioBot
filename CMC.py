from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from forex_python.converter import CurrencyRates
from tabulate import tabulate
import time
import os
from datetime import datetime

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
#tabela_atualizada = []

for moeda, quantidade in informacoes_usuario.items():
    
    xpathBusca = '//html/body/div[1]/div[2]/div/div[1]/div/div[1]/div/div[3]/div/div[2]/div[3]/div/div[1]'
    xpathinput = "//html/body/div[1]/div[2]/div/div[1]/div/div[1]/div/div[3]/div/div[2]/div[4]/div/div/div/div/div[1]/div[1]/div[1]/input"
    try:            
        pesquisa = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, xpathBusca)))
        pesquisa.click()
        print('abrindo pesquisa')
        time.sleep(4) 
        print('procurando input pesquisa')
        pesquisai = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, xpathinput)))
        pesquisai.click()        
        time.sleep(5)
        print(f'tentando enviar pesquisa: {moeda}')
        pesquisai.send_keys(moeda)
    except Exception as e:
        print(f'1-espaço input não achado Erro: {str(e)}')
        break
        
    time.sleep(13)
    buscaResult = "//html/body/div[1]/div[2]/div/div[1]/div/div[1]/div/div[3]/div/div[2]/div[4]/div/div/div/div/div[2]/div[2]/div[1]/a[1]/div"
    pesquisa2 = WebDriverWait(driver, 45).until(
    EC.visibility_of_element_located((By.XPATH, buscaResult))
    )
    print('tentando clicar moeda buscada')
    pesquisa2.click()
    time.sleep(8)
    try:
        print('buscando preço')
        imgPreco = "//*[@id='section-coin-overview']/div[2]/span"
        imgPreco2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, imgPreco)))
        preco2 = imgPreco2.text
        print(f'preço de {moeda} é {preco2}')
    except StaleElementReferenceException:
        print('preço não achado')

    primeiraQuantidade = quantidade   
    if ',' in preco2:
        valor = preco2.replace('$', '').replace(',', '')
        parte_inteira, parte_decimal = valor.rsplit('.', 1)
        valor = parte_inteira + '.' + parte_decimal
    else:    
        valor = preco2.replace('$', '')
    
    valorDolar = float(valor)
    montante = primeiraQuantidade * valorDolar
    print(f'Seu montante para {moeda} é de ${montante}')
    quantidade = primeiraQuantidade
    total_em_dólar = round(montante, 2)
    total_em_real = montante * taxa_dolar_real
    
    linha_atual = [moeda, quantidade, valorDolar, total_em_dólar, total_em_real]
    tabela.append(linha_atual)
    
tabela2 = tabulate(tabela,headers=cabecalho,tablefmt="grid")
total_em_real_sum = 0
total_em_real_sum = sum(linha_atual[4] for linha_atual in tabela)

for linha_atual in tabela:
    total_em_real = linha_atual[4]
    porcentagem_ativo = (total_em_real / total_em_real_sum) * 100
    linha_atual.append(porcentagem_ativo)
    
tabela2 = tabulate(tabela, headers=cabecalho + ['Porcentagem'], tablefmt="grid")
print(tabela2)
print(f"O valor total da sua carteira é: R${total_em_real_sum}")

data_atual = datetime.now().strftime("%Y-%m-%d")
caminho = fr"endereço do diretório\portfolio_{data_atual}.txt"

with open(caminho, 'w') as arquivo:
    arquivo.write(tabela2 + "\n" + f"O valor total da sua carteira é: R${total_em_real_sum}")

if os.path.exists(caminho):
    print(f"O arquivo Notepad foi criado com sucesso em: {caminho}")
else:
    print("Erro ao criar o arquivo Notepad.")
