from django.shortcuts import render
import json
import urllib.request
import platform
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import re  # Importación del módulo re para expresiones regulares
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

if platform.system() == "Windows":
    EUR = "EUR"
else:
    EUR = "€"

# Create your views here.



# Funciones de Home

def consultar(n):
    print(f"numero quellega {n}")
    n = str(n)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en segundo plano
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # WebDriver Manager para obtener ChromeDriver automáticamente
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
   
    
    try:
        # Formar la URL dinámica con el número `n`
        url = f"https://www.elperiodico.com/es/loteria-navidad/comprobar-numero-{n}/"
        
        # Cargar la página
        driver.get(url)
        
        # Esperar un breve tiempo para asegurar que el contenido se cargue (opcional, ajusta si es necesario)
        driver.implicitly_wait(10)
        
        # Obtener el HTML renderizado
        html = driver.page_source
        
        # Parsear el HTML con BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        div_pedrea = soup.find('div', class_='lottery-pedrea')
        if div_pedrea:
        # Buscar el párrafo con la clase "lottery lottery-paragraph"
            premio_span = div_pedrea.find('p', class_='lottery-paragraph')
            print(f"premsiospan numero {n} cib orenui {premio_span}")
        
            if premio_span:
            # Extraer el texto del párrafo y buscar el premio con regex
                texto_premio = premio_span.text.strip()
                print( texto_premio )
                match = re.search(r"Has ganado (\d+)€!", texto_premio)
                print(match)
                if match:
                # Extraer el valor del premio
                    premio = int(match.group(1))
                    print(f"El número {n} ha sido premiado con {premio} euros.")
                    
                    return float(premio)
                else:
                    print(f"No se encontró información de premio para el número {n}.")
                    return 0
            else:
                print(f"No se encontró el elemento con la clase 'lottery lottery-paragraph'.")
                return 0
    except Exception as e:
        print(f"Error al consultar la URL para el número {n}: {e}")
        return 0
    finally:
        # Cerrar el navegador
        driver.quit()

def consultarnumero(n):
    '''file_path = os.path.join(settings.STATICFILES_DIRS[0], "LoteriaNavidadResumen.json")
    with open(file_path, 'r', encoding='utf-8') as file:
        contenido = file.read()
        datos = json.loads(contenido)
   Este bloque es para la url'''
    url_elpais = "https://api-loteria.pabloclementeperez.com/output/LoteriaNavidadResumen.json"
    respuesta = urllib.request.urlopen(url_elpais)
    contenido = respuesta.read()
    datos = json.loads(contenido.decode("utf8").replace("busqueda=", ""))
    valores = [value for key, value in datos.items() if key.startswith("numero")]
    if n in valores:
      premio = 20
      print(f"esta {n}")
    else:
      premio = 0
      print(f"No esta {n}")
    
    
    #premio = float(datos["premio"])
    #premio = 0
    lista_premios = {'numero':n, 'premio':premio }
    return lista_premios

def estado_sorteo():
    url_elpais = "https://api-loteria.pabloclementeperez.com/output/LoteriaNavidadResumen.json"
    respuesta = urllib.request.urlopen(url_elpais)
    contenido = respuesta.read()
    datos = json.loads(contenido.decode("utf8").replace("premios=", ""))
    '''datos = {'timestamp':1292608331,'status':1,'numero1':45110,'numero2':45110,'numero3':45110,'numero4':45110,
'numero5':45110,'numero6':45110,'numero7':45110,'numero8':45110,'numero9':45110,'numero10':45110,'numero11':45110,
'numero12':45110,'numero13':45110,'fraseSorteoPDF':'','fraseListaPDF':'','listaPDF':'','urlAudio':'','error':0}'''
    status = datos["status"]
    estado = None
    if status == 0:
        estado = "El sorteo no ha comenzado."
    elif status == 1:
        estado = "El sorteo ha empezado. Lista de premios parcial."
    elif status == 2:
        estado = "Sorteo terminado. Lista de premios provisional."
    elif status == 3:
        estado = "Sorteo terminado. Lista de premios semioficial."
    elif status == 4:
        estado = "Sorteo terminado. Lista de premios oficial."
    numero1 = datos["numero1"]
    numero2 = datos["numero2"]
    numero3 = datos["numero3"]
    numero4 = datos["numero4"]
    numero5 = datos["numero5"]
    numero6 = datos["numero6"]
    numero7 = datos["numero7"]
    numero8 = datos["numero8"]
    numero9 = datos["numero9"]
    numero10 = datos["numero10"]
    numero11 = datos["numero11"]
    numero12 = datos["numero12"]
    numero13 = datos["numero13"]
    return [estado, numero1, numero2,numero3,numero4,numero5,numero6,numero7,numero8,numero9,numero10,numero11,numero12,numero13]


def predrea():
    # Configuración de Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Ejecutar en segundo plano
    driver = webdriver.Chrome(options=options)  # Asegúrate de tener el ChromeDriver instalado
        
# URL de la página
    url = "https://www.elperiodico.com/es/loteria-navidad/lista-pedrea/lista-completa-pedreas/"
    driver.get(url)

# Esperar a que se cargue el contenido dinámico (ajusta el tiempo si es necesario)
    driver.implicitly_wait(10)  # Espera hasta 10 segundos para cargar los elementos

# Obtener el HTML renderizado
    html = driver.page_source
    driver.quit()  # Cerrar el navegador

# Parsear el HTML con BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

