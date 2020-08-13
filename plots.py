import matplotlib.pyplot as plt

def plt_user(balanced_data, non_balanced_data, _link):
    end = min(len(balanced_data[4]), len(balanced_data[1][_link]), len(non_balanced_data[1][_link]))
    x = balanced_data[4][:end]
    y1 = balanced_data[1][_link][:end]
    y2 = non_balanced_data[1][_link][:end]
    
    plot_title = "Probabilidad de bloqueo por usuario v/s Llegadas"
    plt.plot(x, y1, color = "green") #, linewidth = 0.3, alpha = 0.9)
    plt.plot(x, y2, color = "blue") #, linewidth = 0.2, alpha = 0.7)
    #plt.scatter(x, y, color = "green")
    plt.title(plot_title)
    plt.xlabel("Llegadas")
    plt.ylabel("Prob. bloqueo por usuario")
    plt.savefig("result.png")
    plt.show()

def plt_network(balanced_data, non_balanced_data):
    end = min(len(balanced_data[4]), len(balanced_data[0]), len(non_balanced_data[0]))
    print(end)
    x = balanced_data[4][:end]
    y1 = balanced_data[0][:end]
    y2 = non_balanced_data[0][:end]
    
    plot_title = "Probabilidad de bloqueo de la red v/s Llegadas"
    plt.plot(x, y1, color = "green") #, linewidth = 0.3, alpha = 0.9)
    plt.plot(x, y2, color = "blue") #, linewidth = 0.2, alpha = 0.7)
    #plt.scatter(x, y, color = "green")
    plt.title(plot_title)
    plt.xlabel("Llegadas")
    plt.ylabel("Prob. bloqueo de la red")
    plt.savefig("result.png")
    plt.show()

def plt_link(balanced_data, non_balanced_data, _link):
    end = min(len(balanced_data[4]), len(balanced_data[2][_link]), len(non_balanced_data[2][_link]))
    print(end)
    x = balanced_data[4][:end]
    y1 = balanced_data[2][_link][:end]
    y2 = non_balanced_data[2][_link][:end]
    
    plot_title = "Disponibilidad de canales por enlace v/s Llegadas"
    plt.plot(x, y1, color = "green", linewidth = 0.8, alpha = 0.8)
    plt.plot(x, y2, color = "blue", linewidth = 0.8, alpha = 0.8)
    #plt.scatter(x, y, color = "green")
    plt.title(plot_title)
    plt.xlabel("Llegadas")
    plt.ylabel("Disponibilidad de canales")
    plt.savefig("result.png")
    plt.show()

def plt_stdev(balanced_data, non_balanced_data):
    end = min(len(balanced_data[4]), len(balanced_data[3]), len(non_balanced_data[3]))
    x = balanced_data[4][:end]
    y1 = balanced_data[3][:end]
    y2 = non_balanced_data[3][:end]

    plot_title = "Desviación estandar de canales disponibles entre enlace v/s Llegadas"
    plt.scatter(x, y1, color = "green", s=2)
    plt.scatter(x, y2, color = "blue", s=2)
    #plt.scatter(x, y, color = "green")
    plt.title(plot_title)
    plt.xlabel("Llegadas")
    plt.ylabel("S.D. canales entre enlaces")
    plt.savefig("result.png")
    plt.show()

def plt_10users(x, y1, y2):
    
    plot_title = "Probabilidad de bloqueo de 10 usuarios v/s Llegadas"
    for _uid in range(len(y1)):
        end = min(len(x), len(y1[_uid]), len(y2[_uid]))
        _x = x[10:end]
        _y1 = y1[_uid][:end]
        _y2 = y2[_uid][:end]
        plt.plot(x, _y1, color = "green")
        plt.plot(x, _y2, color = "blue")
    #plt.scatter(x, y, color = "green")
    plt.title(plot_title)
    plt.xlabel("Llegadas")
    plt.ylabel("Probabilidad de bloqueo de 10 usuarios")
    plt.savefig("result.png")
    plt.show()