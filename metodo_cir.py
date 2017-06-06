import math

#xi es la coordenada del perno en x
#yi es la coordenada del perno en y

def vectores(nx,ny,sx,sy):
	_contFilas = 0
	_contColumnas = 0
	vectXY = []
	x = 0
	y = 0
	while _contFilas < ny:
		while _contColumnas < nx:
			vectXY.append([x,y])
			x += sx
			_contColumnas+=1
		x = 0
		_contColumnas = 0
		y+=sy 
		_contFilas+=1
	return vectXY

def vectorX(vectores):
	_x = []
	for x in vectores:
		_x.append(x[0])
	return _x

def vectorY(vectores):
	_y = []
	for y in vectores:
		_y.append(y[1])
	return _y

def centroGravedad(vec):
	return float(sum(vec))/len(vec)

def h(_eprim,xi,xcg):
	return _eprim+xi-xcg

def v(yi,ycg):
	return ycg - yi

def d(h,v):
	return math.sqrt(pow(h,2)+pow(v,2))

def delta(di,m,d0):
	return di*d0/m

def R(_delta,_Rult):
	return _Rult*pow((1-math.exp(-10*_delta)),0.55)

def Rv(Ri,hi,di):
	return Ri*hi/di

def Rd(Ri,di):
	return Ri*di

#eprima se itera, ex lo ingresa el usuario
#valor inicial de eprima es ex
def crearTabla(ex,nx,ny,sx,sy):
	tabla = []
	d0 = 0.34 #valor del perno
	Rultima = 27 #valor del perno
	_xy = vectores(nx,ny,sx,sy)
	x = vectorX(_xy)
	y = vectorY(_xy)
	Xcg = centroGravedad(x)
	Ycg = centroGravedad(y)
	_h = []
	_v = []
	_d = []
	_delta = []
	_R = []
	_Rv = []
	_Rd = []
	_dMax = 0
	for e in x:
		_h.append(round(h(ex,e,Xcg),5))
	for e in y:
		_v.append(round(v(e,Ycg),5))
	for e in range(0,len(_h),1):
		_d.append(round(d(_h[e],_v[e]),5))
	_dMax = max(_d)
	for di in _d:
		_delta.append(round(delta(di,_dMax,d0),5))
	for _delta_i in _delta:
		_R.append(round(R(_delta_i,Rultima),5))
	for var in range(0,len(_h),1):
		_Rv.append(round(Rv(_R[var],_h[var],_d[var]),5))
	for var in range(0,len(_d),1):
		_Rd.append(round(Rd(_R[var],_d[var]),5))
	tabla.append(_h) #0
	tabla.append(_v) #1
	tabla.append(_d) #2
	tabla.append(_delta) #3
	tabla.append(_R)  #4
	tabla.append(_Rv) #5
	tabla.append(_Rd) #6
	return tabla

def mostrarTabla(tabla):
	_str_space = 8*" "
	print "N Tornillo    h(pulg)     v(pulg)      d(pulg)      delta(pulg)    R(pulg)    Rv(pulg)    Rd(pulg)"
	for i in range(0,len(tabla[0]),1):
		print "     " + str(i+1) + _str_space + "  " + str(tabla[0][i]) + _str_space + str(tabla[1][i]) + _str_space + "  " + str(tabla[2][i]) + _str_space + str(tabla[3][i])+ _str_space + str(tabla[4][i])+ _str_space + str(tabla[5][i])+ _str_space + str(tabla[6][i])
		 
def getDatos(datos,ex,eprima):
	_Rv = sum(datos[5])
	_Ri_di_amount = 0
	data = []
	for i in range(0,len(datos[1]),1):
		_Ri_di_amount+=datos[4][i]*datos[2][i]
	pu = _Ri_di_amount/(ex+eprima)
	data = [pu,_Rv,_Ri_di_amount]
	return data

def metodoNumerico(tabla,ex,nx,ny,sx,sy):
	eprima = ex
	datos = getDatos(tabla,ex,eprima)
	print datos
	result = []
	if datos[0] > datos[1]:
		while datos[0]/datos[1] > 1:
			eprima+= 0.02
			tablaAux = crearTabla(eprima,nx,ny,sx,sy)
			datos = getDatos(tablaAux,ex,eprima)
		result = [datos,tabla]
	elif datos[1] > datos[0]: 
		while datos[1]/datos[0] > 1:
			eprima-= 0.02
			tablaAux = crearTabla(eprima,nx,ny,sx,sy)
			datos = getDatos(tablaAux,ex,eprima)
		result = [datos,tablaAux]
	return result	

def c_cir(ex,nx,ny,sx,sy):
	tabla = crearTabla(ex,nx,ny,sx,sy)
	datos = metodoNumerico(tabla,ex,nx,ny,sx,sy)
	_tablaFinal = datos[1]
	_pu = datos[0][0]
	_Rv = datos[0][1]
	_c = _pu/27 
	mostrarTabla(_tablaFinal)
	print "\nEl valor de Pu es: ", round(_pu,4)
	print "El valor de Rv es: ", round(_Rv,4)
	print "El valor de C es: ", round(_c,4)
	return True


ex = float(raw_input("Ingrese la excentricidad: "))
nx = float(raw_input("Ingrese la cantidad de columnas de pernos: "))
ny = float(raw_input("Ingrese la cantidad de filas de pernos: "))
sx = float(raw_input("Ingrese la separacion de columnas: "))
sy = float(raw_input("Ingrese la separacion de filas: "))
c_cir(ex,nx,ny,sx,sy)





