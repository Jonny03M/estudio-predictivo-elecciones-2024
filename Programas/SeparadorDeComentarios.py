import pandas as pd
from unidecode import unidecode 
import os
#--------------------------------------------------------------------------------------------------------------------
#-------------- IDENTIFICAMOS QUE COMENTARIOS NOS SIRVEN PARA PODER HACER EL ANALISIS ------------------------------- 
#--------------------------------------------------------------------------------------------------------------------
def verificar_palabras_clave(texto, lista1, lista2):
    palabras_xo = [palabra.lower() for palabra in lista1]
    palabras_cl = [palabra.lower() for palabra in lista2]
    
    encontrado_xo = any(palabra in texto for palabra in palabras_xo)
    encontrado_cl = any(palabra in texto for palabra in palabras_cl)
    
    if encontrado_xo and encontrado_cl:
        return "AMBOS"
    elif encontrado_xo:
        return "xochitl"
    elif encontrado_cl:
        return "claudia"
    else:
        return None                
#--------------------------------------------------------------------------------------
#------------------------------- PARTE PRINCIPAL ---------------------------------------
#--------------------------------------------------------------------------------------

#Lectura de nuestro archivo
ruta = r"C:\Users\Admin\Desktop\Prediccion Elecciones 2024\Datos\comentarios_iniciales.xlsx"
df = pd.read_excel(ruta)

# Crear un diccionario para almacenar los datos
datos = {}
for index, fila in df.iterrows():
    # Crear una lista para almacenar los valores de esta fila
    valores = [fila[columna] for columna in df.columns]
    # Asignar la lista de valores al identificador correspondiente en el diccionario
    datos[index] = valores

    
#Listas auxiliares para poder determianr a quien va dirigido el comentario 
xo = ["xochitl","zochitl", "xg", "prian","sochitl", "cochil","galvez","gelatina","gelatinas","debate","debates","botarga","xochitlovers","xochitlover","pri","pan","alito"]
cl = ["claudia","sheinbaum ", "shenbaun","4t","obrador","amlo","morena","plan c","cheinbaun","transformacion","4ta","2do piso","momia","hielo"]

#Diccionarios para almacenar comentario de xochitl y claudia
dic_clau={}
dic_xo={}
x=0 ; c=0

for i in range(len(datos)):    
    texto = datos[i][2]
    resultado = verificar_palabras_clave(texto, xo, cl)    
    if resultado:
        if resultado == "claudia":
            dic_clau[c] = [datos[i][0],datos[i][1],texto]
            c += 1            
        elif resultado == "xochitl":
            dic_xo[x] = [datos[i][0],datos[i][1],texto]
            x += 1
        else: 
            # Separar el texto en dos partes usando la palabra clave encontrada
            palabra_clave = [palabra for palabra in xo + cl if palabra in texto][0]
            indice_palabra = texto.index(palabra_clave)
            partes_texto = texto.split(palabra_clave, 1)
            c1 = partes_texto[0].strip() + " " + palabra_clave  # Primera parte del texto
            c2 = partes_texto[1].strip()  # Segunda parte del texto            
            
            # Verificar cada parte para determinar si pertenece a xochitl o claudia
            for comentario, indice in ((c1, c), (c2, x)):
                resultado = verificar_palabras_clave(comentario, xo, cl)
                if resultado == "claudia":
                    dic_clau[indice] = [datos[i][0],datos[i][1],comentario]
                    c += 1
                elif resultado == "xochitl":
                    dic_xo[indice] = [datos[i][0],datos[i][1],comentario]
                    x += 1        
                    
                    
#Pasar los diccionarios generados a un excel para Claudia
df = pd.DataFrame(dic_clau.values(), index=dic_clau.keys(), columns=['Usuario','Fecha', 'Texto']) 
nombre_archivo = 'Claudia_iniciales.xlsx'
df.to_excel(nombre_archivo, index_label='ID')
print(f'Se ha guardado el diccionario en el archivo "{nombre_archivo}"')

#Pasar los diccionarios generados a un excel para Xochitl
df = pd.DataFrame(dic_xo.values(), index=dic_xo.keys(), columns=['Usuario','Fecha', 'Texto']) 
nombre_archivo = 'Xochitl_iniciales.xlsx'
df.to_excel(nombre_archivo, index_label='ID')
print(f'Se ha guardado el diccionario en el archivo "{nombre_archivo}"')