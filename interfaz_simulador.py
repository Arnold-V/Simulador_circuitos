import tkinter as tk
import numpy as np


def crear_matriz_ceros(n):
    matriz = []
    for _ in range(n):
        fila = [0] * n
        matriz.append(fila)
    return matriz

class Componente:

    def __init__(self, nombre, valor, x, y):
        self.nombre = nombre
        self.valor = valor
        self.x = x
        self.y = y
        self.w = 6.2831 * 60
        self.nodo_a = 0
        self.nodo_b = 0

        if self.nombre[0] == 'l':
            self.valor_complejo = self.w * float(self.valor)
        elif self.nombre[0] == 'c':
            self.valor_complejo = (-1) / (float(self.valor) * self.w)
        else:
            self.valor_complejo = 0


class Nodos:
    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.conexiones = []
        self.x = x
        self.y = y
        self.nodo_comun = False
        self.conexiones_nodo_comun = []


class Conexion:

    def __init__(self, componente1, componente2):
        self.componente1 = componente1
        self.componente2 = componente2

        if componente1.nombre[0] == 'n':
            componente1.conexiones.append(componente2.nombre)
        else:
            componente2.conexiones.append(componente1.nombre)

        if (componente1.nombre[0] == 'n' and componente2.nombre[0] != 'n') or (componente2.nombre[0] == 'n' and componente1.nombre[0] != 'n'):
            if componente1.nombre[0] == 'n':
                if componente2.nodo_a == 0:
                    componente2.nodo_a = componente1.nombre
                else:
                    componente2.nodo_b = componente1.nombre

            else:
                if componente1.nodo_a == 0:
                    componente1.nodo_a = componente2.nombre
                else:
                    componente1.nodo_b = componente2.nombre




