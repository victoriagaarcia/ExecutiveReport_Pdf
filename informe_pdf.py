# Importamos las librerías necesarias 
from reportlab.pdfgen import canvas
import pandas as pd
import matplotlib.pyplot as plt

# Importamos esta librería de cosecha propia con funciones útiles para la realización del informe
# Es parte del análisis previo de los datos
import funciones_2016

# Llamando a informe.getAvailableFonts(), sacamos una lista con las posibles fuentes a elegir
# La fuente empleada en el documento será Times New Roman (también en negrita)

def portada_pdf(informe):
    # El parámetro 'informe' es un objeto de la librería Canvas

    # Colocamos el nombre de autor en la portada, de color gris
    informe.setFont('Times-Roman', 16)
    informe.setFillColorRGB(0.5, 0.5, 0.5)
    informe.drawString(180, 670, 'Victoria García Martínez-Echevarría')

    # Añadimos una imagen, la asociada al Maven Pizza Challenge
    informe.drawImage('pizzas_maven_image.jpg', 100, 300, width = 400, height = 350)

    # Se colocan los rótulos del título del informe
    informe.setFont('Times-Bold', 22)
    informe.setFillColorRGB(0.6, 0, 0) # Color ojo oscuro
    informe.drawString(187, 260, 'EXECUTIVE REPORT')
    informe.setFillColorRGB(0, 0.4, 0.2) # Color verde oscuro
    informe.setFontSize(20)
    informe.drawString(242, 232, 'Maven Pizzas')
    informe.setFillColorRGB(0.25, 0.25, 0.25) # Color gris oscuro
    informe.drawString(280, 205, '2016') # Se especifica el año en el que se basa el informe

    informe.showPage() # Se termina la página
    return

def introduccion(informe): 
    # Añadimos en primer lugar el heading principal
    informe.setFont('Times-Bold', 14)
    informe.setFillColorRGB(0.6, 0, 0) # Color rojo oscuro
    informe.drawString(198, 750, 'Informe de Rendimiento - 2016')

    # Creamos el subtítulo, que tendrá el mismo formato en las diferentes partes
    informe.setFont('Times-Bold', 12)
    informe.setFillColorRGB(0, 0.4, 0.2) # Color verde oscuro
    informe.drawString(80, 700, '0. Introducción')

    # Redactamos el párrafo introductorio del informe
    parrafo_intro = informe.beginText(80, 677)
    parrafo_intro.setFont('Times-Roman', 11)
    parrafo_intro.setFillColorRGB(0, 0, 0) # Color negro
    parrafo_intro.textLines("""En este informe se recoge información relevante acerca del rendimiento de la cadena de Pizzas 
    Maven durante el año 2016. Tras haber tratado los datos y realizado un análisis profundo sobre 
    ellos, se incluyen en este documento las gráficas que representan aspectos importantes a tener 
    en cuenta para el futuro y para realizar mejoras en el negocio. Entre estas, se adjunta una 
    recomendación de compra semanal de ingredientes basada en los pedidos de pizzas encargados 
    durante todo el año, la media de pizzas pedidas por semana de cada tipo, y una estimación de
    las ganancias obtenidas en 2016.""")
    informe.drawText(parrafo_intro) # Lo incluimos en el objeto de Canvas
    return

def recomendacion_ingredientes(informe, media_ingredientes): 
    # Establecemos el subtítulo de la sección
    informe.setFont('Times-Bold', 12)
    informe.setFillColorRGB(0, 0.4, 0.2) # Color verde oscuro
    informe.drawString(80, 533, '1. Compra semanal')

    # Explicamos que se incluye la recomendación semanal de ingredientes a comprar
    parrafo1 = informe.beginText(80, 510)
    parrafo1.setFont('Times-Roman', 11)
    parrafo1.setFillColorRGB(0, 0, 0) # Color negro
    parrafo1.textLines("""En la gráfica a continuación se muestra en un diagrama de barras la cantidad (en kilogramos) 
    de cada ingrediente que se recomienda comprar por semana tras realizar la media de cantidades 
    empleadas de cada uno en cada semana del año 2016. Se estima que una pizza pequeña, en 
    general, lleva 100 gramos de cada ingrediente. """)
    informe.drawText(parrafo1) # Lo incluimos en el objeto de Canvas

    # Pintamos un gráfico de barras con las cantidades de cada ingrediente, ordenadas de mayor a menor
    dataframe_ingredientes = pd.DataFrame([[clave, media_ingredientes[clave]] for clave in list(media_ingredientes.keys())], columns = ['Ingredientes', 'Cantidad (kg)']).sort_values(by = 'Cantidad (kg)', ascending = False)
    plt.bar(dataframe_ingredientes['Ingredientes'], dataframe_ingredientes['Cantidad (kg)'])
    plt.title('Compra semanal de ingredientes') # Título del gráfico
    plt.xticks(rotation = 90, fontsize = 5) # Cambiamos el tamaño y la rotación para que las etiquetas sean legibles
    plt.xlabel('Ingredientes') # Título del eje X
    plt.ylabel('Cantidades (kg)') # Título del eje Y
    plt.savefig('compra_ingredientes.png') # Guardamos la imagen en el directorio
    
    informe.drawImage('compra_ingredientes.png', 50, 135, width = 500, height = 310) # Añadimos la imagen del gráfico al pdf

    informe.showPage() # Se termina la página
    return

