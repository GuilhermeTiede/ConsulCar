from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import pywhatkit as kit
import os
import requests
from urllib.parse import unquote
from selenium.webdriver.common.action_chains import ActionChains

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/automacao", methods=["POST"])
def automacao():
    print("Executando Santander")

    cpf_login = "03907034198"
    senha_login = "Udyr2222$"
    cpf_cliente = request.form["cpf_cliente"]
    print("CPF ACEITO")
    placa = request.form["placa"]
    print("PLACA aceita")
    valor_veiculo = request.form["valor_veiculo"]
    print("VALOR ACEITO")
    numero_whatsapp = request.form["whatsapp"]
    print("WHATASPP ACEITO")
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument('--start-fullscreen')

    # Configurar o WebDriver do Chrome com o modo headless
    navegador = webdriver.Chrome(options=options)

    # Acessar a página da web
    navegador.get("https://brpioneer.accenture.com/originacao-auto/login")

    print("Executando Santander Navegador")

    campo_cpf = WebDriverWait(navegador, 15).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='documentNumber']"))
    )

    campo_cpf.send_keys(cpf_login)

    campo_senha = WebDriverWait(navegador, 15).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='password']"))
    )

    campo_senha.send_keys(senha_login)

    # Aguarde até que o botão "Entrar" seja clicável
    botao_entrar = WebDriverWait(navegador, 15).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-flat-button"))
    )

    # Clique no botão "Entrar"
    botao_entrar.click()

#########################################FIM DO LOGIN################################################

    # Encontre o elemento div com a classe "personal-container"
    personal_container = WebDriverWait(navegador, 25).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, 'div.personal-container'))
    )

    campo_cpf = personal_container.find_element(By.CSS_SELECTOR, 'input[formcontrolname="documentNumber"]')

    campo_cpf.send_keys(cpf_cliente)
    campo_cpf.send_keys(Keys.TAB)

    # Certifique-se de que a página foi carregada completamente, esperando pelo elemento "mat-radio-group"
    mat_radio_group = WebDriverWait(navegador, 15).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'mat-radio-group'))
    )

    # Adicione uma pausa curta (opcional)
    import time
    time.sleep(3)

    # Localize o botão de opção "Busca por placa" dentro do elemento "mat-radio-group"
    opcao_busca_por_placa = mat_radio_group.find_element(By.XPATH, ".//span[text()=' Busca por placa ']")

    ActionChains(navegador).move_to_element(opcao_busca_por_placa).perform()

    # Clique no botão de opção
    opcao_busca_por_placa.click()

    campo_placa = WebDriverWait(navegador, 15).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='searchPlate']"))
    )

    campo_placa.send_keys(placa)
    time.sleep(3)
    campo_placa.send_keys(Keys.TAB)

    campo_valor_veiculo = WebDriverWait(navegador, 20).until(
        ec.visibility_of_element_located((By.ID, "mat-input-5"))
    )

    campo_valor_veiculo.send_keys(valor_veiculo)
    time.sleep(1)
    campo_valor_veiculo.send_keys(Keys.TAB)

    botao_continuar = WebDriverWait(navegador, 15).until(
        ec.element_to_be_clickable((By.XPATH, "//button/span[text()=' Continuar ']"))
    )
    botao_continuar.click()

    botao_sim = WebDriverWait(navegador, 15).until(
        ec.element_to_be_clickable((By.XPATH, "//button/span[text()=' Sim ']"))
    )
    botao_sim.click()

    # Aguarde um tempo suficiente para que a página seja carregada completamente

    import time
    time.sleep(35)

    page_body = navegador.find_element(By.TAG_NAME, "body")

    page_body.screenshot("images/tela_cheia.png")

    # Renomeie o arquivo para "tela_cheia.jpg"
    caminho_imagem_png = "images/tela_cheia.png"
    caminho_imagem_jpg = "images/tela_cheia.jpg"
    os.rename(caminho_imagem_png, caminho_imagem_jpg)

    titulo_pagina = "Santander"

    # Fechar o navegador
    navegador.quit()

    # Caminho para a imagem a ser enviada
    caminho_imagem = "/Users/guilhermetiede/Documents/GitHub/ConsultaCred/images/tela_cheia.jpg"

    # Enviar a imagem para o WhatsApp
    kit.sendwhats_image(numero_whatsapp, caminho_imagem, titulo_pagina)

    return "Automação concluída e a página foi salva como 'full_page_screenshot.png'"


