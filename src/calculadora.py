# Calculadora de Costo Total de Soya al Centro de Acopio
COSTO_PRODUCCION_TON = 154.65


COSTO_COMBUSTIBLE_TON_KM = 0.01648  
FACTOR_OPERACIONAL_FIJO = 2.5       
FACTOR_VUELTA = 0.5                 


def calcular_costo_total_soya(distancia_ida_km):
    costo_combustible_ida = distancia_ida_km * COSTO_COMBUSTIBLE_TON_KM
    
    costo_combustible_vuelta = costo_combustible_ida * FACTOR_VUELTA
    
    costo_combustible_total = costo_combustible_ida + costo_combustible_vuelta
    
    costos_operacionales = costo_combustible_total * FACTOR_OPERACIONAL_FIJO
    
    costo_logistico_ton = costo_combustible_total + costos_operacionales
    
    
    costo_total_ton = COSTO_PRODUCCION_TON + costo_logistico_ton
    
    return costo_total_ton, costo_logistico_ton


def calcular_costos():
    print("--- Calculadora de Costo Total de Soya ---")
    try:
        distancia_input = input("Por favor, ingrese la distancia (en km) de la granja al acopio (solo ida): ")
        
        distancia_ida = float(distancia_input)
        
        if distancia_ida < 0:
            raise ValueError("La distancia no puede ser negativa.")

        costo_total, flete = calcular_costo_total_soya(distancia_ida)
        
        print("\n" + "="*40)
        print(f"Distancia ingresada: {distancia_ida:.2f} km")
        print(f"Costo de Producción (Fijo): ${COSTO_PRODUCCION_TON:.2f}/ton")
        print("-" * 40)
        print(f"Costo Logístico (Flete Total): ${flete:.2f}/ton")
        print(f" Costo TOTAL de la Soya al Acopio: ${costo_total:.2f}/ton")
        print("="*40)

    except ValueError as e:
        print(f"\nError de entrada: {e}. Por favor, ingrese un número válido para la distancia.")
    except Exception as e:
        print(f"\nOcurrió un error: {e}")