	# Aqui se reunen una serie de funciones que puede ser de utilidad en la definicion o configuracion de arreglos de antenas

import numpy as np
import scipy.integrate as integrate
import scipy.interpolate as interp
###############################################################################
##     Funciones utiles para el direcionamiento del patron del arreglo       ##
###############################################################################
# Para apuntar el patron de un arreglo a una direccion phi,theta, es necesario conocer las fases
# de con las que se debe alimentar a los radiadores. Para eso se usa la funcion calcularFasesApuntamiento()
# de la siguiente manera:
# * Llama esta funcion por ejemplo asi:w_apuntar=calcularFasesApuntamiento(phi,theta,posiciones)
# * ve a tu arreglo y muliplica las exitaciones por w_apuntar
# Nota: la version del profe Binomi se diferencia de esta en que entrega las exponenciales complejas
# nos pareció más claro para ususario que se entregen las fases solamente.
def calcularFasesApuntamiento(phi,theta, posiciones):
    normal = np.array((np.cos(phi)*np.sin(theta),np.sin(phi)*np.sin(theta),np.cos(theta)))
    fases = -2*np.pi*posiciones@normal
    return fases
    
###############################################################################
##                 Funciones utiles para las aperturas                       ##
###############################################################################
def amplitudCosElev(posiciones,escala=0.8):
    centro = np.mean(posiciones,axis=0)
    desplazamientos = posiciones-centro
    radios = np.linalg.norm(desplazamientos,axis=1)
    rmax=np.max(radios)
    A = 1+np.cos(np.pi*escala*radios/rmax)
    return A/np.linalg.norm(A)*A.size**.5
    
#distintos patrones de radiacion para elementos. Ver ejemplo de arreglo lineal abajo para su uso
###############################################################################
##     Patrones de radiacion que pueden ser usados en los radiadores         ##
###############################################################################

def patron1():
    # Patron arbitrario generado a partir de tabla
    if ("patron" not in dir(patron1)):
        #angulosTheta = np.linspace(0,180,91)*np.pi/180
        angulosTheta = np.array([0,30,60,90,120,150,180])*np.pi/180
        intensidadesRel = np.array([1e-3,1,1.2,2,.3,.1,0])
        #intensidadesRel = np.array([8,8.1,8,6.1,4.1,2.1,5])
        f_denorm = interp.interp1d(angulosTheta,intensidadesRel,kind="cubic")
        # potenciaMedia = integrate.dblquad(lambda fi,th: f_denorm(th)**2*np.sin(th),0,np.pi,-np.pi,np.pi)[0]/(4*np.pi)
        # Por haber simetria respecto al eje z, la integral se reduce a
        potenciaMedia = integrate.quad(lambda th: f_denorm(th)**2*np.sin(th),0,np.pi)[0]/2
        escala = 1/potenciaMedia**.5 # para normalizar a potencia media 1
        def patron(phi,theta):
            return escala*f_denorm(theta)
        patron1.patron = patron
    return patron1.patron

def parche_sat():
    # Patron de la antena parche para el satelite de proy
    
    # la tabla de valores que representa al patron desde 0 hasta 180 grados
    angulosTheta = np.linspace(0,180,91)*np.pi/180
    intensidadesRel =np.array([3.9,4,4.1,4.2,4.3,4.2,4.25,4.2,4.1,4.05,4,3.95,3.95,
        4,4.05,4.15,4.1,4.1,4.1,4.1,4.05,3.95,3.9,
        3.85,3.8,3.8,3.9,3.95,4,4,4.05,4,4,4,3.9,3.85,
        3.8,3.8,3.75,3.6,3.55,3.45,3.35,3.25,3.15,3.05,3,
        2.85,2.7,2.65,2.6,2.6,2.6,2.6,2.6,2.6,2.5,2.5,2.45,
        2.35,2.2,2.15,1.9,1.9,1.95,2,1.9,1,1,1.7,2.1,2.3,2.35,
        2.25,2,1,1,1.8,2.1,2,1.8,1,2.1,2.5,2.55,2.5,2,1,0.5,2.2,2.45])
    
    # La interpolacion
    f_denorm = interp.interp1d(angulosTheta,intensidadesRel,kind="cubic")
    potenciaMedia = integrate.quad(lambda th: f_denorm(th)**2*np.sin(th),0,np.pi)[0]/2
    escala = 1/potenciaMedia**.5 # para normalizar a potencia media 1
    
    # el patron para cualquier phi, theta
    def patron(phi,theta):
        return escala*f_denorm(theta)
    parche_sat.patron = patron
    return parche_sat.patron
    
