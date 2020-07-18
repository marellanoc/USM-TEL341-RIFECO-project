from random import random
import numpy as np
import collections
import itertools
import math as m
import copy

# ------------------------------------------------
#            Topología
# ------------------------------------------------

# i -> fuente
# j -> destino

def get_clockwise_routes(i, j, n):
    clockwise_routes_list = []
    k = i
    overclock = False
    
    if (i < j):
        while (k < j):
            clockwise_routes_list.append(k)
            k += 1

    else:
        while (k < j or not overclock):
            clockwise_routes_list.append(k)
            k += 1
            if k > n - 1:
                k = 0
                overclock = True
    
    return clockwise_routes_list

def get_counterclockwise_routes(i, j, n):
    counterclockwise_routes_list = []
    k = i
    overclock = False

    if (j < i):
        while (k > j):
            k -= 1
            counterclockwise_routes_list.append(k)

    else:
        while (k > j or not overclock):
            k -= 1
            if k < 0:
                k = n - 1
                overclock = True
            counterclockwise_routes_list.append(k)
    
    return counterclockwise_routes_list
    

def get_routes(n): # O(n^2)
    routes = {}
    c = 0
    for i in range(n):
        for j in range(n):
            if (not i == j):
                c+=1
                routes[c] = (i, j, [(get_clockwise_routes(i, j, n)), (get_counterclockwise_routes(i, j, n))])

                
    #print(c)
    return routes

routes = get_routes(10)

print(routes[14][2][0])

L = 10
C = 54
links = np.full(L, C)

print(links)

#print(routes)

#2consideraciones:
#1)se tiene 3 cables, por lo que tendremos las mismas longuitudes de onda por enlace
#en caso de no encontrar la longuitud de onda en un cable, pregunto en los otros hasta que lo encuentre.

#2) Tener que verificar ambas rutas (con sus respectivos long.onda) y
#luego si ambas son permitidas:
#verificar cual esta mas cargadas y elegir esa.
#en caso contrario, si solo 1 esta disponible, se manda por esa sin importar la carga
#en caso de tener cargas iguales, se prefiere siempre horario.

#-------------------------------------------------
#               CABLES LONGITUDES DE ONDA
#-------------------------------------------------

wire = {1: (850, True), 2: (860, True), 3: (870, True), 4: (880, True), 5: (890, True), 6: (900, True), 7: (910, True), 8: (920, True),
        9: (930, True), 10: (940, True), 11: (950, True), 12: (960, True), 13: (970, True), 14: (980, True), 15: (990, True), 16: (1000, True),
        17: (1100, True), 18: (1200, True)}

links = []

for link in range(10):
    links.append(tuple([copy.deepcopy(wire), copy.deepcopy(wire), copy.deepcopy(wire)]))

print(links)

wl = 18
C = 54
L = 3

# ----------------------------------------------------------------------------------------------
#       VARIABLES A CONSIDERAR PARA DETERMINAR EL BALANCE DE CARGAR: 
# ----------------------------------------------------------------------------------------------
# 1. Disponibilidad de la comunicación de origen a destino
# 2. Congestión individual de cada enlace
# 3. Ocupar primero un cable hasta llenarlo (por cada cnaal), antes de pasar al siguiente,
#    con el objetivo de no agotar las longitudes de onda repetidas cuando hay otras disponibles
#4. Se considerara las longuitudes de ondas ocupadas para verificar cual esta mas cargada (se contara por los 3 cables.)
#5. No se tomara en cuanta como usada la longitud de onda que el usuario encontro para comunicarse al momento de contar las longitudes usadas.
# ----------------------------------------------------------------------------------------------

#1)1---2---3 si
#2)1---9---8---7---6---5---4---3 si
#mas cargado?? el 1
#por lo tanto me voy por el 2.



# --------------------------------------------------------------------------
#       PSEUDOCODIGO 
# --------------------------------------------------------------------------
# 1. Usuario quiere transmitir -> ¿pregunta que longitud de onda?
# 2. se añade a la fel :v
# 3. pregunta el mejor camino
#   3.1
# 4. llega al destino y deja de transmitir e.e
# --------------------------------------------------------------------------


#longitudes de onda disponibles de extremo a extremo 
enlace1=0
   
# ------------------------------------------------
#            Variables Principales
# ------------------------------------------------
N = 10 #Cantidad de nodos
M = N*(N-1) #cantidad usuarios (90)
W = 3 # cables entre nodos (arbitrario)
#cada cable en multplexacion densa admite 18 canales.
C = 18*W # canales disponibles (segun DWDM)

t_on = 0.001
rho = 0.3
t_off = t_on * ((1 - rho) / rho)

mu = 1 / t_on
lamb = 1 / (t_on + t_off)
lambPrima = 1 / t_off

charge = lamb / mu #(0.25)

bloqueos_totales=[] 
#FEL = initFEL(M) # Esta función esta en "Manejo FEL"
# ------------------------------------------------



# ------------------------------------------------
#            Funciones de utilidad
# ------------------------------------------------
def randExp(n):
    u = random.random()
    return (-1/n)*m.log(u)
# ------------------------------------------------



# ------------------------------------------------
#            Manejo FEL
# ------------------------------------------------

#0: OFF (Usuario no está transmitiendo)
#1: ON (Usuario transmitiendo)
#-1: BLOCKED (Usuario bloqueado)

def initFEL(M):
    FEL = []

    for j in range(M): # valores iniciales del FEL
        FEL.append(tuple((j, 0, randExp(l))))

    return FEL


def simulation(route_df, L, M, C, l, lp, m):  
  # Definición del estado inicial del sistema
  FEL = initFEL(M)
  arrivals = 0

  #users = np.full((M, 2),0)
  L = 10
  C = 54
  links = np.full(L, C)
  while (arrivals < 10**7):
  
    # el primer paso en cada iteración de la simulación es reordenar la FEL,
    # posterior a la sobreesctritura de el primer elemento de la FEL luego de,
    # ser procesado.
    FEL = sorted(FEL, key=lambda item: item[2])

    if (np.all(links[route_df["ROUTE"][FEL[0][0]]] > 0) and 
       (FEL[0][1] == 0 or FEL[0][1] == -1)):
      
      # sobreesctritura del primer elemento de la FEL con el tiempo de servicio
      # del usuario entrante.
      FEL[0] = (FEL[0][0], 1, FEL[0][2] + randExp(m))
      users[FEL[0][0], 1] += 1
      links[route_df["ROUTE"][FEL[0][0]]] -= 1

    elif (not np.all(links[route_df["ROUTE"][FEL[0][0]]] > 0) and
         (FEL[0][1] == 0 or FEL[0][1] == -1)):
      
      # sobreesctritura del primer elemento de la FEL con el nuevo tiempo
      # de llegada del usuario recién bloqueado.
      FEL[0] = (FEL[0][0], -1, FEL[0][2] + randExp(l)) 
      users[FEL[0][0], 0] += 1

    elif (FEL[0][1] == 1):

      # sobreesctritura del primer elemento de la FEL con el nuevo tiempo
      # de llegada del usuario saliente.
      FEL[0] = (FEL[0][0], 0, FEL[0][2] + randExp(lp))
      links[route_df["ROUTE"][FEL[0][0]]] += 1

    else:
      raise ValueError('Se ha producido un error en el FEL: ',
                       links[route_df["ROUTE"][FEL[0][0]]], FEL[0])

  # salida del sistema
  route_df["BLKING PROB PER USER"] = users[:,0] / users[:,1]
  net_blking_prob = users[:,0].sum() / users[:,1].sum()

  return route_df, net_blking_prob



