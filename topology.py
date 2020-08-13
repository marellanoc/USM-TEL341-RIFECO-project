# ------------------------------------------------
#            CONSTANTES
# ------------------------------------------------

ON, OFF, NO_CHANNEL = 1, 0, -1

# ------------------------------------------------
#            Topología
# ------------------------------------------------

# i -> fuente
# j -> destino

def first_choose_channel(links, first_route, blocked_channels):
    chosen_channel = NO_CHANNEL
    for wire in range(3):       # 3 cables
        for channel in range(18):  # 18 canales
            # elegir el primer lamb disponible
            if ((links[first_route][wire][channel][1] == 1) and (channel not in blocked_channels)):
                if (chosen_channel == -1):
                    #print("El primer canal elegido es:", channel)
                    chosen_channel = channel

    return chosen_channel


def sum_total_lamb(route, links, sum_total_enlace): 
    sum_link = 0
    for wire in range(3):
        for channel in range(18):
            sum_link += links[route][wire][channel][1]
   
    sum_total_enlace[route] = sum_link
    return sum_link, sum_total_enlace


def is_wire_available(links, route, chosen_channel):
    available = False
    for wire in range(3):       # 3 cables
        if (links[route][wire][chosen_channel][1] == 1):
            available = True
    return available


def get_load_balance(routes, links, sum_total_enlace):  # recibe la ruta de horaria o antihoraria y links
    #print("Rutas:", routes)
    chosen_channel = 0
    first_step = True
    counter = 0
    sum_iter = 0
    successful = False
    blocked_channels = []

    while ((counter < len(routes)) and (len(blocked_channels) < 18)):
        route = routes[counter]
        #print("Largo:", len(routes))
        #print("contador", counter)
        #print("ruta", route)
        if (first_step):
            # #print("Entre a first_step")                    # iterando enlaces para ir cable por cable y canal por canal
            first_step = False                              # para elegir el primer lamb
            first_route = route
            #print("First en if:", first_route)
            chosen_channel = first_choose_channel(
                links, first_route, blocked_channels)
            sum_iter, sum_total_enlace = sum_total_lamb(first_route, links, sum_total_enlace)
            # Para debugear despues
            #print('chosen_channel: ', chosen_channel)
        else:
            #print("Entre else para preguntar is_wire")
            # iterando enlaces para ir cable por cable y canal por canal
            #print("ruta", route)
            # elegir los siguientes
            if (is_wire_available(links, route, chosen_channel)):
                _sum_iter, sum_total_enlace = sum_total_lamb(route, links, sum_total_enlace)
                sum_iter += _sum_iter
                #print("sum_iter:", sum_iter)
                successful = True
            else:
                #print("Me bloquee we")
                blocked_channels.append(chosen_channel)
                first_step = True
                counter = 0
                successful = False
        counter += 1
    return successful, chosen_channel, sum_iter, sum_total_enlace


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


# O(n^2) n es la cantidad de usuarios y se crearan todas las rutas de n*(n-1)
def get_user_routes(M):
    routes = {}
    user_id = 0
    for i in range(M):
        for j in range(M):
            if (not i == j):
                # Tomar el origen, destino y regresar rutas horarias y antih de esos nodos.
                routes[user_id] = (i, j, [(get_clockwise_routes(i, j, M)),
                                    (get_counterclockwise_routes(i, j, M))])
                user_id += 1

    return routes

def change_preferred_route(route, links, channel, event):
    if event == ON:
        new_event = OFF
    else:
        new_event = ON

    for link in route:
        for wire in range(3):
            if links[link][wire][channel][1] == event:
                links[link][wire][channel][1] = new_event
                break