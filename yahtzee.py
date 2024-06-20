import random

def lanzar_dados(num_dados, dados_bloqueados={}):
    resultados = []
    for i in range(num_dados):
        if i not in dados_bloqueados:
            probabilidad = random.random()
            if 0 <= probabilidad < 1/6:
                resultados.append(1)
            elif 1/6 <= probabilidad < 2/6:
                resultados.append(2)
            elif 2/6 <= probabilidad < 3/6:
                resultados.append(3)
            elif 3/6 <= probabilidad < 4/6:
                resultados.append(4)
            elif 4/6 <= probabilidad < 5/6:
                resultados.append(5)
            else:
                resultados.append(6)
        else:
            resultados.append(dados_bloqueados[i])
    return resultados

def calcular_puntuacion(resultados, categoria, puntuaciones,jugador):
    """Calcula la puntuación según la categoría elegida."""
    if categoria == "unos":
        return resultados.count(1) * 1
    elif categoria == "dos":
        return resultados.count(2) * 2
    elif categoria == "tres":
        return resultados.count(3) * 3
    elif categoria == "cuatros":
        return resultados.count(4) * 4
    elif categoria == "cincos":
        return resultados.count(5) * 5
    elif categoria == "seises":
        return resultados.count(6) * 6
    elif categoria == "full":
        valores = set(resultados)
        puntuacion = sum(resultados) if len(valores) == 2 and any(resultados.count(v) == 3 for v in valores) else 0
    elif categoria == "poker":
        puntuacion = sum(resultados) if any(resultados.count(v) >= 4 for v in set(resultados)) else 0
    elif categoria == "escalera":
        puntuacion = 30 if set(resultados) in [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}] else 0
    elif categoria == "grande":
        puntuacion = 40 if set(resultados) in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}] else 0
    elif categoria == "yahtzee":
        if len(set(resultados)) == 1:
            puntuacion_actual = puntuaciones[jugador].get("yahtzee", 0)
            if puntuacion_actual == 0:
                return 50
            else:
                return int(puntuacion_actual) + 100
        else:
            return 0
    elif categoria == "chance":
        puntuacion = sum(resultados)
    elif categoria == "trio":
        return sum(resultados) if any(resultados.count(v) >= 3 for v in set(resultados)) else 0
    else:
        puntuacion = 0

    return puntuacion

def mostrar_menu_categorias(puntuaciones):
    """Muestra un menú de categorías disponibles y permite al jugador elegir."""
    print("\nCategorías disponibles:")
    categorias = ["unos", "dos", "tres", "cuatros", "cincos", "seises", "trio", "full", "poker", "escalera", "grande", "yahtzee", "chance"]
    for i, categoria in enumerate(categorias):
        puntuacion = puntuaciones.get(categoria)
        if puntuacion == "-":
            puntuacion = 0
        print(f"{i+1}. {categoria}: {puntuacion}")

    while True:
        try:
            opcion = int(input("Elige una categoría (1-13): "))
            if 1 <= opcion <= 13:
                return categorias[opcion - 1]
            else:
                print("Opción inválida. Elige un número del 1 al 13.")
        except ValueError:
            print("Ingrese un número válido.")

def jugar_turno(jugador, puntuaciones):
    """Juega un turno completo para un jugador."""
    dados_bloqueados = {}

    for lanzamiento in range(3):
        print(f"\nLanzamiento {lanzamiento + 1}")
        resultados = lanzar_dados(5, dados_bloqueados)
        print("Resultados:", resultados)
        if lanzamiento < 2:
            dados_bloqueados_str = input("¿Qué dados quieres bloquear? (Ej: 1,3,5 o ninguno): ")
            dados_bloqueados = {int(x)-1: resultados[int(x)-1] for x in dados_bloqueados_str.split(',') if x}

    categoria = mostrar_menu_categorias(puntuaciones[jugador]) 

        while categoria == "yahtzee" and puntuaciones[jugador]["yahtzee"] != 0:
        print("Ya has llenado la categoría Yahtzee. Debes elegir otra categoría.")
        categoria = mostrar_menu_categorias(puntuaciones[jugador])

    puntuacion = calcular_puntuacion(resultados, categoria, puntuaciones, jugador)
    puntuaciones[jugador][categoria] = puntuacion  # Actualizar la puntuación de la categoría elegida

    if len(set(resultados)) == 1 and puntuaciones[jugador]["yahtzee"] != 0:  # Es un Yahtzee y ya se había anotado uno antes
        puntuaciones[jugador]["yahtzee"] += 100

    print(f"Puntuación obtenida: {puntuacion}")


def main():
    """Función principal del juego."""
    while True:
        try:
            num_jugadores = int(input("Ingrese el número de jugadores (2 o más): "))
            if num_jugadores >= 2:
                break
            else:
                print("Debe haber al menos 2 jugadores.")
        except ValueError:
            print("Ingrese un número válido.")

    puntuaciones = {}
    for i in range(num_jugadores):
        nombre_jugador = input(f"Ingrese el nombre del jugador {i+1}: ")
        puntuaciones[nombre_jugador] = {cat: 0 for cat in ["unos", "dos", "tres", "cuatros", "cincos", "seises", "trio", "full", "poker", "escalera", "grande", "yahtzee", "chance"]}  # Inicializar con 0

    for ronda in range(13):
        print(f"\nRonda {ronda + 1}")
        for jugador in puntuaciones.keys():
            print(f"\nTurno de {jugador}")
            jugar_turno(jugador, puntuaciones)

    # Mostrar resultados finales
    print("\nPuntuaciones finales:")
    for jugador, puntuacion in puntuaciones.items():
        total = sum(p for p in puntuacion.values() if p != "-")
        print(f"{jugador}: {total}")

if __name__ == "__main__":
    main()