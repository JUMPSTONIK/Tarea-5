from SR1 import *
from math import * 
import copy
from collections import namedtuple
width = 800
x = 0.1
y = 0.1
height = 600
V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])
zbuffer = [[-99999999999 for x in range(1000)] for y in range(1000)]


def loadModelMatrix(transalte, scale, rotate):
	transalte = V3(*transalte)
	scale = V3(*scale)
	rotate = V3(*rotate)
	translate_matrix=[
		[1,0,0,transalte.x],
		[0,1,0,transalte.y],
		[0,0,1,transalte.z],
		[0,0,0,1]
		]
	scale_matrix = [
			[scale.x,0,0,0],
			[0,scale.y,0,0],
			[0,0,1,scale.z],
			[0,0,0,1]
		]

	a = rotate.x
	rotation_matrix_x =[
			[1,0,0,0],
			[0,cos(a),-sin(a),0],
			[0,sin(a),cos(a),0],
			[0,0,0,1]
		]

	a = rotate.y
	rotation_matrix_y =[
			[cos(a),0,-sin(a),0],
			[0,1,0,0],
			[-sin(a),0,cos(a),0],
			[0,0,0,1]
		]

	a = rotate.z
	rotation_matrix_z =[
			[cos(a),-sin(a),0,0],
			[sin(a),cos(a),0,0],
			[0,0,1,0],
			[0,0,0,1]
		]
	
	rotation_matrix =  mulmat(rotation_matrix_z,mulmat(rotation_matrix_y,rotation_matrix_x))
	#Model = traslate_matrix @ rotation_matrix @ scale_matrix
	model = mulmat(scale_matrix,mulmat(rotation_matrix,translate_matrix))
	#print('model',model)
	return model
class Modelobj(object):
	def __init__(self,filename,material = None):
		with open(filename) as f:
			self.lines = f.read().splitlines()

		with open(material) as f:
			self.linesmtl = f.read().splitlines()

		self.vertices = []
		self.faces = []
		self.material = {}

	def read(self):
		global view
		materialA = ''
		for line in self.lines:
			if line:
				prefix, value = line.split(' ',1)

				if prefix == 'v':
					self.vertices.append(list(map(float,value.split(' '))))
				if prefix == 'f':
					# Separar por espacio
					listf1 = value.split(' ')
					listx = []
					# Ahora separar por guiones y castear a int
					for face in listf1:
						listf2 = face.split('/')
						listf = []
						for t2 in listf2:
							if t2:
								listf.append(int(t2))
							else:
								listf.append(0)
						# Se guarda el material antes de las caras a las que se aplicaran
						listf.append(materialA)
						listx.append(listf)
						self.faces.append(listx)
				# Para ver que material es el que toca a ciertas caras
				elif prefix == 'usemtl':
					materialA = value

	def readMtl(self):
		nameMat = ''
		for line in self.linesmtl:
			if line:
				prefix, value = line.split(' ',1)
				if prefix == 'newmtl':
					nameMat = value
				elif prefix == 'Kd':
					coloresStr = value. split(' ')
					listColores = list(map(float,coloresStr))
					self.material[nameMat] = listColores

	def getverts(self):
		return self.vertices
	def getfaces(self):
		return self.faces
	def getmateriales(self):
		return self.material
verts = []

def reverse(var):
	varc = []
	vat = []
	for y in range(0,len(var[0])):
		varf = []
		for x in range(0,len(var)):
			if y == 0 :
				vat.append(1)
			varf.append(var[x][y])

		varc.append(varf)

	varc.append(vat)
	#print(varc)
	return varc

def recover(mat):
    matriz = []
    for y in range(0,len(mat[0])):
        vam = []
        for x in range(0,len(mat)-1):
            vam.append(mat[x][y]/mat[3][y])
        matriz.append(vam)
    #print(matriz)
    return matriz


def mulmat(mat1, mat2):
	#print(mat1)
	mat3 = copy.deepcopy(mat2)
	for y in range(0,len(mat2)):
		for x in range(0,len(mat2[0])):
			mat3[y][x] = fabs(mat3[y][x]*0.0)
	#print(mat3)
	#print(mat1)
	#print(mat2)
	#print(len(mat3[0]))
	#print(len(mat3))
	#print(len(mat1[0]))
	#print(len(mat1))
	#print(len(mat2[0]))
	#print(len(mat2))
	for i in range(0,len(mat1)):
		#print('i =' + str(i))
		for j in range(0,len(mat2[1])):
			#print('j =' + str(j))
			for k in range(0,len(mat2)):
				#print('k =' + str(k))
				mat3[i][j] += mat1[i][k] * mat2[k][j]
				#print(mat3[i][j])
	#print(mat3)
	return mat3

def loadViewMatrix(x,y,z, center):
	M = [
		[x.x, x.y, x.z, 0],
		[y.x, y.y, y.z, 0],
		[z.x, z.y, z.z, 0],
		[0,0,0,1]
		]
	O = [
		[1,0,0,-center.x],
		[0,1,0,-center.y],
		[0,0,1,-center.z],
		[0,0,0,1]
		]
	
	view = mulmat(O,M)
	#print('view', view)
	return view

def loadProjectionMatrix(coeff):
	Projection = [
		[1,0,0,0],
		[0,1,0,0],
		[0,0,1,0],
		[0,0,coeff,1]
	]
	return Projection
#def lookat():	

