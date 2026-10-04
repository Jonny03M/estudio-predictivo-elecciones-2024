import pandas as pd
import spacy
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Definir la lista de palabras a eliminar
palabras_a_eliminar = ["claudia","sheinbaum ", "shenbaun","4t","obrador","amlo","morena","plan c","cheinbaun","transformacion","4ta","2do piso","vato","maynez"
    "xochitl","zochitl", "xg", "prian","sochitl", "cochil","galvez","gelatina","gelatinas","debate","debates","botarga","xochitlovers","xochitlover","pri","pan","alito"]

def eliminar_palabras(texto):
    # Verificar si el valor es un string
    if isinstance(texto, str):
        palabras = texto.split()
        palabras_filtradas = [palabra for palabra in palabras if palabra.lower() not in palabras_a_eliminar]
        return ' '.join(palabras_filtradas)
    else:
        # Si no es un string, retornar el mismo valor
        return texto
ruta1 = r"C:\Users\Admin\Desktop\Prediccion Elecciones 2024\Datos\train_data.xlsx"
ruta2 = r"C:\Users\Admin\Desktop\Prediccion Elecciones 2024\Datos\Claudia_Tokens.xlsx" #Cargar datos para poder entrenar
df = pd.read_excel(ruta1)
df2 = pd.read_excel(ruta2)

# Eliminar filas con NaN en la columna 'Tokens'
df = df.dropna(subset=['Tokens'])
# Verificar si hay documentos que no sean cadenas de texto después de eliminar NaN
df2 = df2[df2['Tokens'].apply(lambda x: isinstance(x, str))]

# Verificar si hay documentos vacíos
df2 = df2[df2['Tokens'].apply(lambda x: len(x.strip()) > 0)]

# Convertir el campo 'Fecha' a formato de fecha especificando dayfirst=True
df2['Fecha'] = pd.to_datetime(df2['Fecha'], dayfirst=True)

# Extraer solo la parte de la fecha y eliminar la parte de la hora
df2['Fecha'] = df2['Fecha'].dt.date

# Ordenar el DataFrame por la columna 'Fecha' de manera descendente
df2 = df2.sort_values(by='Fecha', ascending=True)

df3 = df2.iloc[:, 2].apply(eliminar_palabras)
# Vectorizacion de caracteristicas
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['Tokens'])
y = df['Sentimiento_Predicho']

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamiento del modelo SVM
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

# Evaluación del modelo SVM
y_pred = svm_model.predict(X_test)
print("Resultados del modelo SVM")
print(classification_report(y_test, y_pred, zero_division=1))

# Predicción de sentimientos para nuevos textos con SVM
new_texts_vectorized = vectorizer.transform(df3)
predictions = svm_model.predict(new_texts_vectorized)

# Entrenamiento y predicciones con el modelo Naive Bayes
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)
predictions_nb = nb_model.predict(new_texts_vectorized)
proba_predictions_nb = nb_model.predict_proba(new_texts_vectorized) #Prob de que pertenezca a su clase
# Imprimir la forma de proba_predictions_nb
print(proba_predictions_nb.shape)

# Calculando las probabilidades para cada clase
probabilities = nb_model.predict_proba(new_texts_vectorized)

# Probabilidad de ser positivo
prob_pos = probabilities[:, 1]  # Tomando la columna de probabilidad de clase positiva

# Probabilidad de ser negativo
prob_neg = probabilities[:, 0]  # Tomando la columna de probabilidad de clase negativa

# Probabilidad de ser neutro (si es necesario)
prob_neutral = 1 - (prob_pos + prob_neg)

if len(prob_neutral) != len(df2):
    print("Error: La longitud de prob_neutral no coincide con la longitud de df2")
    exit()
else:
    print("Todo bien")
# Crear un DataFrame para almacenar los resultados
results_df = pd.DataFrame()

# Copiar las columnas 'Fecha' y 'Comentario' de df2 al nuevo DataFrame
results_df['Fecha'] = df2['Fecha']
results_df['Comentario'] = df2['Comentario']
results_df['Token_filtrado'] = df2['Tokens']

# Agregar las predicciones y probabilidades de ambos modelos al DataFrame
results_df['Sentimiento_Predicho_SVC'] = predictions
results_df['Sentimiento_por_NaiveBayes'] = predictions_nb
results_df['Probabilidad'] = np.max(proba_predictions_nb, axis=1)

# Reiniciar los índices de results_df
results_df.reset_index(drop=True, inplace=True)

# Crear una lista para almacenar las probabilidades calculadas
probabilities_nb = []

# Iterar a través de las filas del DataFrame
for index, row in results_df.iterrows():
    sentiment = row['Sentimiento_por_NaiveBayes']
    
    if sentiment == 'Positivo':
        probabilities_nb.append(proba_predictions_nb[index, 1])  # Probabilidad de ser positivo
    elif sentiment == 'Negativo':
        probabilities_nb.append(proba_predictions_nb[index, 0])  # Probabilidad de ser negativo
    else:
        probabilities_nb.append(proba_predictions_nb[index, 2])  # Probabilidad de ser neutro

# Agregar la lista de probabilidades al DataFrame como una nueva columna
results_df['Probabilidad_por_NaiveBayes'] = probabilities_nb

# Obtener las palabras asociadas por Naive Bayes
palabras_asociadas_nb = []

# Convertir la representación vectorizada de los nuevos textos de vuelta a texto
new_texts = vectorizer.inverse_transform(new_texts_vectorized)

# Iterar a través de las filas del DataFrame
for index, _ in results_df.iterrows():
    # Obtener las palabras asociadas al comentario
    palabras_asociadas = new_texts[index]

    # Si hay palabras asociadas, tomar la primera (asumimos que solo hay una)
    if len(palabras_asociadas) > 0:
        palabra_asociada = palabras_asociadas[0]
    else:
        palabra_asociada = ""

    # Agregar la palabra asociada a la lista
    palabras_asociadas_nb.append(palabra_asociada)

# Agregar la lista de palabras asociadas al DataFrame como una nueva columna
results_df['Palabra_Asociada_por_NaiveBayes'] = palabras_asociadas_nb


# Guardar el DataFrame en un archivo Excel
results_df.to_excel("resultados_Claudia.xlsx", index=False)

print("Resultados guardados en resultados_Claudia.xlsx")