## <center>Memoria de nuestro proyecto</center>

<img src="Media/Header ReadMe.png" alt="Header" width="100%">

### Sprint 0:
- #### Creación del canal de Discord:
Desde el grupo de Slack se propuso utilizar Discord como medio de comunicación por su facilidad para compartir pantalla, dividir la comunicación en canales y por ser una herramienta que la mayoría sabia utilizar.
En la imagen siguiente se muestra como fue la división de canales y salas de reuniones:

<img src="./Media/discord.png">

- #### Primeras reuniones para conocernos.
A través de Discord programamos un horario conveniente para tener nuestra primera reunión. En ella nos conocimos, compartimos nuestra experiencia previa, organizamos horarios y roles.

- #### Definición de horario de reuniones diarias.
Definimos que el horario de reunión diaria sería todos los días a las 9 AM hora Argentina, con exccepción de Lunes y Jueves cuando nos reunimos luego de la reunión con el TL (9:30 AM)

- #### Definiciñon roles:
Así quedaron definidos los roles:

<img src="./Media/roles.png">

- #### Primeras ideas sobre proyectos.
Se barajaron varias opciones al principio, pero la decisión por unanimidad fue crear un gestor de restaurantes
partiendo de datos reales del local donde trabaja una de las integrantes del grupo. Nos pareció la mejor opción no solo por el potencial que vimos en estos datos sino por tratarse de un caso real, lo que representa un desafio mayor.

### Sprint 1:

- #### Elección del proyecto
A partir de la elección de nuestro proyecto de ggestión de restaurantes, al que llamamos DataChef, comenzamos el print 1.

- #### User Stories:

1. Como propietario del restaurante, quiero poder acceder a análisis detallados sobre las ventas para la eficiencia operativa.
2. Como gerente del restaurante, quiero recibir predicciones de las ventas de productos para ajustar el inventario y evitar la escasez o el exceso de stock.
3. Como gerente del restaurante, quiero recibir mensualmente promociones más rentables para aumentar las ventas en horarios de poca demanda.
4. Como gerente del restaurante, quiero saber la eficiencia de los empleados para incrementar el ticket promedio.


- #### Primera extracción y limpieza de datos:
Obtenemos los datos con los que el restaurante cuenta actualmente, a través de la API con la que el local trabaja.
Podemos ver la estructura que tenian en ese momento:

<img src="./Media/datos_toteat.png">

En el archivo [conexión_api](./base_de_datos/conexion_api.ipynb) se puede ver todo el proceso de extracción y limpieza.

- #### Creación de tablas y relaciones:
Mediante cambios en la estructura de los datos, se definieron distintas tablas en las que dividimos los registros, para su escalabilidad. De esta manera la base de datos no solo es más eficiente y optimiza el rendimiento, sino que permite hacer análisis más detallados de algunos puntos importantes, como las ventas por productos.

<img src="./Media/diagrama.png" width="1200">

En el archivo [conexión_bbdd](./base_de_datos/conexion_bbdd.ipynb) se puede ver también cómo se crean las diferentes tablas y sus relaciones.

- #### Creación de la base de datos en AWS
El método para alojar nuestros datos es Amazon Web Service.

<img src="./Media/aws.png">

En el archivo [conexión_bbdd](./base_de_datos/conexion_bbdd.ipynb) se puede ver también cómo se crean las diferentes tablas y sus relaciones.

- #### Conexión de la base de datos a Power Bi y primeros análisis
Una vez creada la base de datos, alojada en la nube, el equipo de análisis de datos comenzo con los primeros análisis.

<img src="./Media/pbi1.png" width="800">
<img src="./Media/pbi2.png" width="800">