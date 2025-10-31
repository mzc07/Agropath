from fincas_produccion import ver_fincas

def menu_principal():

        print("Agropath - Menú Principal")
        print("1. Ver fincas de producción.")
        print("2. Ver centros de acopio.")
        print("3. Ver puertos.")
        print("4. Ver ruta mas cercana. ")
        print("5. Analisis de producción anual.")
        print("5. Ver repositorio de código.")
        print("0. Salir.")

if __name__ == "__main__":
    menu_principal()
    try:
        entrada_usuario = int(input("Ingrese su opción: "))
    except ValueError:
        print("Error: Ingrese datos numericos.")
    except IndexError:
        print("Error: Entrada fuera del rango.")
    except KeyboardInterrupt:
        print("Error: Interrupcion del teclado.")
    else:
        match entrada_usuario:
            case 1:
                ver_fincas()
            case 2:
                None
            case 3:
                None
            case 4:
                None
            case 5:
                None
            case 0:
                None
            case _:
                print("Error: Ingrese una opción valida.")