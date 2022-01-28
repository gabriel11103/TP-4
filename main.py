import os
from reg_libro import *
import pickle

# tupla Punto 5.
decadas = ('1900', '1910', '1920', '1930', '1940', '1950', '1960', '1970', '1980', '1990')


def mostrar_menu():
	print('\n************** MENU DE OPCIONES **************')
	print('1. Cargar vector')
	print('2. Buscar libro por ISBN o titulo')
	print('3. Buscar libro con mayor cantidad de revisiones')
	print('4. Generar matriz de libros con mayor rating segun idioma y año (entre 2000 y 2020)')
	print('5. Mostrar libros por decada (entre 1900 y 2000)')
	print('6. Generar archivo del punto 4.')
	print('7. Mostrar archivo')
	print('8. Salir\n')


def cargar_vector():
	vec = []
	if os.path.exists('libros.csv'):
		m = open("libros.csv", mode="rt", encoding="utf8")
		cont = 0
		for linea in m:
			cont += 1
			if cont > 1:
				nuevo_libro = str_a_libro(linea[:-1])
				add_in_order_isbn(nuevo_libro, vec)
		m.close()
	return vec


def add_in_order_isbn(reg, vec):
	n = len(vec)
	pos = n
	izq, der = 0, n - 1
	while izq <= der:
		c = (izq + der) // 2
		if vec[c].isbn == reg.isbn:
			pos = c
			break
		if reg.isbn < vec[c].isbn:
			der = c - 1
		else:
			izq = c + 1
	if izq > der:
		pos = izq
	vec[pos:pos] = [reg]


def buscar_por_titulo(libros, x_titulo):
	n = len(libros)
	for i in range(n):
		if x_titulo == libros[i].titulo:
			libros[i].revisiones += 1
			return libros[i]
	return -1


def buscar_por_isbn(libros, x_isbn):
	izq, der = 0, len(libros) - 1
	while izq <= der:
		c = (izq + der) // 2
		if x_isbn == libros[c].isbn:
			libros[c].revisiones += 1
			return libros[c]
		if x_isbn < libros[c].isbn:
			der = c - 1
		else:
			izq = c + 1
	return -1


# Funcion para buscar libro con mayor revisiones Punto 3.
def buscar_libro_con_mas_rev(libros):
	libro_cant_mayor = libros[0]
	vec_acumulacion_rating = [0] * 27
	vec_cont_por_idioma = [0] * 27

	for libro in libros:
		vec_acumulacion_rating[libro.idioma - 1] += libro.rating
		vec_cont_por_idioma[libro.idioma - 1] += 1

		if libro.revisiones > libro_cant_mayor.revisiones:
			libro_cant_mayor = libro

	print(f'\nEl libro con mas revisiones es {libro_cant_mayor.titulo}')
	print(libro_cant_mayor)

	# Sacamos el promedio
	indice = libro_cant_mayor.idioma
	rating_promedio = vec_acumulacion_rating[indice] / vec_cont_por_idioma[indice]
	print(f'\nRating promedio del idioma {indice} : {rating_promedio}')

	# Muestra si el resultado es mayor, menos o igual al promedio
	if libro_cant_mayor.rating > rating_promedio:
		print('El rating del libro encontrado es mayor al promedio\n')
	elif libro_cant_mayor.rating < rating_promedio:
		print('El rating del libro encontrado es menor al promedio\n')
	else:
		print('El rating del libro encontrado es igual al promedio\n')


def obtener_libro_mayor_rating(libros, anio, idioma):
	cont = 0
	libro_may_rating = None

	for libro in libros:
		if anio == libro.anio and idioma == libro.idioma:
			if cont == 0:
				libro_may_rating = libro
			if libro.rating > libro_may_rating.rating:
				libro_may_rating = libro
			cont += 1
	return libro_may_rating


