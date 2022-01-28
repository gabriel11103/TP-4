TABLA = "{:<150} | {:<6} | {:^4} | {:<4} | {:<4} | {:<15}"


class Libro:
	def __init__(self, titulo, revisiones, anio, idioma, rating, isbn):
		self.titulo = titulo
		self.revisiones = revisiones
		self.anio = anio
		self.idioma = idioma
		self.rating = rating
		self.isbn = isbn

	def __str__(self):
		return TABLA.format(self.titulo, self.revisiones, self.anio, self.idioma, self.rating, self.isbn)


def str_a_libro(linea):
	v = linea.split(',')
	titulo = v[0]
	revisiones = int(v[1])
	anio = int(v[2])
	idioma = int(v[3])
	rating = float(v[4])
	isbn = v[5]

	return Libro(titulo, revisiones, anio, idioma, rating, isbn)


def validar_entero(msj, limite_inferior, limite_superior):
	x = int(input(msj))
	while x < limite_inferior or x > limite_superior:
		print(f'Error, el valor tiene que estar entre {limite_inferior} y {limite_superior}')
		x = int(input(msj))

	return x