# Buscar el ul con id "winner-numbers"
    ul = soup.find('ul', id='winner-numbers')
    if ul:
        # Inicializar un diccionario para almacenar los datos
        data = {}

        # Iterar sobre todos los li dentro del ul
        for li in ul.find_all('li'):
            # Buscar el span con clase 'numero' y 'premio'
            numero_span = li.find('span', class_='numero')
            premio_span = li.find('span', class_='premio')

            if numero_span and premio_span:
                # Extraer el texto y limpiar el valor del premio
                numero = numero_span.text.strip()
                premio = premio_span.text.strip().replace('€', '')
                # Agregar al diccionario
                data[numero] = premio

        # Convertir el diccionario en JSON
        json_data = json.dumps(data, indent=4, ensure_ascii=False)

        # Mostrar el JSON resultante
        #print(json_data)
        
        # Guardar en un archivo JSON
        with open('pedreas.json', 'w', encoding='utf-8') as file:
            file.write(json_data)
    else:
        print("No se encontró el ul con id 'winner-numbers'.")
    return json_data
    
    

def checknumeros():
    
    with open(os.path.join(settings.MEDIA_ROOT, 'mis_numeros.txt')) as file:
        lineas = file.readlines()
        contenido = ''.join(lineas)
    #fichero_jugados = open(os.path.join(settings.MEDIA_ROOT, 'mis_numeros.txt'), 'r').read()
    #fichero_jugados = open(settings.MEDIA_ROOT, 'mis_numeros.txt', "r").read()
    mis_premios = {}
    print(f"misnuemero {mis_premios}")
    total_ganado = 0.0
    total_jugado = 0.0
    for elemento in lineas:
        numero, jugado = elemento.split(":")
        jugado =  jugado.rstrip("\n")
        num = str(numero)
        print(f"mis nuemero {num}")
        
        ganado_decimo = consultar(num)
        mi_premio = {}
        he_ganado = max(float(jugado) * float(ganado_decimo) / 20, 0)
        total_ganado += he_ganado
        total_jugado += float(jugado)
        mi_premio = {'numero_jugado': numero, 'cantidad_jugada': jugado, 'premio': int(ganado_decimo), 'premioxdecimo': int(he_ganado) , 'total_ganado': total_ganado, 'total_jugado':total_jugado}
        mis_premios[numero] = mi_premio


        
    return mis_premios
        

    if platform.system() == "Windows":
        input()
           


# Fin de funciones de HOME

def home(request):
    
    estadosorteo = estado_sorteo()
    misnumeros = checknumeros()
    sort = estadosorteo[0]
    numero1 =  estadosorteo[1]
    numero2 = estadosorteo[2]
    numero3 = estadosorteo[3]
    numero4 = estadosorteo[4]
    numero5 = estadosorteo[5]
    numero6 = estadosorteo[6]
    numero7 = estadosorteo[7]
    numero8 = estadosorteo[8]
    numero9 = estadosorteo[9]
    numero10 = estadosorteo[10]
    numero11 = estadosorteo[11]
    numero12 = estadosorteo[12]
    numero13 = estadosorteo[13]
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje', '')
        resultado = consultarnumero(mensaje)
        elpremio = resultado['premio']
        contenido_premio = f'<p class="text-muted mb-0 btn-success rounded-3 p-2 textoblancobr text-center" style="font-weight: 700; color: yellow!important;">PREMIADO con {elpremio}€</p>'
        contenido_nopremio = '<p class="text-muted mb-0 btn-warning m-1 rounded-3 textoblancobr p-2 text-center" style="font-weight: 700; color: #000000!important;">No premiado</p>'
        imagen_premio = f'<img src="{ settings.STATIC_URL+"images/loteria-premio.png"}" style="width: 45px; height: 45px" class="rounded-circle"/>'
        imagen_nopremio = f'<img src="{ settings.STATIC_URL+"images/loteria-no-premio.png"}" style="width: 45px; height: 45px" class="rounded-circle"/>'
        return HttpResponse(f""" <div class="col-md-12">
                                 <div class="card">
                                 <div class="card-body">
                                 <div class="d-flex align-items-center">
                                    {''.join([
                                         f'{imagen_premio}' if resultado['premio'] > 0 else f'<p>{imagen_nopremio}</p>'
                                        ])}
                                     <div class="ms-1 col-md-10">
                                        
                                        <p class="fw-bold mb-1 text-center">Numero:   {resultado['numero']} | Premio:  {resultado['premio']}€</p>
                                        {''.join([
                                         f'{contenido_premio}' if resultado['premio'] > 0 else f'<p>{contenido_nopremio}</p>'
                                        ])}
                                             
                                        
                                            
					                    
                                    </div>
                                    </div>
                                </div>
                                </div>
                            </div>""")
    return render(request,
                  'index.html',
                  context={'matrix': misnumeros, 'estado': sort, 'primero': numero1, 'segundo': numero2, 'tercero':numero3, 'cuartouno':numero4, 
                           'cuartodos':numero5, 'quintouno':numero6,'quintodos':numero7, 'quintotres':numero8,
                           'quintocuatro':numero9,'quintocinco':numero10,'quintoseis':numero11,'quintosiete':numero12,
                           'quintoocho':numero13,})
    
    
def index(request):
    return render(request,
                  'index.html',
                  context={'primero': 00000, 'segundo':00000, 'tercero':00000, 'cuartouno':00000, 
                           'cuartodos':00000, 'quintouno':00000,'quintodos':00000, 'quintotres':00000,
                           'quintocuatro':00000,'quintocinco':00000,'quintoseis':00000,'quintosiete':00000,
                           'quintoocho':00000,})
    
def register (request):
    if request.method == "GET":
        #TODO Pasar formulario a la plantilla de registro
        pass
    elif request.method == "POST":
        #TODO Guardar el usuario siguiendo el formulario
        pass