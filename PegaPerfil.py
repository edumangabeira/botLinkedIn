from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from parsel import Selector
import re
import time
# import os
# import logging


def getDriverOnLinkedIn(timeout):
    # cria nova sessão no browser
    driver = webdriver.Chrome("./chromedriver")

    driver.implicitly_wait(timeout)  # 30 segundos para iniciar o browser
    driver.maximize_window()  # maximiza ao iniciar
    # Navega até a home page
    driver.get("https://linkedin.com")
    return driver


def fazerLogin(usuario, senha, driver):

    user = driver.find_element_by_name('session_key')
    user.clear()
    user.send_keys(usuario)

    password = driver.find_element_by_name('session_password')
    password.clear()
    password.send_keys(senha)

    password.submit()  # Simulating user pressing Enter after type the password
    # I could simulate press the button to submit, but that was not necessary. The Enter is enough.


def getParametrosBot(arquivo):

    parametros = {}
    for linha in arquivo:
        texto = re.sub('#+[\s\S]*', "", linha)
        texto = texto.strip()
        if len(texto) > 0:
            chave, valor = texto.split("=")
            chave = chave.strip()
            valor = valor.strip()
            parametros[chave] = valor

    return parametros


def campos_perfil() 


def pegandoPerfil(driver, contato):
    driver.get("https://linkedin.com{}".format(contato))
    time.sleep(5)
    sel = Selector(text=driver.page_source)
    campos = []

    ''' campo nome '''
    nome = sel.xpath('//*[starts-with(@class, "pv-top-card-section__name")]/text()').extract_first()
    print(nome)
    descricao = ""
    formacao = ""
    cargos = []
    recomendacoes = []
    interesses = []

    # driver.find_element_by_xpath("//div[contains(@class='pv-top-card-section__name')]/h1")
    # "//div[contains(@class='pv-top-card-section__name.inline.t-24.t-black.t-normal')]/h1")
    # nome.get_attribute("innerHTML")
    campos.append(nome.strip())
    # campos.extend(nome, descricao, formacao, cargos, recomendacoes, interesses)
    print(campos)
    return campos


def RodarColetador(arquivo, contatos):

    with open(arquivo, "r") as arq:
        parametros = getParametrosBot(arq)

    with open(contatos, "r") as contatos:
        for contato in contatos:
            contato = str(contato)
            contato = contato.strip()
            driver = getDriverOnLinkedIn(parametros['timeoutNavegador'])
            time.sleep(int(parametros['timeToLogIn']))
            user = parametros['user']
            password = parametros['password']
            fazerLogin(user, password, driver)
            # raise Exception("Invalid login")
            # waiting the user login before catch the desired fields
            time.sleep(int(parametros['timeToLoadTheProfile']))

            perfil = pegandoPerfil(driver, contato)
            contato = contato.replace("/", "").replace("in", "_")
            with open("perfil{}.txt".format(contato), "w") as arq:
                for campo in perfil:
                    arq.write("nome:{}".format(perfil[0]))


if __name__ == '__main__':
   
    RodarColetador("config_labcorres.txt", "simula_contatos.txt")