def guardar_libros_rating(mat, vec):
	for f in range(len(mat)):
		for c in range(len(mat[f])):
			# Guardar libro con mayor rating para ese idioma y anio
			mat[f][c] = obtener_libro_mayor_rating(libros=vec, anio=c + 2000, idioma=f + 1)


def contar_libros_por_decada(libros):
	vector_conteo = [0] * 10
	for libro in libros:
		if 1900 <= libro.anio < 2000:
			a = int(libro.anio / 100)
			b = int(libro.anio - a * 100)
			decada = int(b / 10)
			vector_conteo[decada] += 1
	return vector_conteo


def mostrar_decadas(vector_conteo):
	mayor = vector_conteo[0]
	mayores = []
	print('\n______Cantidad de libros por decada______')
	for i in range(len(vector_conteo)):
		if vector_conteo[i] > mayor:
			mayor = vector_conteo[i]
			mayores = [i]
		elif vector_conteo[i] == mayor:
			mayores.append(i)
		if vector_conteo[i] > 0:
			print(f'Decada {decadas[i]} = {vector_conteo[i]}')

	print('\nDecada(s) con mas libros:')
	for i in range(len(mayores)):
		print(decadas[mayores[i]], 'con', mayor, 'libros')
	print()


def generar_archivo(mat):
	archivo = open('popular.dat', 'wb')
	cont = 0
	for f in range(len(mat)):
		for c in range(len(mat[f])):
			if mat[f][c]:
				pickle.dump(mat[f][c], archivo)
				cont += 1

	archivo.close()
	print(f'\nArchivo "populares.dat" creado con {cont} registros\n')


def mostrar_archivo():
	nombre_archivo = 'popular.dat'
	if not os.path.exists(nombre_archivo):
		print('\nDebe crear el archivo primero\n')
		return

	print('\nContenido del archivo\n')
	archivo = open(nombre_archivo, 'rb')
	tam = os.path.getsize(nombre_archivo)
	while archivo.tell() < tam:
		reg = pickle.load(archivo)
		print(f'Libro del idioma={reg.idioma} y anio {reg.anio} con mayor rating')
		print(reg)

	archivo.close()


def principal():
	libros = []
	mat = None
	mostrar_menu()
	opc = int(input('Ingrese la opcion: '))

	while opc != 8:
		if opc == 1:
			libros = cargar_vector()
			print('\nVector de libros cargado\n')

		elif opc == 2:
			op_busqueda = validar_entero(msj='Ingrese el metodo de busqueda: (1:titulo, 2:ISBN) ', limite_inferior=1, limite_superior=2)

			libro_encontrado = -1

			if op_busqueda == 1:

				x_titulo = input('Titulo a buscar: ')
				libro_encontrado = buscar_por_titulo(libros, x_titulo)

			elif op_busqueda == 2:

				x_isbn = input('ISBN a buscar: ')
				libro_encontrado = buscar_por_isbn(libros, x_isbn)

			if libro_encontrado != -1:
				print('\nSe Ha encontrado el libro con el termino de busqueda\n')
				print(libro_encontrado)
				print()
			else:
				print('\nNo se encontro un libro con el termino buscado\n')
		elif opc == 3:
			buscar_libro_con_mas_rev(libros)
		elif opc == 4:

			mat = [[0] * 21 for f in range(27)]
			guardar_libros_rating(mat, libros)
			print('\nMatriz generada correctamente')

		elif opc == 5:

			vector_conteo = contar_libros_por_decada(libros)
			mostrar_decadas(vector_conteo)

		elif opc == 6:

			if mat:
				generar_archivo(mat)
			else:
				print('\nDebe crear la matriz primero\n')

		elif opc == 7:
			mostrar_archivo()
		else:
			print('\nIngrese una opcion correcta')

		mostrar_menu()
		opc = int(input('Ingrese la opcion: '))


if __name__ == '__main__':
	print('\nBienvenido a la biblioteca de libros electronicos !!!')
	principal()
