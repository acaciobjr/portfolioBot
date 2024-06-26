from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from tabulate import tabulate
import time
import os
from datetime import datetime

def busca(nome):
    while True:
        try:     
            xpathBusca = "//div[contains(text(), 'Search')]"       
            pesquisa = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpathBusca)))
            pesquisa.click()          
            print('abrindo pesquisa')
            time.sleep(4) 
            xpathinput = "//input[@class='sc-d565189d-3 kKevNe desktop-input']"
            print('procurando input pesquisa')
            pesquisai = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpathinput)))
            if pesquisai is not None:
                pesquisai.click()     
                pesquisai.clear()  
                print(f'tentando enviar pesquisa: {nome}')
                pesquisai.send_keys(nome)
                break
        except Exception as e:
            print(f'1-espaço input não achado Erro: {str(e)}')
    
file_path = input('digite o caminho completo para o notepad: ')

informacoes_usuario = {}

PATH = file_path
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    print("arquivo existe e é legível")
else:
    print("arquivo não existe ou está ilegível")

try:
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':',1)
                key = key.strip()
                value = value.strip()
                try:
                    value = float(value)
                except ValueError:
                    print(f"Valor não pode ser convertido para float: {value}")
                    continue
                informacoes_usuario[key] = value
except Exception as e:
    print(f'Erro ao achar o diretorio: {e}') 

print("O portfolio é:")
print(informacoes_usuario)

quantidade_chaves = len(informacoes_usuario)
projecao = {}
for chave in informacoes_usuario:
    novo_valor = input(f"Digite sua projeção de multiplicação para o ativo:'{chave}': ")
    novo_valor1 = float(novo_valor)
    projecao[chave] = novo_valor1

print("suas projeções para cada ativo são:")
print(projecao)

driver = webdriver.Chrome()
try:
    driver.get("https://www.google.com/search?q=dolar")
except:
    print('página do dolar nao abriu')

try:
    xpathD = "//*[@id='knowledge-currency__updatable-data-column']/div[1]/div[2]/span[1]"
    imgPreco2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpathD)))
    preco = imgPreco2.text
    preco2 = preco.replace(',', '.')
    print(preco2)
    taxa_dolar_real = float(preco2)
    print(f'O preço do dólar é {taxa_dolar_real}')
except Exception as e:
    print(f'Erro ao obter o preço do dólar: {e}')
driver.quit()

driver = webdriver.Chrome()
try:
    driver.get("https://coinmarketcap.com/")
    driver.maximize_window()
    time.sleep(8)
except:
    print('nao abriu')

cabecalho = ["Nome da Moeda", "Quantidade", "Preço do ativo $US", "Preço do ativo R$", "saldo em dolar", "saldo em real", "Projeção futura R$"]
tabela = []
for moeda, quantidade in informacoes_usuario.items():       
    
    while True:
        try:  
            busca(moeda)
            time.sleep(7)
            asset = "//div[@class='sc-f70bb44c-0 sc-230facf7-2 xRfEp' and contains(text(), 'Cryptoassets')]"
            pesquisa3 = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, asset))
            )
            visible = pesquisa3.text
            print('o nome achado em cima da busca foi:',visible)
            if visible == 'Cryptoassets':
                print('validação de categoria, ok')
                #buscaResult = '//div[@class="sc-42dd6c6d-0 VWkPh focused"]'
                #buscaResult = '//div[@class="sc-d5a83aa9-0 cNbNlm focused"]'
                buscaResult = '//div[@class="sc-d5a83aa9-4 kgda-dh"]'                
                pesquisa2 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, buscaResult))
                )
                print('clicando')
                pesquisa2.click()
                time.sleep(5)
                break            
        except (NoSuchElementException, TimeoutException) as e:
            print("'Cryptoassets' não encontrado. Tentando novamente em 2 segundos...")
    
    try:
        print('buscando preço')
        imgPreco = "//*[@id='section-coin-overview']/div[2]/span"
        imgPreco2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, imgPreco)))
        preco2 = imgPreco2.text
        print(f'preço de {moeda} é {preco2}')        
    except (StaleElementReferenceException, NoSuchElementException, TimeoutException):
        print('preço não achado. tentando outro xpath')
        imgPreco = '//div[@class="sc-f70bb44c-0 jxpCgO base-text"]'
        imgPreco2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, imgPreco)))
        preco2 = imgPreco2.text
        print(f'preço de {moeda} é {preco2}')
    
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
    precoReal = valorDolar * taxa_dolar_real
    novo_valor1 = projecao[moeda]
    realProjecao = total_em_real * novo_valor1
    
    linha_atual = [moeda, quantidade, valorDolar, precoReal, total_em_dólar, total_em_real, realProjecao]
    tabela.append(linha_atual)

total_em_real_sum = sum(linha_atual[5] for linha_atual in tabela)
total_em_real_proj = sum(linha_atual[6] for linha_atual in tabela)

for linha_atual in tabela:
    total_em_real = linha_atual[5]
    porcentagem_ativo = (total_em_real / total_em_real_sum) * 100
    linha_atual.append(porcentagem_ativo)
    
cabecalho.extend(['Porcentagem Atual'])
tabela2 = tabulate(tabela, headers=cabecalho, tablefmt="grid")
print(tabela2)
print(f"O valor total da sua carteira é: R${total_em_real_sum}. A projeção por sua amostra é: {total_em_real_proj}")

data_atual = datetime.now().strftime("%Y-%m-%d")
caminho = fr"(diretório de destino)_{data_atual}"
extensao = '.txt'
contador = 1

while True:  
    Arq = f"{caminho}_{contador}{extensao}"
    if not os.path.exists(Arq):
        break
    contador += 1

with open(Arq, 'w') as arquivo:
    arquivo.write(tabela2 + "\n" + f"O valor total da sua carteira é: R${total_em_real_sum}. A projeção por sua amostra é: {total_em_real_proj}")
    print(f"O arquivo Notepad foi criado com sucesso em: {Arq}")
driver.quit()
