from random import random
import numpy as np
import collections
import itertools
import math as m

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
    for i in range(n):
        for j in range(n):
            if (not i == j):
                    routes[(i, j)] = [(get_clockwise_routes(i, j, n)), (get_counterclockwise_routes(i, j, n))]
    return routes

routes = get_routes(10)

print(routes)

#consideraciones:
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
cable1 = {'1': 850, '2': 860, '3': 870, '4': 880, '5': 890, '6': 900, '7': 910, '8': 920,
          '9': 930, '10': 940, '11': 950, '12':960, '13':970, '14': 980, '15': 990, '16': 1000,
          '17': 1100, '18': 1200}

cable2 = {'1': 850, '2': 860, '3': 870, '4': 880, '5': 890, '6': 900, '7': 910, '8': 920,
          '9': 930, '10': 940, '11': 950, '12':960, '13':970, '14': 980, '15': 990, '16': 1000,
          '17': 1100, '18': 1200}
        
cable3 = {'1': 850, '2': 860, '3': 870, '4': 880, '5': 890, '6': 900, '7': 910, '8': 920,
          '9': 930, '10': 940, '11': 950, '12':960, '13':970, '14': 980, '15': 990, '16': 1000,
          '17': 1100, '18': 1200}

wl = 18
C = 54
W = 3

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
def byTime(elem):
    return elem[1]

def initFEL(users):
    FEL = []
    for i in range (users):
        arrival_time = randExp(lamb)
        FEL.append([i, arrival_time])
        FEL.sort(key = byTime)
    return FEL

def enter(FEL, links, dfRutas, user, users, current_time):
    links[dfRutas["RUTA"][user]] -= 1 # Se utliza el enlace 
    next_arrival_time = current_time + randExp(mu) # Se asigna tiempo de salida
                
    FEL.append([user + users, next_arrival_time])
    FEL.sort(key = byTime)
    return FEL, links

def blocked(FEL, user_list, user, current_time):
    user_list[user][1] += 1 
    next_arrival_time = current_time + randExp(lamb) # Se asigna tiempo a la siguiente llegada
                
    FEL.append([user, next_arrival_time])
    FEL.sort(key = byTime)
    return FEL, user_list

def leave(FEL, links, dfRutas, user, users, current_time):
    links[dfRutas["RUTA"][user - users]] += 1 # Se libera el enlace
    next_arrival_time = current_time + randExp(lambPrima) # Se asigna la siguiente llegada
            
    FEL.append([user - users, next_arrival_time])
    FEL.sort(key = byTime)
    return FEL, links
# ------------------------------------------------