def parche_sat_2():
    # Patron de la antena parche para el satelite de proy
    
    # la tabla de valores que representa al patron desde 0 hasta 180 grados
    angulosTheta = np.linspace(0,180,181)*np.pi/180
    intensidadesRel =np.array([
     6.570,6.569,6.565,6.560,6.552,6.542,6.529,6.515,6.498,6.479,6.458,6.435,6.410,
     6.383,6.354,6.322,6.289,6.254,6.218,6.179,6.139,6.097,6.053,6.008,5.961,5.913,
     5.864,5.813,5.761,5.707,5.653,5.597,5.540,5.483,5.424,5.365,5.305,5.244,5.183,
     5.121,5.058,4.995,4.932,4.868,4.804,4.740,4.676,4.611,4.547,4.482,4.418,4.353,
     4.289,4.225,4.161,4.098,4.035,3.972,3.910,3.848,3.787,3.726,3.666,3.607,3.548,
     3.489,3.432,3.375,3.319,3.264,3.209,3.155,3.102,3.050,2.999,2.949,2.899,2.851,
     2.803,2.756,2.710,2.665,2.621,2.578,2.536,2.495,2.454,2.415,2.377,2.339,2.303,
     2.267,2.232,2.199,2.166,2.134,2.103,2.072,2.043,2.015,1.987,1.961,1.935,1.910,
     1.886,1.862,1.840,1.818,1.797,1.777,1.758,1.739,1.722,1.705,1.688,1.673,1.658,
     1.644,1.631,1.618,1.606,1.595,1.585,1.575,1.565,1.557,1.549,1.542,1.535,1.529,
     1.524,1.519,1.515,1.511,1.508,1.506,1.504,1.502,1.501,1.501,1.501,1.501,1.502,
     1.503,1.505,1.507,1.509,1.511,1.514,1.517,1.521,1.524,1.528,1.532,1.536,1.540,
     1.544,1.549,1.553,1.557,1.562,1.566,1.570,1.574,1.578,1.582,1.586,1.589,1.593,
     1.596,1.599,1.602,1.604,1.606,1.608,1.610,1.611,1.612,1.613,1.613,1.614
    ])
    
    # La interpolacion   integrate.dbquad doble intrgación
    
    f_denorm = interp.interp1d(angulosTheta,intensidadesRel,kind="cubic")
    potenciaMedia = integrate.quad(lambda th: f_denorm(th)**2*np.sin(th),0,np.pi)[0]/2
    
    #revisar formular para hacer el patron en 3D
    
    escala = 1/potenciaMedia**.5 # para normalizar a potencia media 1
    
    # el patron para cualquier phi, theta
    def patron(phi,theta):
        return escala*f_denorm(theta)
    parche_sat_2.patron = patron
    return parche_sat_2.patron
   

    
def patronDipoloCorto():
    if ("patron" not in dir(patronDipoloCorto)):
        f_denorm = np.sin
        #simetria axial, eje z
        potenciaMedia = integrate.quad(lambda th: f_denorm(th)**2*np.sin(th),0,np.pi)[0]/2
        escala = 1/potenciaMedia**.5 # para normalizar a potencia media 1
        def patron(phi,theta):
            return escala*f_denorm(theta)
        patronDipoloCorto.patron = patron
    return patronDipoloCorto.patron
def patronDipoloMediaOnda():
    self = patronDipoloCorto
    if ("patron" not in dir(self)):
        epsilon = 1e-6
        def f_denorm(theta):
            theta=np.array(theta)
            determinado = (theta > epsilon) & ((np.pi-theta) > epsilon)
            result = np.zeros(theta.shape)
            theta_determinado = theta[determinado]
            result[determinado] = np.cos(np.pi/2*np.cos(theta_determinado))/np.sin(theta_determinado) 
            return result
        #simetria axial, eje z
        potenciaMedia = integrate.quad(lambda th: f_denorm(th)**2*np.sin(th),0,np.pi)[0]/2
        escala = 1/potenciaMedia**.5 # para normalizar a potencia media 1
        def patron(phi,theta):
            return escala*f_denorm(theta)
        self.patron = patron
    return self.patron
def patronMonopoloCuartoOnda():
    self = patronMonopoloCuartoOnda
    if ("patron" not in dir(self)):
        epsilon = 1e-6
        def f_denorm(theta):
            theta=np.array(theta)
            determinado = (theta > epsilon) & (theta <= np.pi/2)
            result = np.zeros(theta.shape)
            theta_determinado = theta[determinado]
            result[determinado] = np.cos(np.pi/2*np.cos(theta_determinado))/np.sin(theta_determinado) 
            return result
        #simetria axial, eje z
        potenciaMedia = integrate.quad(lambda th: f_denorm(th)**2*np.sin(th),0,np.pi)[0]/2
        escala = 1/potenciaMedia**.5 # para normalizar a potencia media 1
        def patron(phi,theta):
            return escala*f_denorm(theta)
        self.patron = patron
    return self.patron

#def pmcoka(phi,theta):
#    pmcoi=patronMonopoloCuartoOnda()
#    p=pmcoi(phi,theta)
#    return p
##################################################################
##   Varias configuraciones de posiciones para arreglos         ##
##################################################################
#     Arreglo planar
# permite obtener las posiciones para un arreglo planar
# organizado de manera que vemos Nx filas y Ny columnas
# de manera que hay N=Nx x Ny radiadores y todos están distanciados
# de sus vecinos en una distand D x lambda
# las posiciones se entregan en forma de un vector de N elementos.

