import pandas as pd
import os

# Función para obtener etiqueta de sentimiento
def obtener_etiqueta_sentimiento(token):
    if isinstance(token, float) and pd.isna(token):  # Verificar si el valor es NaN
        return "neutro"
    positivos = 0
    negativos = 0    
    for palabra in token.split():
        if palabra in palabras_sentimiento:
            if palabras_sentimiento[palabra] == "positivo":
                positivos += 1
            elif palabras_sentimiento[palabra] == "negativo":
                negativos += 1
                
    if positivos > negativos:
        return "positivo"
    elif negativos > positivos:
        return "negativo"
    else:
        return "neutro"

# Cargar datos y definir diccionario de sentimientos
palabras_sentimiento = {
    #Palabras Positivas
    "apoyar": "positivo", "presidenta": "positivo", "ir": "positivo", "abogar": "positivo", "alinear": "positivo", "bravo": "positivo",
    "presidente": "positivo", "excelente": "positivo", "progresar": "positivo", "votar": "positivo", "avalar": "positivo",
    "felicitar": "positivo", "capaz": "positivo", "honestidad": "positivo","calidad": "positivo", "elegir": "positivo", "arriba": "positivo",
    "ganar": "positivo", "mucho": "positivo","respaldar": "positivo", "felicidad": "positivo", "alegria": "positivo", "mejor": "positivo",
    "favorita": "positivo", "bien": "positivo", "ganar": "positivo", "felicidad": "positivo", "favorecer": "positivo", "efectivo": "positivo",
    "respeto": "positivo", "admirar": "positivo", "confiar": "positivo", "confianza": "positivo", "amar": "positivo", "primera": "positivo",
    "celebrar": "positivo","valorar": "positivo", "elogiar": "positivo", "inspirar": "positivo", "impulsar": "positivo","motivar": "positivo",
    "enriquecer": "positivo","empoderar": "positivo","promover": "positivo","libertad": "positivo", "democracia": "positivo",
    "increible": "positivo","genial": "positivo","fabuloso": "positivo","notable": "positivo","estupendo": "positivo", "seguir": "positivo",
    "continuar": "positivo","transformar": "positivo","sobresalir": "positivo","crear": "positivo","confirmar": "positivo", 
    "construir": "positivo","seguridad": "positivo","adelante": "positivo","victoria": "positivo","viva": "positivo","garantizar": "positivo",
    "ayudar": "positivo","estar": "positivo","dedicar": "positivo","chingon": "positivo","fregon": "positivo","corazon": "positivo",
    #Palabras negativas 
    "talones": "negativo", "perder": "negativo", "pendejo": "negativo", "pendeja": "negativo", "terror": "negativo", "corrupcion":"negativo",
    "desesperar": "negativo", "fallar": "negativo", "reir": "negativo", "loco": "negativo","idiota": "negativo", "condenar": "negativo",
    "rata": "negativo", "robar": "negativo", "vender": "negativo", "pasado": "negativo", "pobre": "negativo", "rechazar": "negativo",
    "arrastrada": "negativo", "ignorante": "positivo", "verguenza": "negativo", "bote": "negativo", "carcel": "negativo", "sarcasmo": "negativo",
    "narco": "negativo", "mentir": "negativo", "perder": "negativo", "culero": "negativo","sarcasmo": "negativo", "desacreditar": "negativo",
    "incompetente": "negativo","deshonesto": "negativo","engañar": "negativo","inepto": "negativo","irresponsable": "negativo",
    "desleal": "negativo","tramposo": "negativo","ineficiente": "negativo","manipulador": "negativo","sucio": "negativo", "ratero": "negativo",
    "ultima": "negativo","lejos": "negativo","mal": "negativo","peor": "negativo","desafortunado": "negativo", "hielo": "negativo",
    "botarga": "negativo", "abajo": "negativo", "fuera": "negativo", "imbecil": "negativo", "tarado": "negativo", "lamentar": "negativo",
    "arrepentir": "negativo", "verdulera": "negativo", "anciana": "negativo", "vieja": "negativo", "bruja": "negativo", "chencha": "negativo",
    "floja": "negativo", "peligro": "negativo", "dañar": "negativo", "botarga": "negativo", "muerte": "negativo", "agresion": "negativo",
    "atras": "negativo","abandonar": "negativo","rabia": "negativo","tristeza": "negativo","depresion": "negativo","derrotar": "negativo",
    "traicion": "positivo","momia": "positivo", "hielo": "positivo",
}

ruta = r"C:\Users\Admin\Desktop\Prediccion Elecciones 2024\Datos\Datos_Entrenamiento.xlsx"
df = pd.read_excel(ruta)  
etiquetas = [obtener_etiqueta_sentimiento(token) for token in df['Tokens']] # Obtener etiquetas de sentimiento para cada comentario
df['Sentimiento_Predicho'] = etiquetas # Añadir las etiquetas al DataFrame
df.to_excel("train_data.xlsx", index=False)