class Circuito:

    def __init__(self):

        self.componentes = []
        self.nodos = []
        self.conexiones = []

    def agregar_componente(self):

        lista_componentes_predefinida = ['f', 'r', 'c', 'l', 'n']
        nombre = nombre_entry.get()
        valor = valor_entry.get()
        temp = False

        for componente in self.componentes:
            if componente.nombre == nombre:
                temp = True
            else:
                temp = False
        if not temp:

            if nombre[0] in lista_componentes_predefinida:

                if nombre[0] == 'n':
                    nodo = Nodos(nombre, 50, 50)
                    self.nodos.append(nodo)
                    self.componentes.append(nodo)
                    self.dibujar_componentes()
                    self.actualizar_lista()
                    return True
                else:
                    componente = Componente(nombre, valor, 50, 50)
                    self.componentes.append(componente)
                    self.actualizar_lista()
                    self.dibujar_componentes()
                    return True

            else:
                return False
        else:
            print('El componente ya existe')

    def dibujar_componentes(self):

        canvas.delete("componentes")

        for componente in self.componentes:
            if componente.nombre[0] == 'r':
                canvas.create_rectangle(componente.x - 20, componente.y - 10, componente.x + 20, componente.y + 10,
                                        fill="lightblue", tags="componentes")
            elif componente.nombre[0] == 'c':
                canvas.create_rectangle(componente.x - 20, componente.y - 10, componente.x + 20, componente.y + 10,
                                        fill="lightgreen", tags="componentes")
            elif componente.nombre[0] == 'l':
                canvas.create_rectangle(componente.x - 20, componente.y - 10, componente.x + 20, componente.y + 10,
                                        fill="orange", tags="componentes")

            elif componente.nombre[0] == 'f':
                canvas.create_oval(componente.x - 20, componente.y - 20, componente.x + 20, componente.y + 20,
                                   fill="yellow", tags="componentes")

            elif componente.nombre[0] == 'n':
                canvas.create_oval(componente.x - 4, componente.y - 4, componente.x + 4, componente.y + 4, fill="black",
                                   tags="componentes")
            else:
                # Si el tipo de componente no es reconocido, se dibuja un rectángulo por defecto
                canvas.create_rectangle(componente.x - 20, componente.y - 20, componente.x + 20, componente.y + 20,
                                        fill="lightgray", tags="componentes")

            if componente.nombre[0] == 'n':
                canvas.create_text(componente.x, componente.y - 20, text=componente.nombre, tags="componentes")
            else:
                canvas.create_text(componente.x, componente.y, text=componente.nombre, tags="componentes")

    def dibujar_topologia(self):
        canvas.delete("lineas")
        for nodo in self.nodos:
            for i in range(len(nodo.conexiones)):
                componente_buscado = None
                for componente in self.componentes:
                    if componente.nombre == nodo.conexiones[i]:
                        componente_buscado = componente

                canvas.create_line(nodo.x, nodo.y, componente_buscado.x, componente_buscado.y, tags="lineas")

    def actualizar_lista(self):

        lista_componentes.delete(0, tk.END)
        for componente in self.componentes:
            if componente.nombre[0] == 'n':
                lista_componentes.insert(tk.END, f"{componente.nombre}: {0}")
            else:
                lista_componentes.insert(tk.END, f"{componente.nombre}: {componente.valor}")

    def seleccionar_componente(self, event):
        index = lista_componentes.nearest(event.y)
        if event.state == 4:  # Si la tecla Ctrl está presionada
            elementos_seleccionados.append(index)
        else:
            elementos_seleccionados.clear()
            elementos_seleccionados.append(index)

    def conectar_componentes(self):

        if len(elementos_seleccionados) == 2:
            componente1_index, componente2_index = elementos_seleccionados
            componente1 = self.componentes[componente1_index]
            componente2 = self.componentes[componente2_index]

            if componente1.nombre[0] == 'n':
                if componente2.nombre in componente1.conexiones:
                    print('conexion ya existe')
                else:
                    conexion = Conexion(componente1, componente2)
            else:
                if componente1.nombre in componente2.conexiones:
                    print('conexion ya existe')
                else:
                    conexion = Conexion(componente1, componente2)

            if componente1.nombre[0] == 'n' and componente2.nombre[0] == 'n':

                if componente1.nombre == 'nf':
                    for nombre_componente in componente2.conexiones:
                        if nombre_componente in componente1.conexiones:
                            pass
                        else:
                            componente1.conexiones_nodo_comun.append(nombre_componente)

                    for nombre_componente_comun in componente2.conexiones_nodo_comun:
                        if nombre_componente_comun in componente1.conexiones:
                            pass
                        else:
                            componente1.conexiones_nodo_comun.append(nombre_componente_comun)
                    componente2.nodo_comun = True
                elif componente2.nombre == 'nf':
                    for nombre_componente in componente1.conexiones:
                        if nombre_componente in componente2.conexiones:
                            pass
                        else:
                            componente2.conexiones_nodo_comun.append(nombre_componente)

                    for nombre_componente_comun in componente1.conexiones_nodo_comun:
                        if nombre_componente_comun in componente2.conexiones:
                            pass
                        else:
                            componente2.conexiones_nodo_comun.append(nombre_componente_comun)

                    componente1.nodo_comun = True

                else:
                    for nombre_componente in componente1.conexiones:
                        if nombre_componente in componente2.conexiones:
                            pass
                        else:
                            componente2.conexiones_nodo_comun.append(nombre_componente)
                    for nombre_componente in componente2.conexiones:
                        if nombre_componente in componente1.conexiones:
                            pass
                        else:
                            componente1.conexiones_nodo_comun.append(nombre_componente)

                    for nombre_componente_comun in componente1.conexiones_nodo_comun:
                        if nombre_componente_comun in componente2.conexiones:
                            pass
                        else:
                            componente2.conexiones_nodo_comun.append(nombre_componente_comun)

                    for nombre_componente_comun in componente2.conexiones_nodo_comun:
                        if nombre_componente_comun in componente1.conexiones:
                            pass
                        else:
                            componente1.conexiones_nodo_comun.append(nombre_componente_comun)

                    componente2.nodo_comun = True
                    componente2.nodo_comun = True

            self.dibujar_topologia()

        else:
            print("Por favor, seleccione exactamente dos componentes para conectar.")

    def mover_componente(self, event):

        for componente in self.componentes:
            if abs(event.x - componente.x) < 20 and abs(event.y - componente.y) < 20:
                componente.x = event.x
                componente.y = event.y
                self.dibujar_componentes()
                self.dibujar_topologia()
                break

    def encontrar_valor(self, nombre):
        for componente in self.componentes:
            if componente.nombre == nombre:
                parte_real = int(componente.valor)
                parte_imaginaria = int(componente.valor_complejo)
                valor_complejo = complex(parte_real, parte_imaginaria)
                return valor_complejo
        return False

    def imprimir_valores(self, matrix_informacion):
        cantidad = len(matrix_informacion[0])
        voltaje_fuente = int(matrix_informacion[2][0])
        nombres_nodos_independientes = []
        voltaje_tierra = 0
        voltajes = {}
        corrientes = {}
        potencias = {}

        nodos_comunes = []
        voltaje_nodos = {}

        voltaje_nodos['nf'] = voltaje_fuente
        voltaje_nodos['nt'] = voltaje_tierra

        for i in range(cantidad):
            print('El voltaje en el nodo ' + str(matrix_informacion[1][i]) + ' es: ' + str(matrix_informacion[0][i]))
            voltaje_nodos[str(matrix_informacion[1][i])] = matrix_informacion[0][i]
            nombres_nodos_independientes.append(str(matrix_informacion[1][i]))

        for componente in self.componentes:

            if componente.nombre[0] == 'n':
                if componente.nodo_comun:
                    nodos_comunes.append(componente.nombre)

            if componente.nombre[0] == 'l' or componente.nombre[0] == 'c' or componente.nombre[0] == 'r':

                if componente.nodo_a in nodos_comunes:
                    componente.nodo_a = 'nt'
                if componente.nodo_b in nodos_comunes:
                    componente.nodo_b = 'nt'

                if componente.nodo_a in nombres_nodos_independientes:
                    pass
                elif componente.nodo_a == 'nf':
                    pass
                else:
                    componente.nodo_a = 'nt'

                if componente.nodo_b in nombres_nodos_independientes:
                    pass
                elif componente.nodo_b == 'nf':
                    pass
                else:
                    componente.nodo_b = 'nt'

                voltajes[componente.nombre] = voltaje_nodos[componente.nodo_a] - voltaje_nodos[componente.nodo_b]
                corrientes[componente.nombre] = voltajes[componente.nombre]/self.encontrar_valor(componente.nombre)
                potencias[componente.nombre] = voltajes[componente.nombre]*corrientes[componente.nombre]

                print('Componente: ' + str(componente.nombre) + ' Voltaje: ' + str(voltajes[componente.nombre]) +
                      ' Corriente: ' + str(corrientes[componente.nombre]) + ' Potencia: ' + str(potencias[componente.nombre]))




    def calcular_voltajes(self):

        numero_nodo_independientes = 0
        lista_nodos_independientes = []
        nodo_fuente = 0
        nodo_tierra = 0
        for nodo in self.nodos:

            if nodo.nombre == 'nf':
                nodo_fuente = nodo

            if not nodo.nodo_comun and len(nodo.conexiones) > 2:
                lista_nodos_independientes.append(nodo)
                numero_nodo_independientes += 1

            if nodo.nombre == 'nt':


                for i in range(len(nodo.conexiones_nodo_comun)):
                    if nodo.conexiones_nodo_comun[i] != 'n':
                        if nodo.conexiones_nodo_comun[i] in nodo.conexiones:
                            pass
                        else:
                            nodo.conexiones.append(nodo.conexiones_nodo_comun[i])

                nodo_tierra = nodo


        fuente_voltaje = 0
        for componente in self.componentes:
            if componente.nombre[0] == 'f':
                fuente_voltaje = componente


        matrix_resultados = [0] * len(lista_nodos_independientes)
        matrix_nodos = crear_matriz_ceros(len(lista_nodos_independientes))

        for i in range(numero_nodo_independientes):


            nodo_actual = lista_nodos_independientes[i]
            coeficiente_nodo_actual = 0

            nodos_vecinos = len(nodo_actual.conexiones)

            conjunto_nodo_actual = set(nodo_actual.conexiones)
            conjunto_nodo_fuente = set(nodo_fuente.conexiones)
            conjunto_nodo_tierra = set(nodo_tierra.conexiones)

            if len(conjunto_nodo_actual.intersection(conjunto_nodo_fuente)) > 0:
                nodos_vecinos -= 1
                elementos_interseccion_fuente = list(conjunto_nodo_actual.intersection(conjunto_nodo_fuente))
                elemento_interseccion = self.encontrar_valor(elementos_interseccion_fuente[0])

                matrix_resultados[i] = int(fuente_voltaje.valor)/elemento_interseccion

                coeficiente_nodo_actual += 1/elemento_interseccion


            if len(conjunto_nodo_actual.intersection(conjunto_nodo_tierra)) > 0:
                cantidad_elementos = len(conjunto_nodo_actual.intersection(conjunto_nodo_tierra))
                elementos_interseccion_tierra = list(conjunto_nodo_actual.intersection(conjunto_nodo_tierra))

                while cantidad_elementos != 0:
                    cantidad_elementos -= 1
                    elemento_interseccion = self.encontrar_valor(elementos_interseccion_tierra[cantidad_elementos])
                    coeficiente_nodo_actual += 1 / elemento_interseccion
                    nodos_vecinos -= 1

            contador = 0

            while nodos_vecinos != 0:
                if nodo_actual.nombre != lista_nodos_independientes[contador].nombre:
                    conjunto_nodos_independientes = set(lista_nodos_independientes[contador].conexiones)
                    if len(conjunto_nodo_actual.intersection(conjunto_nodos_independientes)) > 0:
                        lista_elemento_interseccion = list(conjunto_nodo_actual.intersection(conjunto_nodos_independientes))
                        elemento_interseccion = self.encontrar_valor(lista_elemento_interseccion[0])
                        coeficiente_nodo_actual += 1/elemento_interseccion
                        matrix_nodos[i][contador] = -1/elemento_interseccion
                        nodos_vecinos -= 1
                contador += 1
            matrix_nodos[i][i] = coeficiente_nodo_actual


        solucion = np.linalg.solve(matrix_nodos, matrix_resultados)

        if len(solucion) > 3:
            matrix_informacion = crear_matriz_ceros(len(solucion))
        else:
            matrix_informacion = crear_matriz_ceros(3)

        matrix_informacion[0] = solucion
        iterador = 0
        for nodo in lista_nodos_independientes:
            matrix_informacion[1][iterador]= nodo.nombre
            iterador += 1
        matrix_informacion[2][0] = fuente_voltaje.valor

        self.imprimir_valores(matrix_informacion)








