from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


class Wspra1:
    """
    Clase utilizada para realizar la descarga de productos y precios de comercialización de alimentos  en la principal
    sede de abastos del Pais.

    ...

    Atributos
    ----------
    opciones : webdriver.ChromeOptions()
        Variable para especificar las opciones con las que se deberá iniciar el navegador Chrome para el proceso de
        webscraping
    servicio : selenium.webdriver.chrome.service
        Ubicación de ejecutable 'chromedriver.exe'
    driver : selenium.webdriver
        Driver de conexión selenium a navegador Chrome
    fecha : datetime
        fecha a la cual corresponden los precios

    Methods
    -------
    __ingresa_tab
        usado para  enviar "TABS" al input de campo fecha

    __ingresa_reverse_tab
        usado para  enviar  "TABS" reversos al input de campo fecha

    selecciona_fecha
        Establece el valor de fecha en el campo input para realizar la descarga de datos

    genera_boletin_fecha
        Realiza clic sobre el boton de generación de boletin de precios

    descarga_precios
        retorna conjunto de datos de alimentos y precios en una fecha establecida

    """

    opciones = None
    servicio = None
    driver = None
    fecha = None

    def __init__(self):
        # Opciones del navegador
        self.opciones = webdriver.ChromeOptions()
        self.opciones.add_argument('--start-maximized')
        self.opciones.add_argument('--disable-extensions')
        self.opciones.add_argument('--headless')

        # Ubicación del driver de Chrome
        self.servicio = Service('./chromedriver.exe')

        self.driver = webdriver.Chrome(service=self.servicio, options=self.opciones)
        # Carga de la Url de corabastos
        self.driver.get('https://precios.precioscorabastos.com.co/#/boletin/grupos')

    def __ingresa_tab(self):
        WebDriverWait(self.driver, 1) \
            .until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-boletin-table/section/div/div['
                                                         '3]/div/div/div/div/div[1]/input'))) \
            .send_keys(Keys.TAB)

    def __ingresa_reverse_tab(self):
        WebDriverWait(self.driver, 1) \
            .until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-boletin-table/section/div/div['
                                                         '3]/div/div/div/div/div[1]/input'))) \
            .send_keys(Keys.SHIFT, Keys.TAB)

    def selecciona_fecha(self, anio, mes, dia):

        self.fecha = datetime(int(anio), int(mes), int(dia))

        WebDriverWait(self.driver, 5) \
            .until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-boletin-table/section/div/div['
                                                         '3]/div/div/div/div/div[1]/input'))) \
            .click()

        self.__ingresa_tab()
        self.__ingresa_tab()

        if self.driver.find_element(by=By.XPATH, value='/html/body/app-root/app-boletin-table/section/div/div['
                                                       '3]/div/div/div/div/div[1]/input') == self.driver.switch_to.active_element:
            WebDriverWait(self.driver, 2) \
                .until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-boletin-table/section/div/div['
                                                             '3]/div/div/div/div/div[1]/input'))) \
                .send_keys(anio)
            WebDriverWait(self.driver, 2) \
                .until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-boletin-table/section/div/div['
                                                             '3]/div/div/div/div/div[1]/input'))) \
                .send_keys(anio)
        else:
            WebDriverWait(self.driver, 2) \
                .until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-boletin-table/section/div/div['
                                                             '3]/div/div/div/div/div[1]/input'))) \
                .send_keys(anio)

        self.__ingresa_reverse_tab()
        self.__ingresa_reverse_tab()

        WebDriverWait(self.driver, 2) \
            .until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-boletin-table/section/div/div['
                                                         '3]/div/div/div/div/div[1]/input'))) \
            .send_keys(dia)

        WebDriverWait(self.driver, 2) \
            .until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-boletin-table/section/div/div['
                                                         '3]/div/div/div/div/div[1]/input'))) \
            .send_keys(mes)

    def genera_boletin_fecha(self, anio, mes, dia) -> None:

        self.selecciona_fecha(anio, mes, dia)

        print(self.fecha)

        # Botón generar boletin
        WebDriverWait(self.driver, 5) \
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.mat-focus-indicator mr-3 mat-raised-button '
                                                                'mat-button-base mat-primary'.replace(' ', '.')))) \
            .click()

    def descarga_precios(self):
        # Lectura de tablas de (1)Hortalizas, (2)Frutas, (3)Tubérculos, (4)Platanos, (5)Granos y Procesados,
        # (6)Lacteos, (7)Carnicos y (8)Huevos

        # Columnas del conjunto de datos
        codigos = []
        productos = []
        presentaciones = []
        cantidades = []
        unidades = []
        extras = []
        primeras = []
        corrientes = []

        try:
            # Iteración sobre cada una de las 8 "table"s con los productos
            for i in range(4, 12):
                WebDriverWait(self.driver, 20) \
                    .until(EC.visibility_of_all_elements_located((By.XPATH,
                                                                  f'/html/body/app-root/app-boletin-table/section/div'
                                                                  f'/div[{i}]/div/div/div[2]/table/tbody')))
                texto_columnas = self.driver.find_element(by=By.XPATH,
                                                          value=f'/html/body/app-root/app-boletin-table/section/div/div'
                                                                f'[{i}]/div/div/div[2]/table/tbody') \
                    .get_attribute('outerHTML')

                tabla = BeautifulSoup(texto_columnas, 'lxml')
                table_body = tabla.find('tbody')

                # Recorrido por cada fila de la tabla y actualización de listas que representan cada columna del
                # conjunto de datos
                for fila in table_body.find_all('tr'):
                    codigos.append(fila.find_all('td')[1].text)
                    productos.append(fila.find_all('td')[2].text)
                    presentaciones.append(fila.find_all('td')[3].text)
                    cantidades.append(fila.find_all('td')[4].text)
                    unidades.append(fila.find_all('td')[5].text)
                    extras.append(fila.find_all('td')[6].text)
                    primeras.append(fila.find_all('td')[7].text)
                    corrientes.append(fila.find_all('td')[8].text)

            # Creación del conjunto de datos
            datos = pd.DataFrame(data=
                                 {'fecha': self.fecha, 'codigos': codigos, 'producto': productos,
                                  'presentacion': presentaciones,
                                  'cantidad': cantidades, 'unidad': unidades, 'extra': extras, 'primera': primeras,
                                  'corriente': corrientes})
            datos['fecha'] = self.fecha
            return datos

        except:
            print(f'No se encontraron datos para la fecha {self.fecha}')
