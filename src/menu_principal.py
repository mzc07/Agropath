import os
import webbrowser
from analisis_produccion import regresion_produccion
from repositorio_abrir import abrir_repositorio

def limpiar_consola():
    os.system('cls' if os.name=='nt' else 'clear')

def menu_principal():

        print("=== Agropath - Menú Principal ===")
        print("1. Ver fincas de producción.")
        print("2. Ver centros de acopio.")
        print("3. Ver puertos.")
        print("4. Ver ruta mas cercana de las fincas al centro de acopio.")
        print("5. Ver ruta mas cercana del centro de acopio al puerto")
        print("6. Analisis de producción anual.")
        print("7. Ver repositorio de código.")
        print("0. Salir.")

if __name__ == "__main__":
    while True:
        limpiar_consola()
        menu_principal()
        try:
            entrada_usuario = int(input("Ingrese su opción: "))
        except ValueError:
            print("Error: Ingrese datos numericos.")
            print("Presione enter para continuar")
            continue
        except IndexError:
            print("Error: Entrada fuera del rango.")
            print("Presione enter para continuar")
            continue
        except KeyboardInterrupt:
            print("Error: Interrupcion del teclado.")
            break
        else:
            match entrada_usuario:
                case 1:
                    webbrowser.open_new(r'pages\index\mapa_fincas_illinois.html')
                case 2:
                    webbrowser.open_new(r'pages\index\centro_de_acopio.html')
                case 3:
                    webbrowser.open_new(r'pages\index\puerto_st_louis.html')
                case 4:
                    webbrowser.open_new(r'pages\index\rutas_fincas_centro.html')
                case 5:
                    webbrowser.open_new(r'pages\index\ruta_centro_puerto.html')
                case 6:
                    regresion_produccion()
                case 7:
                    abrir_repositorio()
                case 0:
                    break
                case _:
                    print("Error: Ingrese una opción valida.")