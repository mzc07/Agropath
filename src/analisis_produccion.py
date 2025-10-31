import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

def regresion_produccion():
    dataset_soya = pd.read_csv(r'dataset\Soy.csv')
    dataset_soya = dataset_soya[dataset_soya["Attribute_Desc"] == "Total storage"]
    dataset_soya["Year"] = dataset_soya["Marketing_Year"].str.split("/").str[0].astype(int)
    dataset_soya_yearly = dataset_soya.groupby("Year", as_index=False)["Amount"].mean()
    dataset_soya_yearly["Millions_bushels"] = dataset_soya_yearly["Amount"] / 1000

    X = dataset_soya_yearly[["Year"]]
    y = dataset_soya_yearly["Millions_bushels"]

    modelo_regresion = LinearRegression()
    modelo_regresion.fit(X, y)

    # Predicción de la línea
    y_pred = modelo_regresion.predict(X)

    # Solo línea
    plt.plot(X, y_pred, color='blue')  # línea de regresión
    plt.xlabel("Year")
    plt.ylabel("Millions_bushels")
    plt.grid(False)
    plt.scatter(X, y)
    plt.plot(X, y_pred, color='red')
    plt.show()