def posiciones_arreglo_planar(Nx,Ny, D):
    return D*np.array([(x,y,0) for x in range(Nx) for y in range(Ny)])
    
def posiciones_arreglo_esferico(Nx,Ny,D):
    cx=(Nx-1)/2
    cy=(Ny-1)/2
    return D*np.array([(x,y,np.sqrt(2*max(cx,cy)**2-(x-cx)**2-(y-cy)**2)) for x in range(Nx) for y in range(Ny)])

def posiciones_arreglo_cilindro(Nx,Ny,D):
    cx = (Nx-1)/2
    return D*np.array([(x,y,np.sqrt(2*cx**2-(x-cx)**2)) for x in range(Nx) for y in range(Ny)])

def posiciones_arreglo_linealz(Nz,Dz):
    return Dz*np.array([(0,0,z) for z in range(Nz)])
def posiciones_arreglo_sat_viejo():
    # Todas las distancias estan en lambdas
    # Bl el largo del panel solar
    # Ba el ancho del panel solar
    # D distancia entre radiadores de la parte basica
    Bl=3
    Ba=1
    antena11=np.array([Ba/2, Bl,0])
    antena12=np.array([-Ba/2, Bl,0])
    antena13=np.array([Ba/2, Bl-Ba,0])
    antena14=np.array([-Ba/2, Bl-Ba,0])
    arreglo1=np.array([antena11,antena12,antena13,antena14])
    return arreglo1    


def posiciones_arreglo_sat_ladoyp(Nx,Ny,D):
    # radiadores en el eje y parte positiva
    a1=posiciones_arreglo_planar(Nx,Ny,D)
    # lo siguiente es para correr el array del centro para despejar el
    # espacio que ocupa el cubo del satelite
    a1=a1+np.array([-D/2,1.5*D,0])
    return a1    

def posiciones_arreglo_sat_ladoydoble(Nx,Nypos,D):
    # radiadores en el eje y a ambos lados
    # Nypos, es el numero de elementos solo en el lado y positivo
    a1=posiciones_arreglo_sat_ladoyp(Nx,Nypos,D)
    a2=a1+np.array([0,-(Nypos+2)*D,0])
    return np.concatenate((a1,a2))

def posiciones_arreglo_sat_ladoxp(Nx,Ny,D):
    a1=posiciones_arreglo_planar(Nx,Ny,D)
    # lo siguiente es para correr el array del centro para despejar el
    # espacio que ocupa el cubo del satelite
    a1=a1+np.array([1.5*D,-D/2,0])
    return a1    
def posiciones_arreglo_sat_ladoxdoble(Nxpos,Ny,D):
    # radiadores en el eje y a ambos lados
    # Nypos, es el numero de elementos solo en el lado y positivo
    a1=posiciones_arreglo_sat_ladoxp(Nxpos,Ny,D)
    a2=a1+np.array([-(Nxpos+2)*D,0,0])
    return np.concatenate((a1,a2)) 

def posiciones_arreglo_sat_full(Nx,Ny,D):
   a1=posiciones_arreglo_sat_ladoydoble(Nx,Ny,D)
   a2=posiciones_arreglo_sat_ladoxdoble(Ny,Nx,D)
   return np.concatenate((a1,a2)) 
   #return a1
   
      
      
def posiciones_arreglo_dcentro(Nx,D,Dc):  
#f=2400 Hz

   long_onda= 0.124917   #en metros   
   gap= 0.5	#  distancia minima entre la antena y el contorno del panel solar 0.5 cm
   lon_sat= 10     # lontigud de la cara del satélite 10 cm
   lon_panel= 30   #  longitud de cada panel solar 30 cm
   rant = 4	# radio antena cm
   
   l1cm = (lon_sat/2) + rant + gap  
   Dcmin=(l1cm/100)/long_onda	
   
   #distancia máxima y minima entre antenas, depende del numero de antenas por panel. para esta aplicacion 1,2 o 3 son posibles
   #D_min=((rant*2 + 0.2 )/100/long_onda) # depende del radio de la antena y espacio minimo entre antenas
   #D_max = (((lon_panel - 2*rant-2*gap)/(Nx-1))/100)/long_onda #depende de la longitud del satélite y el radio de la antena  	
   	
   
   Dant=(Nx-1)*D
   a = Dc+np.linspace(0,Dant,num=Nx)
   b=[]
   for i in range(len(a)):
      rr=a[-(i+1)]
      b.append(-rr)
   T=np.concatenate((b,a))
   finalenx=np.array([(a,0,0) for a in T])
   finaleny=np.array([(0,a,0) for a in T])
   return np.concatenate((finalenx,finaleny))     
      
      


