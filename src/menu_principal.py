import os
import webbrowser
from fincas_de_produccion import fincas_de_produccion
from centro_de_acopio import centros_de_acopio
from puerto import puerto
from ruta_fincas_centro import generar_rutas
from ruta_centro_puerto import generar_ruta_cent
from analisis_produccion import regresion_produccion
from repositorio_abrir import abrir_repositorio
from calculadora import calcular_costos

# Función para limpiar la consola dependiendo del sistema operativo.
# En Windows usa 'cls', en Linux/Mac usa 'clear'.
def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función que imprime el menú principal.
# Se separa en una función para mantener el código organizado y reutilizable.
def menu_principal():
    print("=== Agropath - Menú Principal ===")
    print("1. Ver fincas de producción.")
    print("2. Ver centros de acopio.")
    print("3. Ver puertos.")
    print("4. Ver ruta mas cercana de las fincas al centro de acopio.")
    print("5. Ver ruta mas cercana del centro de acopio al puerto")
    print("6. Analisis de producción anual.")
    print("7. Ver pagina de analisis.")
    print("8. Calcular costos de logistica.")
    print("9. Ver repositorio de código.")
    print("0. Salir.")

# Punto de entrada del programa.
# Se ejecuta solo si el archivo es ejecutado directamente (no importado).
if __name__ == "__main__":
    while True:  # Ciclo principal del menú
        limpiar_consola()  # Limpia la pantalla en cada iteración
        menu_principal()   # Muestra las opciones disponibles

        try:
            # Se intenta convertir la entrada del usuario a entero
            entrada_usuario = int(input("Ingrese su opción: "))

        # Manejo de errores comunes:
        except ValueError:
            # Ocurre si el usuario ingresa letras u otros caracteres no numéricos
            print("Error: Ingrese datos numericos.")
            print("Presione enter para continuar")
            continue

        except IndexError:
            # No aplicaría normalmente aquí, pero se incluye como ejemplo de manejo
            print("Error: Entrada fuera del rango.")
            print("Presione enter para continuar")
            continue

        except KeyboardInterrupt:
            # Permite capturar Ctrl+C y salir de forma controlada
            print("Error: Interrupcion del teclado.")
            break

        else:
            # match-case (Python 3.10+) para evaluar la opción seleccionada
            match entrada_usuario:

                # Cada caso abre un archivo HTML o ejecuta una función específica.
                case 1:
                    try:
                        webbrowser.open_new(r'docs\mapa_fincas_illinois.html')
                    except Exception as error:
                        print(f'Error: {error}')
                        print("Generando archivo")
                        fincas_de_produccion()
                case 2:
                    try:
                        webbrowser.open_new(r'docs\centro_de_acopio.html')
                    except Exception as error:
                        print(f'Error: {error}')
                        print("Generando archivo")
                        centros_de_acopio()
                case 3:
                    try:
                        webbrowser.open_new(r'docs\puerto_st_louis.html')
                    except Exception as error:
                        print(f'Error: {error}')
                        print("Generando archivo")
                        puerto()
                case 4:
                    try:
                        webbrowser.open_new(r'docs\rutas_fincas_centro.html')
                    except Exception as error:
                        print(f'Error: {error}')
                        print("Generando archivo")
                        generar_rutas()
                case 5:
                    try:
                        webbrowser.open_new(r'docs\ruta_centro_puerto.html')
                    except Exception as error:
                        print(f'Error: {error}')
                        print("Generando archivo")
                        generar_ruta_cent()
                case 6:
                    # Llama a la función importada que realiza regresiones de producción
                    regresion_produccion()

                case 7:
                    # Abre documentación en HTML
                    webbrowser.open_new(r'docs\analisis.html')
                case 8:
                    calcular_costos()
                case 9:
                    # Abre el repositorio de código desde la función importada
                    abrir_repositorio()
                case 0:
                    # Opción para salir del programa
                    break
                case _:
                    # Cualquier valor fuera de las opciones válidas
                    print("Error: Ingrese una opción valida.")
            input("Presione Enter para continuar")