def pedidos_por_semana(informe, dataframe_conjunto):
    # Establecemos el subtítulo de la sección
    informe.setFont('Times-Bold', 12)
    informe.setFillColorRGB(0, 0.4, 0.2) # Color verde oscuro
    informe.drawString(80, 765, '3. Media de tipos de pizzas')

    # Explicamos que se incluye la media de cada tipo de pizza que se pide cada semana
    parrafo2 = informe.beginText(80, 742)
    parrafo2.setFont('Times-Roman', 11)
    parrafo2.setFillColorRGB(0, 0, 0) # Color negro
    parrafo2.textLines("""Para obtener una estimación de cuántas pizzas de cada tipo se piden cada semana, se muestra 
    a continuación un gráfico de sectores con la media de las que se pidieron en el año 2016. Para
    sacar estos datos, se ha sumado el número de veces que se pide cada tipo de pizza durante el 
    año entero y se ha dividido entre 53 semanas (a pesar de que un año tenga 52 semanas, la 
    primera semana de enero y la última de diciembre de 2016 comienzan a mitad de semana, por 
    lo que con este dataset consideramos 53 semanas para hacer los cálculos). """)
    informe.drawText(parrafo2) # Lo incluimos en el objeto de Canvas

    # Guardamos los recuentos y los tipos de pizza para poder pintar un gráfico de barras
    recuento = dataframe_conjunto['pizza_type_id'].value_counts()
    tipos_pizza = dataframe_conjunto['pizza_type_id'].unique().tolist()
    cuentas_pizzas = []
    for i in range(len(recuento)):
        cuentas_pizzas.append(recuento[tipos_pizza[i]]/53) # Dividimos por el número de semanas para obtener la media
    plt.clf() # Limpiamos los posibles restos de gráficos anteriores
    plt.pie(cuentas_pizzas, labels = tipos_pizza) # Pintamos el gráfico de sectores
    plt.title('Media semanal de cada tipo de pizza') # Título del gráfico
    plt.savefig('pizzas_sectores.png') # Guardamos la imagen en el directorio 

    informe.drawImage('pizzas_sectores.png', 120, 374, width = 350, height = 300) # Añadimos la imagen del gráfico al pdf
    return

def ingresos_semanales(informe, orders_byweek):
    # Establecemos el subtítulo de la sección
    informe.setFont('Times-Bold', 12)
    informe.setFillColorRGB(0, 0.4, 0.2) # Color verde oscuro
    informe.drawString(80, 352, '3. Ingresos por semana')

    # Explicamos que se incluyen los ingresos del año 2016 por semanas
    parrafo3 = informe.beginText(80, 329)
    parrafo3.setFont('Times-Roman', 11)
    parrafo3.setFillColorRGB(0, 0, 0) # Color negro
    parrafo3.textLines("""A continuación se muestra un gráfico de barras con los ingresos obtenidos cada semana del año 
    2016, considerando un precio específico para cada tipo de pizza y su respectivo tamaño. Los 
    ingresos están en dólares y las semanas, numeradas del 0 al 52. """)
    informe.drawText(parrafo3) # Lo incluimos en el objeto de Canvas

    # Pintamos un gráfico de barras con el ingreso obtenido cada semana
    precios = []
    for semana in orders_byweek: # Redondeamos el precio final a dos decimales para trabajar con números más sencillos
        precios.append(round(semana['price'].sum(), 2))
    dataframe_ingresos = pd.DataFrame([[i, precios[i]] for i in range(len(precios))], columns = ['Ingreso semanal', 'Semana'])
    plt.clf() # Limpiamos los posibles restos de gráficos anteriores
    plt.bar(dataframe_ingresos['Ingreso semanal'], dataframe_ingresos['Semana'])
    plt.title('Ingreso por semana - Año 2016') # Título del gráfico
    plt.xlabel('Semana') # Título del eje X
    plt.ylabel('Ganancia ($)') # Título del eje Y
    plt.savefig('ingresos.png') # Guardamos la imagen en el directorio

    informe.drawImage('ingresos.png', 125, 47, width = 350, height = 250) # Añadimos la imagen del gráfico al pdf

    informe.showPage() # Se termina la página
    return

if __name__ == '__main__':
    # Creamos el documento pdf con el objeto Canvas de la librería Canvas
    informe = canvas.Canvas('reporte_ejecutivo_pizzas.pdf', pagesize = (596, 840))
    portada_pdf(informe) # Creamos la portada con la función definida para ello
    introduccion(informe) # Creamos el párrafo introductorio

    # Trabajamos y amoldamos los datos con la librería de funciones 
    dataframes = funciones_2016.extract()
    dataframe_conjunto, orders_byweek = funciones_2016.fix_data(dataframes)
    media_ingredientes = funciones_2016.transform(dataframes, dataframe_conjunto, orders_byweek)
    
    # Creamos cada sección del informe, con su respectiva gráfica
    recomendacion_ingredientes(informe, media_ingredientes) 
    pedidos_por_semana(informe, dataframe_conjunto)
    ingresos_semanales(informe, orders_byweek)
    
    # Guardamos el documento, y se exporta el pdf al directorio actual
    informe.save()