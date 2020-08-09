from statistics import stdev
from random import random
from copy import deepcopy
import numpy as np
import math as m

import topology as top

# print(rutas[14][2][0])
# rutas2 = create_path(rutas[14][2][0])
# print(rutas2)

# L = 10
# C = 54
# links = np.full(L, C)


# 2consideraciones:
# 1)se tiene 3 cables, por lo que tendremos las mismas longuitudes de onda por enlace
# en caso de no encontrar la longuitud de onda en un cable, pregunto en los otros hasta que lo encuentre.

# 2) Tener que verificar ambas rutas (con sus respectivos long.onda) y
# luego si ambas son permitidas:
# verificar cual esta mas cargadas y elegir esa.
# en caso contrario, si solo 1 esta disponible, se manda por esa sin importar la carga
# en caso de tener cargas iguales, se prefiere siempre horario.

# -------------------------------------------------
#               CABLES LONGITUDES DE ONDA
# -------------------------------------------------

wire = {0: [840, 1], 1: [850, 1], 2: [860, 1], 3: [870, 1], 4: [880, 1], 5: [890, 1], 6: [900, 1], 7: [910, 1], 8: [920, 1],
        9: [930, 1], 10: [940, 1], 11: [950, 1], 12: [960, 1], 13: [970, 1], 14: [980, 1], 15: [990, 1], 16: [1000, 1],
        17: [1100, 1]}

links = []

for link in range(10):
    links.append(
        list([deepcopy(wire), deepcopy(wire), deepcopy(wire)]))

links[0][0][0][1] = 0
print(links[0][0][0][1])

routes_per_user = top.get_user_routes(10)
print(routes_per_user[0][2][1])





# print(links)
# link[0]-> 1er enlace/10
# link[0][0]->primer cable del primer enlace
# link[0][0][1]->1er canal del primer cable del primer enlace
# link[0][0][1][1]-> acceder al true

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
# 4. Se considerara las longuitudes de ondas ocupadas para verificar cual esta mas cargada (se contara por los 3 cables.)
# 5. No se tomara en cuanta como usada la longitud de onda que el usuario encontro para comunicarse al momento de contar las longitudes usadas.
# ----------------------------------------------------------------------------------------------

# 1)1---2---3 si
# 2)1---9---8---7---6---5---4---3 si
# mas cargado?? el 1
# por lo tanto me voy por el 2.


# --------------------------------------------------------------------------
#       PSEUDOCODIGO
# --------------------------------------------------------------------------
# 1. Usuario quiere transmitir -> ¿pregunta que longitud de onda?
# 2. se añade a la fel :v
# 3. pregunta el mejor camino
#   3.1
# 4. llega al destino y deja de transmitir e.e
# --------------------------------------------------------------------------


# longitudes de onda disponibles de extremo a extremo
enlace1 = 0

# ------------------------------------------------
#            Variables Principales
# ------------------------------------------------
N = 10  # Cantidad de nodos
M = N*(N-1)  # cantidad usuarios (90)
W = 3  # cables entre nodos (arbitrario)
# cada cable en multplexacion densa admite 18 canales.
C = 18*W  # canales disponibles (segun DWDM)

t_on = 0.001
rho = 0.3
t_off = t_on * ((1 - rho) / rho)

mu = 1 / t_on
lamb = 1 / (t_on + t_off)
lambPrima = 1 / t_off

charge = lamb / mu  # (0.25)

bloqueos_totales = []
# FEL = initFEL(M) # Esta función esta en "Manejo FEL"
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

# 0: OFF (Usuario no está transmitiendo)
# 1: ON (Usuario transmitiendo)
# -1: BLOCKED (Usuario bloqueado)

def initFEL(M):
    FEL = []

    for j in range(M):  # valores iniciales del FEL
        FEL.append(tuple((j, 0, randExp(lamb))))

    return FEL

def simulator(M, routes_per_user, links, m, l, lp):
  B = 0
  data = []
  # Inicialización de la FEL
  FEL = []
  for j in range(M): # valores iniciales del FEL
    FEL.append(tuple((j, ON, -1, randExp(l))))
  
  for arrivals in range(10**6):
    # Se ordena la FEL para conocer el evento próximo
    FEL = sorted(FEL, key=lambda item: item[3])
    
    # Se obtienen los datos del evento actual
    user_id, event, channel, current_time = FEL[0][0], FEL[0][1], FEL[0][2], FEL[0][3]
    # Se agrega un nuevo elemento a la FEL con el tiempo de llegada para el
    # mismo usuario.

    if event == ON:    
        is_successful_clock, chosen_channel_clock, sum_clock, total_network_sums = top.get_load_balance(
            routes_per_user[user_id][2][0], links)

        is_successful_counterclock, chosen_channel_counterclock, sum_counterclock, total_network_sums = top.get_load_balance(
            routes_per_user[user_id][2][1], links)

        if (is_successful_clock and is_successful_counterclock):
            if (sum_clock >= sum_counterclock):
                change_preferred_route(routes_per_user[user_id][2][0], links, chosen_channel_clock, event)
                FEL[0] = (user_id, OFF, chosen_channel_clock, current_time + randExp(m))
            else:
                change_preferred_route(routes_per_user[user_id][2][1], links, chosen_channel_counterclock, event)
                FEL[0] = (user_id, OFF, chosen_channel_counterclock, current_time + randExp(m))
        
        else if (is_successful_clock and not is_successful_counterclock):
            change_preferred_route(routes_per_user[user_id][2][0], links, chosen_channel_clock, event)
            FEL[0] = (user_id, OFF, chosen_channel_clock, current_time + randExp(m))

        else if (not is_successful_clock and is_successful_counterclock):
            change_preferred_route(routes_per_user[user_id][2][1], links, chosen_channel_counterclock, event)
            FEL[0] = (user_id, OFF, chosen_channel_counterclock, current_time + randExp(m))

        else:
            FEL[0] = (user_id, ON, -1, current_time + randExp(l))
            B += 1

    else if event == OFF:
        FEL[0] = (user_id, ON, -1, current_time + randExp(lp))

    if arrivals/100 == 0:
        data.append(((B / arrivals), stdev(total_network_sums)))
    
    return data


