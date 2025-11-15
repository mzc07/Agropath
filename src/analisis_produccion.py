import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

def regresion_produccion():
    try:
        # Se intenta cargar el archivo CSV que contiene los datos de producción de soya.
        # Si no existe, se captura el error.
        dataset_soya = pd.read_csv(r'dataset\Soy.csv')
    except FileNotFoundError:
        print("Error: No se encontro el archivo.")
    else:
        # Filtrar solo las filas donde la columna "Attribute_Desc" sea "Total storage".
        # Esto limpia el dataset para quedarnos solo con la información relevante.
        dataset_soya = dataset_soya[dataset_soya["Attribute_Desc"] == "Total storage"]

        # La columna "Marketing_Year" tiene años en formato "YYYY/YY".
        # Se extrae el primer año, se convierte a entero y se usa como columna "Year".
        dataset_soya["Year"] = (
            dataset_soya["Marketing_Year"]
            .str.split("/")     # Separa por "/" 
            .str[0]             # Se toma la parte del año inicial
            .astype(int)        # Se convierte a número entero
        )

        # Agrupar por año y obtener el promedio de "Amount".
        # Esto construye un dataset anual resumido.
        dataset_soya_yearly = dataset_soya.groupby("Year", as_index=False)["Amount"].mean()

        # Convertir las cantidades a millones de "bushels"
        # Dividiendo entre 1000 para hacer la escala más legible.
        dataset_soya_yearly["Millions_bushels"] = dataset_soya_yearly["Amount"] / 1000

        # X es la variable independiente (año), y es la variable dependiente (producción).
        X = dataset_soya_yearly[["Year"]]               # Debe ser un DataFrame (2D)
        y = dataset_soya_yearly["Millions_bushels"]     # Serie (1D)

        # Crear el modelo de regresión lineal.
        modelo_regresion = LinearRegression()

        # Ajustar el modelo con los datos.
        modelo_regresion.fit(X, y)

        # Predecir los valores estimados por el modelo.
        y_pred = modelo_regresion.predict(X)

        # Graficar la recta de regresión.
        plt.plot(X, y_pred, color='blue')

        # Etiquetas de los ejes.
        plt.xlabel("Year")
        plt.ylabel("Millions_bushels")

        # Se desactiva la grilla para una visualización más limpia.
        plt.grid(False)

        # Graficar los puntos reales.
        plt.scatter(X, y)

        # Dibujar nuevamente la línea de regresión en rojo por encima de los puntos.
        plt.plot(X, y_pred, color='red')

        # Mostrar la gráfica final.
        plt.show()