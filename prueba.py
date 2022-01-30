from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time
from selenium.common.exceptions import NoSuchElementException

correo = 'rh0test0ga@gmail.com'
contrasenia = '123698745874' 
busqueda = 'Carta a nuestro profe Fajardo en nombre del equipo de Voluntarios Coalición Colombia' 
urls_comentarios_strs = []
datos = []

def cargar_mas_comentarios ():
    boton_cargar_mas = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div[2]/div/button'))
    )
    boton_cargar_mas.click()
    time.sleep(3)

#Instanciando WebDriver

serv = Service('WEB_DRIVERS/chromedriver.exe')
opt = webdriver.ChromeOptions()
opt.add_argument('start-maximized')
driver = webdriver.Chrome(service=serv, options=opt) #crear instancia de driver y abrir navegador (Chrome)
driver.get('https://www.change.org/')

#iniciando sesión

driver.find_element(By.XPATH, '/html/body/div[2]/header/div[2]/div/div/div[2]/table/tbody/tr/td[2]/button').click()

input_user = driver.find_element(By.XPATH, '/html/body/div[2]/header/div[3]/div/div/div/form/div[1]/div[1]/div/span/input')
input_user.send_keys(correo)

input_contasenia = driver.find_element(By.XPATH, '/html/body/div[2]/header/div[3]/div/div/div/form/div[1]/div[2]/div/span/input')
input_contasenia.send_keys(contrasenia)

driver.find_element(By.XPATH, '/html/body/div[2]/header/div[3]/div/div/div/form/div[3]/div/input').click()

#Navegando hasta la página requerida: sección de Comentarios

time.sleep(3)

boton_buscar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/header/div[2]/div/div/div[2]/table/tbody/tr/td[1]/a/span')))

time.sleep(3)

boton_buscar.click()

input_busqueda = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div/div/div/div/div/div/div[1]/form/div/div/div/div[1]/input'))
)

input_busqueda.send_keys(busqueda)

WebDriverWait(driver, 50).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div/div/div/div/div/div/div[1]/form/div/div/div/div[2]/button'))
).click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div/div/div/div/div/div/div[2]/ul/div[1]/a/div/div'))
).click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/nav/div/a[2]/div/div/span'))
).click()

#Obteniendo url de cada comentario:

for i in range(5): #Número de veces que se cargan más comentarios (hace click en 'Cargar más')
    cargar_mas_comentarios()

divs = driver.find_elements(By.CLASS_NAME,'pam xs-pas'.replace(' ', '.'))
time.sleep(5)

for i in range(1, len(divs)+1):
    elemento_xpath = f'/html/body/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div[1]/div[{i}]/div/div/div/a'
       
    try:
        url_comentario = driver.find_element(By.XPATH, elemento_xpath)
    
    except NoSuchElementException:
        elemento_xpath = f'/html/body/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div[1]/div[{i}]/div/div/a[2]'
        url_comentario = driver.find_element(By.XPATH, elemento_xpath)
        
    finally:
        urls_comentarios_strs.append(url_comentario.get_attribute('href'))
        

print('Número de comentarios cargados: ', len(urls_comentarios_strs))

#Accediendo a cada comentario

for url_comentario in urls_comentarios_strs:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url_comentario)
    time.sleep(2)
    
    nombre = driver.find_element(By.TAG_NAME, 'h1').text
    ubicacion = driver.find_element(By.CLASS_NAME, 'type-weak mbs'.replace(' ', '.')).text
    datos.append([nombre, ubicacion])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
       
#for dato in datos:
#    print(f'{dato[0]:{35}} {dato[1]:{25}}')

driver.close()    

#______________________________________________________________________________________________

from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'clave.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID spreadsheet.
SAMPLE_SPREADSHEET_ID = '14pTDxuItmbQ4LQvBw4Oz80Q1SWGPfXKDbS3FbuWNh3I' #ID de SPREADSHEET para escribir o leer

service = build('sheets', 'v4', credentials=creds) #Obtener acceso al servicio de la API

# Call the Sheets API
sheet = service.spreadsheets()
#Obtener datos (read Sheet)
'''
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="noms_locs!A1:B4").execute()
values = result.get('values', [])
'''

#Actualizar/cargar datos al sheet
request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                            range="noms_locs!A2", valueInputOption="USER_ENTERED", body={"values":datos}).execute()  

    

    




