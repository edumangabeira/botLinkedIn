from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import time

def extraindoApenasTexto(tweet_texto):
    
    texto = re.sub('<[^>]*>'," ",tweet_texto)
    texto = re.sub('\s+',' ',texto)
    texto = texto.strip()
    return texto

def getDriverOnLinkedIn(timeout):
    # create a new browser session
    driver = webdriver.Chrome("./chromedriver")
    driver.implicitly_wait(timeout)#30 seconds to launch the browser
    driver.maximize_window()#When launched, maximize it
    # Navigate to the application home page
    driver.get("https://linkedin.com/login")
    #waiting the browser load the twitter webpage
    return driver
    
def fazerLogin(usuario,senha,driver):

    user = driver.find_element_by_name('session_key')
    user.clear()
    user.send_keys(usuario)

    password = driver.find_element_by_name('session_password')
    password.clear()
    password.send_keys(senha)

    password.submit()#Simulating user pressing Enter after type the password
    #I could simulate press the button to submit, but that was not necessary. The Enter is enough.

def getParametrosBot(arquivo):

    parametros = {}
    for linha in arquivo:
        texto = re.sub('#+[\s\S]*',"",linha)
        texto = texto.strip()
        if len(texto) > 0:
            
            chave,valor = texto.split("=")
            chave = chave.strip()
            valor = valor.strip()
            
            parametros[chave]=valor

    return parametros

def pegandoPerfil(driver):
    campos =[]
    # nome = driver.find_elements(By.CSS_SELECTOR,"pv-top-card-section__name.inline.t-24.t-black.t-normal")#find_elements_by_class_name pode usar tb
    nome = driver.find_element_by_xpath("//div[contains(@class='pv-top-card-section__name inline t-24 t-black t-normal')]/h1").get_attribute("innerHTML")
    campos = campos.append(nome)
    '''tweets_lis = element.find_elements(By.CSS_SELECTOR, "li.js-stream-item.stream-item.stream-item")#ou 
    return tweets_lis
    '''
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
            fazerLogin(user,password,driver)
            #waiting the user login before catch the desired fields
            time.sleep(int(parametros['timeToLoadTheProfile']))

            driver_perfil = driver.get("https://linkedin.com{}".format(contato))

            perfil = pegandoPerfil(driver_perfil)
            with open("perfil{}".format(contato),"w") as arq:
                for campo in perfil:
                    arq.write("nome:{}".format(perfil[0]))

if __name__ == '__main__':
    RodarColetador("config_labcorres.txt","simula_contatos.txt")