@app.route("/itau", methods=["POST"])
def itau():
    print("Executando Itau")
    cpf_cliente = request.form["cpf_cliente"]
    placa = request.form["placa"]
    valor_veiculo = request.form["valor_veiculo"]
    numero_whatsapp = request.form["whatsapp"]

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument('--start-fullscreen')

    # Configurar o WebDriver do Chrome com o modo headless
    navegador = webdriver.Chrome(options=options)

    navegador.get("https://www.credlineitau.com.br/simulator")

    email = "Raisa.novaveiculos@gmail.com"
    senha = "Nova@2025"

    # Localize o elemento iframe
    iframe = navegador.find_element(By.TAG_NAME, "iframe")

    # Mude o foco para o iframe
    navegador.switch_to.frame(iframe)

    # Aguarde até que o campo de e-mail seja visível
    campo_email = WebDriverWait(navegador, 10).until(
        ec.visibility_of_element_located((By.ID, "username"))
    )
    campo_email.send_keys(email)

    # Aguarde até que o campo de senha seja visível
    campo_senha = WebDriverWait(navegador, 20).until(
        ec.visibility_of_element_located((By.ID, "password"))
    )
    campo_senha.send_keys(senha)

    # Aguarde até que o botão "Entrar" seja clicável e clique nele
    botao_entrar = WebDriverWait(navegador, 20).until(
        ec.element_to_be_clickable((By.ID, "kc-login"))
    )
    botao_entrar.click()

    ##############################################FIM LOGIN ITAU######################################################
    # Após o login, voltar ao contexto padrão
    navegador.switch_to.default_content()

    # Aguarde até que o campo de CPF seja visível
    campo_cpf = WebDriverWait(navegador, 20).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, "input[data-placeholder='CPF']"))
    )

    # Insira o valor do CPF no campo
    campo_cpf.send_keys(cpf_cliente)

    import time

    # Aguarde 1 segundo após a inserção do CPF
    time.sleep(3)

    # Localize a imagem pelo atributo 'src'
    imagem_chassi_plate = navegador.find_element(By.CSS_SELECTOR, 'img[src="/assets/img/simulator/chassi-plate-search'
                                                                 '-icon.svg"]')

    # Clique na imagem
    imagem_chassi_plate.click()

    # Localize o campo de input da placa
    campo_placa = navegador.find_element(By.CSS_SELECTOR, 'input[formcontrolname="vehicleIdentification"]')

    campo_placa.send_keys(placa)

    # Localize e clique no botão "buscar veículo"
    botao_buscar = navegador.find_element(By.CSS_SELECTOR, 'button.btn-search-vehicle')
    botao_buscar.click()

    # Aguarde até que os elementos de seleção de modelo estejam visíveis
    elementos_modelo = WebDriverWait(navegador, 10).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[formcontrolname="vehicle"]'))
    )

    # Verifique se há algum modelo disponível
    if elementos_modelo:
        # Se houver modelos, clique no primeiro
        primeiro_modelo = elementos_modelo[0]
        primeiro_modelo.click()

    # Aguarde até que o botão "selecionar veículo" esteja visível e clicável
    botao_selecionar = WebDriverWait(navegador, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.voxel-button.voxel-button--full'))
    )

    # Clique no botão "selecionar veículo"
    botao_selecionar.click()

    # Aguarde até que o campo de Valor Veículo seja visível
    campo_valor = WebDriverWait(navegador, 20).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, "input[data-placeholder='valor do veículo']"))
    )

    # Insira o valor do CPF no campo
    campo_valor.send_keys(valor_veiculo)

    import time
    time.sleep(10)

    page_body = navegador.find_element(By.TAG_NAME, "body")
    elemento = navegador.find_element(By.CSS_SELECTOR, 'mat-card[formgroupname="operationRequest"]')

    # Role a página para o elemento
    navegador.execute_script("arguments[0].scrollIntoView(true);", elemento)
    for _ in range(1):
        navegador.execute_script("window.scrollBy(0, window.innerHeight/1.5);")
        time.sleep(1)

    page_body.screenshot("images/itau.png")

    # Renomeie o arquivo para "tela_cheia.jpg"
    caminho_imagem_png = "images/itau.png"
    caminho_imagem_jpg = "images/itau.jpg"
    os.rename(caminho_imagem_png, caminho_imagem_jpg)

    titulo_pagina = "Itau"

    # Fechar o navegador
    navegador.quit()

    # Caminho para a imagem a ser enviada
    caminho_imagem = "/Users/guilhermetiede/Documents/GitHub/ConsultaCred/images/itau.jpg"

    # Faça o upload da imagem para o ImgBB
    response = requests.post("https://api.imgbb.com/1/upload", data={"key": "ed8bf3f23b33326552eee4693b90c95e"},
                             files={"image": (caminho_imagem, open(caminho_imagem, "rb"))})

    # Analise a resposta JSON
    json_response = response.json()

    # Obtenha o link da imagem enviada
    link_imagem = json_response["data"]["url"]
    print (link_imagem)
    link_final = unquote(link_imagem)
    print(link_final)
    wait_time = 7

    # Enviar a imagem para o WhatsApp
    kit.sendwhats_image(numero_whatsapp, caminho_imagem, titulo_pagina, wait_time)

    # kit.sendwhatmsg_instantly(numero_whatsapp, link_final, wait_time=6)

    return "Automação concluída e a página foi salva"


if __name__ == "__main__":
    app.run(debug=True)