elementos_seleccionados = []
circuito = Circuito()

app = tk.Tk()
app.title("Simulador Version 1.0")

nombre_label = tk.Label(app, text="Nombre del componente:")
nombre_label.grid(row=0, column=0, padx=5, pady=5)
nombre_entry = tk.Entry(app)
nombre_entry.grid(row=0, column=1, padx=5, pady=5)

valor_label = tk.Label(app, text="Valor del componente:")
valor_label.grid(row=1, column=0, padx=5, pady=5)
valor_entry = tk.Entry(app)
valor_entry.grid(row=1, column=1, padx=5, pady=5)

agregar_button = tk.Button(app, text="Agregar Componente", command=circuito.agregar_componente)
agregar_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

lista_componentes = tk.Listbox(app)
lista_componentes.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
lista_componentes.bind("<Button-1>", circuito.seleccionar_componente)

conectar_button = tk.Button(app, text="Conectar Componentes", command=circuito.conectar_componentes)
conectar_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

calcular_button = tk.Button(app, text="Calcular", command=circuito.calcular_voltajes)
calcular_button.grid(row=6, column=1, columnspan=2, padx=5, pady=5)

canvas = tk.Canvas(app, width=500, height=500)
canvas.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
canvas.bind("<B1-Motion>", circuito.mover_componente)

app.mainloop()
