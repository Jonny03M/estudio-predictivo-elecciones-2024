import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Cargar el archivo Excel
rutaC = r"C:\Users\Admin\Desktop\Prediccion Elecciones 2024\Datos\resultados_Claudia.xlsx"
rutaX = r"C:\Users\Admin\Desktop\Prediccion Elecciones 2024\Datos\resultados_Xochitl.xlsx"

df = pd.read_excel(rutaX)

# Convertir la columna de fechas a tipo datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Filtrar los datos por sentimiento negativo y positivo
df_negativo = df[df['Sentimiento_por_NaiveBayes'] == 'negativo']
df_positivo = df[df['Sentimiento_por_NaiveBayes'] == 'positivo']

# Agrupar por fecha y sumar el sentimiento y promediar la probabilidad
df_negativo_agrupado = df_negativo.groupby('Fecha').agg({'Probabilidad_por_NaiveBayes': 'mean'}).reset_index()
df_positivo_agrupado = df_positivo.groupby('Fecha').agg({'Probabilidad_por_NaiveBayes': 'mean'}).reset_index()

# Ajustar un modelo de regresión lineal a los datos históricos de sentimiento negativo
X_negativo = np.arange(len(df_negativo_agrupado)).reshape(-1, 1)
y_negativo = df_negativo_agrupado['Probabilidad_por_NaiveBayes'].values
modelo_negativo = LinearRegression()
modelo_negativo.fit(X_negativo, y_negativo)

# Ajustar un modelo de regresión lineal a los datos históricos de sentimiento positivo
X_positivo = np.arange(len(df_positivo_agrupado)).reshape(-1, 1)
y_positivo = df_positivo_agrupado['Probabilidad_por_NaiveBayes'].values
modelo_positivo = LinearRegression()
modelo_positivo.fit(X_positivo, y_positivo)

# Predecir los próximos 20 días para sentimiento negativo
proximos_dias_negativo = pd.date_range(start=df_negativo_agrupado['Fecha'].iloc[-1] + pd.Timedelta(days=1), periods=20, freq='D')
proximos_indices_negativo = np.arange(len(df_negativo_agrupado), len(df_negativo_agrupado) + 20).reshape(-1, 1)
predicciones_negativo = modelo_negativo.predict(proximos_indices_negativo)
predicciones_df_negativo = pd.DataFrame({'Fecha': proximos_dias_negativo, 'prediccion_probabilidad_negativo': predicciones_negativo})

# Predecir los próximos 20 días para sentimiento positivo
proximos_dias_positivo = pd.date_range(start=df_positivo_agrupado['Fecha'].iloc[-1] + pd.Timedelta(days=1), periods=20, freq='D')
proximos_indices_positivo = np.arange(len(df_positivo_agrupado), len(df_positivo_agrupado) + 20).reshape(-1, 1)
predicciones_positivo = modelo_positivo.predict(proximos_indices_positivo)
predicciones_df_positivo = pd.DataFrame({'Fecha': proximos_dias_positivo, 'prediccion_probabilidad_positivo': predicciones_positivo})

# Graficar los datos históricos y las predicciones para sentimiento negativo
plt.figure(figsize=(10, 6))
plt.plot(df_negativo_agrupado['Fecha'], df_negativo_agrupado['Probabilidad_por_NaiveBayes'], label='Negativo - Datos Históricos', marker='o', color='red')
plt.plot(predicciones_df_negativo['Fecha'], predicciones_df_negativo['prediccion_probabilidad_negativo'], label='Negativo - Predicción', linestyle='--', marker='o', color='darkred')

# Graficar los datos históricos y las predicciones para sentimiento positivo
plt.plot(df_positivo_agrupado['Fecha'], df_positivo_agrupado['Probabilidad_por_NaiveBayes'], label='Positivo - Datos Históricos', marker='o', color='green')
plt.plot(predicciones_df_positivo['Fecha'], predicciones_df_positivo['prediccion_probabilidad_positivo'], label='Positivo - Predicción', linestyle='--', marker='o', color='darkgreen')

#plt.title('Predicción de Probabilidad por Sentimiento de Naive Bayes (Claudia Sheinbaum)')
plt.title('Predicción de Probabilidad por Sentimiento de Naive Bayes (Xochitl Gálvez)')
plt.xlabel('Fecha')
plt.ylabel('Probabilidad Promedio')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
