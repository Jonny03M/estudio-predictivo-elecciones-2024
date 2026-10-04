import os
import pandas as pd
import spacy

def leer_archivo(ruta):
    df = pd.read_excel(ruta)
    datos = df['Texto']
    fecha = df['Fecha']    
    return datos,fecha
    
def tokenizar(datos):
    nlp = spacy.load('es_core_news_md')  # Indicamos el idioma (español)
    tokens_filtrados=[]
    for texto in datos:
        texto_tokens = nlp(texto)  # Convertir a tokens
        tokens = [token.lemma_ for token in texto_tokens if not (token.is_space or token.is_punct or token.like_num or (len(token.text) <= 3) or token.like_url or token.is_punct)]
        tokens_filtrados.append(' '.join(tokens))  # Unir tokens filtrados
    return tokens_filtrados
        
def guardar_excel(nombre_archivo,fecha,datos,tokens):
    resultados = pd.DataFrame({'Fecha': fecha,'Comentario': datos,'Tokens':tokens})
    resultados.to_excel(nombre_archivo,index=False)
    print("El archivo "+nombre_archivo +" se guardo correctamente")


#Guardar los datos de claudia
datos,fecha = leer_archivo(r"C:\Users\Admin\Desktop\Prediccion Elecciones 2024\Datos\Claudia_iniciales.xlsx")
tokens = tokenizar(datos)
guardar_excel("Claudia_Tokens.xlsx",fecha,datos,tokens)

#Guardar los datos de xochitl
datos,fecha = leer_archivo(r"C:\Users\Admin\Desktop\Prediccion Elecciones 2024\Datos\Xochitl_iniciales.xlsx")
tokens = tokenizar(datos)
guardar_excel("Xochitl_Tokens.xlsx",fecha,datos,tokens)