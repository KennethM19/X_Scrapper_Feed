from selenium import webdriver
from selenium.webdriver.common.by import By

# Configurar el WebDriver (aquí se usa ChromeDriver, asegúrate de tenerlo instalado y en el PATH)
driver = webdriver.Chrome()

# Guardar el contenido HTML en un archivo temporal
html_content = '''
<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
<div>
    <div>
        <article>
            <span class="username">Kenneth</span>
            <div class="color">rojo</div>
            <div class="contenido"></div>
        </article>
    </div>
</div>
<div>
    <div>
        <article>
            <span class="username">Javier</span>
            <div class="color">azul</div>
        </article>
    </div>
</div>
<div>
    <div>
        <article>
            <span class="username">Pedro</span>
            <div class="contenido"></div>
        </article>
    </div>
</div>
<div>
    <div>
        <article>
            <span class="username">Alfredo</span>
            <span class="text"></span>
            <div class="color">amarillo</div>
        </article>
    </div>
</div>
</body>
</html>
'''

# Crear un archivo temporal con el contenido HTML
with open('temp.html', 'w') as file:
    file.write(html_content)

# Cargar el archivo HTML en el navegador
driver.get('D:/python/twitterScraper/X_Scrapper_Feed/temp.html')  # Reemplaza /absolute/path/to/temp.html con la ruta completa al archivo

# Encontrar todos los elementos <article>
articles = driver.find_elements(By.XPATH, '//article')

# Lista para almacenar los resultados
results = []

# Iterar sobre cada <article> y buscar el elemento específico dentro de él
for article in articles:
    try:
        username = article.find_element(By.XPATH, '//article//span[contains(@class, "username")]').text
        specific_element = article.find_element(By.XPATH, '//article//div[contains(@class, "color")]').text
        results.append(specific_element)  # Guardar el nombre de usuario
    except:
        results.append(None)

# Cerrar el WebDriver
driver.quit()

# Imprimir los resultados
print(results)
