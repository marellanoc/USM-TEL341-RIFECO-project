 
Balance de Carga de una Red Anillo. – RIFECO Inc.
Departamento de Electrónica, Universidad Técnica Federico Santa María

Matías Concha 201530017-8
Jorge Fernández 201504100-8
María Fernanda Rivas 201584033-4

Resumen—A continuación, se presentarán los principales
motivos por los que es de gran utilidad una simulación de una red anillo y lo que conlleva este tipo de red, por otro lado, se expondrán los resultados esperados de la simulación.


INTRODUCCIÓN
La tecnología avanza con el tiempo siendo así importante entender el funcionamiento de las redes ópticas, las cuales  son muy comunes en estos días, como por ejemplo una red metropolitana suele utilizar redes ópticas para mantener conexiones rápidas y estables entre sus habitantes.

La  importancia de entender este tipo de red y el balance de carga, hace que pueda ser elegida a futuro para proyectos grandes como lo es instalarla en una ciudad y poder entender a fondo las ventajas y desventajas de utilizar este tipo de red.

Descripción del problema
La red utilizada para este proyecto es una red óptica con forma de anillo que posee 10 nodos, simulando un tráfico normal de usuarios
.
Figura 1. Red anillo de 10 nodos.

Uno de los principales problemas a resolver con la simulación es la sobrecarga que pueden tener los enlaces al momento de comunicar usuarios, también el poco entendimiento que se podría tener de esta red al momento de ser usada. 
Como se mencionó con anterioridad, es importante entender el funcionamiento de la red de anillos para poder avanzar a pasos más grandes con este tipo de red y poder mantener lo mejor posible una carga homogénea para así no sobrecargar los enlaces y tener una comunicación más eficientes.

objetivos
Modelar y simular la carga sobre la red anillo descrita previamente, con el objetivo de observar si el balance de carga sobre la red es efectivo.

Entradas
Las entradas al simulador son la cantidad de nodos que componen la red, estos nodos son la principal fuente de la comunicación de los usuarios, la cantidad de estos nodos es 10.
Otra entrada es  la cantidad de usuarios que se simular, los cuales son 90, estos son los actores principales del simulador, donde ellos intentan comunicarse de un nodo a otro, por una cierta cantidad de tiempo.
También se tiene una cantidad de canales menor que la cantidad de usuarios, 50 canales.
Además de una cantidad de iteraciones K para ir verificando cómo se comporta la red, donde K=10^7 iteraciones.
El balance de carga utilizado se calcula previamente eligiendo λ y µ, estos tienen valor 1 y 4 respectivamente.
La carga de tráfico en la red se calcula con la siguiente fórmula: 



Fórmula 1

Donde λ = 1Ton + Toff  y µ =  1Ton donde da como resultado que la carga es:
ρ =λµ [Erlang]

Fórmula 2.

Dónde la Fórmula 2 se multiplica por la cantidad de usuarios que están pasando por un enlace y esto resulta en la carga de tráfico del enlace en ese momento.

Salidas
Las salidas del simulador es un detalle de la carga de tráfico de cada enlace para saber si el balanceo de carga está siendo efectivo o no. Lo que conlleva a mostrar una lista con la cantidad de usuarios que están ocupando los enlaces y su carga de tráfico en ese momento. La exposición de los datos se hará cada 100 iteraciones. 

Conocimientos y Herramientas
Conocimientos y herramientas adquiridas

Uno de los principales conocimientos que se tiene hasta ahora es del ramo TEL 317 que ha sido cursado con anterioridad por la mayoría de los miembros del equipo, donde el haber cursado este ramo entrega un mayor conocimiento de la carga de tráfico y del funcionamiento de la red redes ópticas; estos conocimientos ayudan a poder plantear el proyecto y encaminarlo de manera correcta.

Conocimientos y herramientas necesarias

Una de las herramientas necesarias y de la cual no se ha recibido información para el desarrollo del proyecto es  Google Colab, esta herramienta brinda un mejor desempeño a la simulación debido a que no todos los equipos de los integrantes tiene una buena capacidad para poder ejecutar la simulación, por lo que hace falta un poco de investigación de la herramienta, para poder utilizarla de manera correcta. Además permite el desarrollo del simulador de manera colaborativa, lo que es particularmente útil dado el contexto actual.



2consideraciones:
1)se tiene 3 cables, por lo que tendremos las mismas longuitudes de onda por enlace
en caso de no encontrar la longuitud de onda en un cable, pregunto en los otros hasta que lo encuentre.

2) Tener que verificar ambas rutas (con sus respectivos long.onda) y
luego si ambas son permitidas:
verificar cual esta mas cargadas y elegir esa.
en caso contrario, si solo 1 esta disponible, se manda por esa sin importar la carga
en caso de tener cargas iguales, se prefiere siempre horario.

----------------------------------------------------------------------------------------------
      VARIABLES A CONSIDERAR PARA DETERMINAR EL BALANCE DE CARGAR:
----------------------------------------------------------------------------------------------
1. Disponibilidad de la comunicación de origen a destino
2. Congestión individual de cada enlace
3. Ocupar primero un cable hasta llenarlo (por cada cnaal), antes de pasar al siguiente,
   con el objetivo de no agotar las longitudes de onda repetidas cuando hay otras disponibles
4. Se considerara las longuitudes de ondas ocupadas para verificar cual esta mas cargada (se contara por los 3 cables.)
5. No se tomara en cuanta como usada la longitud de onda que el usuario encontro para comunicarse al momento de contar las longitudes usadas.
----------------------------------------------------------------------------------------------

1)1---2---3 si
2)1---9---8---7---6---5---4---3 si
mas cargado?? el 1
por lo tanto me voy por el 2.


--------------------------------------------------------------------------
      PSEUDOCODIGO
--------------------------------------------------------------------------
1. Usuario quiere transmitir -> ¿pregunta que longitud de onda?
2. se añade a la fel :v
3. pregunta el mejor camino
  3.1
4. llega al destino y deja de transmitir e.e
--------------------------------------------------------------------------



