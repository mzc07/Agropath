import os
from fincas_produccion import ver_fincas
from analisis_produccion import regresion_produccion
from repositorio_abrir import abrir_repositorio
from centros_acopio import ver_centrosacopio

def limpiar_consola():
    os.system('cls' if os.name=='nt' else 'clear')

def menu_principal():

        print("=== Agropath - Menú Principal ===")
        print("1. Ver fincas de producción.")
        print("2. Ver centros de acopio.")
        print("3. Ver puertos.")
        print("4. Ver ruta mas cercana. ")
        print("5. Analisis de producción anual.")
        print("6. Ver repositorio de código.")
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
                    ver_fincas()
                case 2:
                    ver_centrosacopio()
                case 3:
                    None
                case 4:
                    None
                case 5:
                    regresion_produccion()
                case 6:
                    abrir_repositorio()
                case 0:
                    break
                case _:
                    print("Error: Ingrese una opción valida.")