def draw():
	verts_itter = iter(verts)
	try:
		while True:
			a = next(verts_itter)
			b = next(verts_itter)
			c = next(verts_itter)
			val.line_float(a[0],a[1],b[0],b[1])
			val.line_float(b[0],b[1],c[0],c[1])
			val.line_float(c[0],c[1],a[0],a[1])
	except StopIteration as e:
		print("f")

def loadViewportMatrix():
	Viewport = [
		[width/500,0,0,x+width/500],
		[0,height/500,0,y + height/500],
		[0,0,16,16],
		[0,0,0,1]
		]
	return Viewport
#eye=V3(0,0,1),center=V3(0,0,0),up=V3(0,1,0)
def load(filename,filenameMtl,eye,center,up,transalte, scale, rotate):
	var = Modelobj(filename,filenameMtl)
	var.read()
	var.readMtl()
	vertices = var.getverts()
	faces = var.getfaces()
	materiales = var.getmateriales()
	z = normVec(restVec(eye, center))
	x = normVec(prodx(up,z))
	y = normVec(prodx(z,x))
	
	#print(self.vertices)
	#print(reverse(self.vertices))
	#print('global view', view)
	#print(loadProjectionMatrix(-1/len(restVec(eye,center))))
	 
	matriz = mulmat(loadViewportMatrix(),mulmat(loadProjectionMatrix(-0.1),mulmat(loadViewMatrix(x,y,z, center),loadModelMatrix(transalte, scale, rotate))))
	vertices = mulmat(matriz,reverse(vertices))
	vertices = recover(vertices)
	#print(vertices)
	scal = 0.4


	luz=V3(0,0,1)
	for face in faces:
	
		x1=round(scal*(vertices[face[0][0]-1][0]+1)*(getwidth()/2))
		y1=round(scal*(vertices[face[0][0]-1][1]+1)*(getwidth()/2))
		z1=round(scal*(vertices[face[0][0]-1][2]+1)*(getwidth()/2))
		x2=round(scal*(vertices[face[1][0]-1][0]+1)*(getwidth()/2))
		y2=round(scal*(vertices[face[1][0]-1][1]+1)*(getwidth()/2))
		z2=round(scal*(vertices[face[1][0]-1][2]+1)*(getwidth()/2))
		x3=round(scal*(vertices[face[2][0]-1][0]+1)*(getwidth()/2))
		y3=round(scal*(vertices[face[2][0]-1][1]+1)*(getwidth()/2))
		z3=round(scal*(vertices[face[2][0]-1][2]+1)*(getwidth()/2))
		v1 = V3(x1,y1,z1)
		v2 = V3(x2,y2,z2)
		v3 = V3(x3,y3,z3)
		
		normal = normVec(prodx(restVec(v2,v1),restVec(v3,v1)))
		intens = prod(normal,luz)
		if intens<0:
			pass
		else:
			#print("jjj")
			glColor(materiales[face[0][3]][0]*intens,materiales[face[0][3]][1]*intens,materiales[face[0][3]][2]*intens)
			triangle(v1,v2,v3)

def barycentric(A, B, C, P):
	cx, cy, cz = prodx(
		V3(B.x - A.x, C.x - A.x, A.x - P.x),
		V3(B.y - A.y, C.y - A.y, A.y - P.y)
	)

	if cz == 0:
		return -1, -1, -1
	# Coordenadas baricentricas
	u = cx/cz
	v = cy/cz
	w = 1 - (u + v)

	return w,v,u

def bbox(A, B, C):
	xs = sorted([A.x, B.x, C.x])
	ys = sorted([A.y, B.y, C.y])
	return V2(xs[0], ys[0]), V2(xs[2], ys[2])

def triangle(A, B, C):
	bbox_min, bbox_max = bbox(A, B, C)

	for x in range(bbox_min.x, bbox_max.x + 1):
		for y in range(bbox_min.y, bbox_max.y + 1):
			w, v, u = barycentric(A, B, C, V2(x, y))

			# Si estan fuera del triangulo, no pintar
			if w < 0 or v < 0 or u < 0:
				pass
			else:
				z = A.z * w + B.z * v + C.z * u
				# Si z es mayor que el z buffer, pintar y cambiar valor zbuffer
				try:
					if z > zbuffer[x][y]:
						pointf(x, y)
						zbuffer[x][y] = z
				except:
						pass
					

def prod(v0,v1):
	return (v0.x*v1.x)+(v0.y*v1.y)+(v0.z*v1.z)
def restVec(v0,v1):
	return V3(v0.x-v1.x,v0.y-v1.y,v0.z-v1.z)
def prodx(v0,v1):
	return V3(
	v0.y * v1.z - v0.z * v1.y,
	v0.z * v1.x - v0.x * v1.z,
	v0.x * v1.y - v0.y * v1.x
		)
def magVec(v0):
	return (v0.x**2 + v0.y**2 + v0.z**2)**0.5
def normVec(v0):
	l = magVec(v0)
	if not l:
		return V3(0, 0, 0)
	return V3(v0.x/l, v0.y/l, v0.z/l)



glCreateWindow(width,height)

val = get_var()
trans = [0.0,0.8]
sca = [1.0,1.0]
#lookat()
load("BMONorm.obj","BMONorm.mtl",eye=V3(0,0,1),center=V3(0,0,0),up=V3(0,1,0),transalte=(-0.5,0,0),scale=(1,1,1), rotate=(0,0,0))
#draw()
glFinish()




