from statistics import stdev
from random import random
from copy import deepcopy
from math import log
import topology as top

# ------------------------------------------------
#            CONSTANTES
# ------------------------------------------------

ON, OFF, NO_CHANNEL = 1, 0, -1
WIRES, WAVELENGTHS = 3, 18
WIRE_MODEL = [[840, 1], [850, 1], [860, 1], [870, 1], [880, 1], [890, 1], [900, 1], [910, 1], [920, 1],
    [930, 1], [940, 1], [950, 1], [960, 1], [970, 1], [980, 1], [990, 1], [1000, 1], [1100, 1]]


# ------------------------------------------------
#            Variables Principales
# ------------------------------------------------
N = 10  # Cantidad de nodos
M = N * (N - 1)  # cantidad usuarios (90)

t_on = 0.001
rho = 0.3
t_off = t_on * ((1 - rho) / rho)

mu = 1 / t_on
lamb = 1 / (t_on + t_off)
lambPrima = 1 / t_off

links = []
for link in range(N):
    links.append(
        list([deepcopy(WIRE_MODEL), deepcopy(WIRE_MODEL), deepcopy(WIRE_MODEL)]))
routes_per_user = top.get_user_routes(N)


# ------------------------------------------------
#        FUNCIÓN DISTRIBUCIÓN EXPONENCIAL
# ------------------------------------------------
def randExp(n):
    u = random()
    return (-1 / n) * log(u)

# ------------------------------------------------
#            Manejo FEL
# ------------------------------------------------

def simulator(M, links, routes_per_user, m, l, lp, load_balance):
    print(len(routes_per_user))
    B = 0
    blk_prob = []
    load_stdev = []
    # Inicialización de la FEL
    FEL = []
    total_network_sums = [54, 54, 54, 54, 54, 54, 54, 54, 54, 54]
    for j in range(M): # valores iniciales del FEL
        FEL.append(tuple((j, ON, NO_CHANNEL, randExp(l))))
    
    for arrivals in range(1, 10**6):
        # Se ordena la FEL para conocer el evento próximo
        FEL = sorted(FEL, key=lambda item: item[3])
        
        # Se obtienen los datos del evento actual
        user_id, event, asigned_channel, current_time = FEL[0][0], FEL[0][1], FEL[0][2], FEL[0][3]
        # Se agrega un nuevo elemento a la FEL con el tiempo de llegada para el
        # mismo usuario.

        if event == ON:    
            is_successful_clock, chosen_channel_clock, sum_clock, total_network_sums = top.get_load_balance(
                routes_per_user[user_id][2][0], links, total_network_sums)

            is_successful_counterclock, chosen_channel_counterclock, sum_counterclock, total_network_sums = top.get_load_balance(
                routes_per_user[user_id][2][1], links, total_network_sums)

            clock_hops = routes_per_user[user_id][2][0]
            counterclock_hops = routes_per_user[user_id][2][1]

            if is_successful_clock and is_successful_counterclock:
                if (sum_clock >= sum_counterclock and load_balance) or (clock_hops < counterclock_hops and not load_balance):
                    top.change_preferred_route(routes_per_user[user_id][2][0], links, chosen_channel_clock, event)
                    FEL[0] = (user_id, OFF, chosen_channel_clock, current_time + randExp(m))
                else:
                    top.change_preferred_route(routes_per_user[user_id][2][1], links, chosen_channel_counterclock, event)
                    FEL[0] = (user_id, OFF, chosen_channel_counterclock, current_time + randExp(m))

            elif is_successful_clock and (not is_successful_counterclock):
                top.change_preferred_route(routes_per_user[user_id][2][0], links, chosen_channel_clock, event)
                FEL[0] = (user_id, OFF, chosen_channel_clock, current_time + randExp(m))

            elif (not is_successful_clock) and is_successful_counterclock:
                top.change_preferred_route(routes_per_user[user_id][2][1], links, chosen_channel_counterclock, event)
                FEL[0] = (user_id, OFF, chosen_channel_counterclock, current_time + randExp(m))

            else:
                FEL[0] = (user_id, ON, NO_CHANNEL, current_time + randExp(l))
                B += 1

        elif event == OFF:
            top.change_preferred_route(routes_per_user[user_id][2][1], links, asigned_channel, event)
            FEL[0] = (user_id, ON, NO_CHANNEL, current_time + randExp(lp))

        if arrivals % 100 == 0:
            print(((B / arrivals), stdev(total_network_sums), total_network_sums))
            blk_prob.append((B / arrivals))
            load_stdev.append(stdev(total_network_sums))
    
    return blk_prob, load_stdev, total_network_sums

simulator(M, links, routes_per_user, mu, lamb, lambPrima, True)
# balanced_simulator(M, links, routes_per_user, mu, lamb, lambPrima)

