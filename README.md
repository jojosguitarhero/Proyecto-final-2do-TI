# Proyecto-final-2do-TI
El Videojuego trata sobre el control de un Antibodyn (Monoclonal) ya que es el anticuerpo que ataca a los tumores en el corazon, este anticuerpo debe navegar a través de 10 áreas críticas del cuerpo humano (representadas como cabinas biológicas).
La Misión : Limpiar el organismo de Tumor el cual se encuentra alojado en en corazon y bacterias.
Evolución : A medida que se recolecta Trofeos (inhibidores), Antibody desbloquea habilidades poderosas como el Rayo penetrante y el Escudo protector .
El juego es narrado por el Profesor Bio el cual guía al jugador con datos científicos reales, y culmina en un enfrentamiento final contra el Tumor , el origen de la negligencia en el organismo.
Cuerpo del codigo: Utilize una Máquina de Estados para separar el menú de inicio, la exploración, las batallas contra jefes (BOSS) y las pantallas de victoria o derrota. Esto permite que el juego sea fluido y organizado.
Generación de Laberintos : En lugar de niveles fijos, use un sistema procedimental. Cada área se genera usando una semilla (random.seed), lo que hace que los obstáculos sean diferentes en cada nivel pero se mantengan iguales si el jugador decide retroceder.
Sistema de pelea y Colisiones: Use Grupos de Sprites para manejar cientos de objetos simultáneamente. El juego calcula en tiempo real si un rayo golpeó a un virus o si el jugador tocó una pared, aplicando una física de rebote para evitar que el personaje se quede atrapado.
Inmersión Sonora : Tiene un sistema de audio que reacciona a las acciones del jugador: golpes, muertes de enemigos, diálogos y subidas de nivel, proporcionando un feedback constante.

pygame : Es la columna vertebral del proyecto. La elegí porque permite un control total sobre el renderizado de gráficos 2D y el manejo de eventos (teclado/ratón) de forma muy eficiente.
random : Fundamental para la rejugabilidad. Gracias a esta librería, la aparición de enemigos y la posición de los trofeos varían, haciendo que cada partida sea Diferente.
math : Esencial para la trigonometría de combate. Se utiliza para calcular los ángulos de los rayos y la rotación de la barra de hierro, asegurando que los ataques salgan en la dirección correcta hacia donde mira el jugador.
os : Crucial para la portabilidad . Permite que el juego localice las carpetas de assets (imágenes y sonidos) automáticamente, sin importar en qué carpeta o computadora se ejecute el proyecto.
Datos Biológicos : Los textos del Profesor Bio no son inventados; son curiosidades científicas reales integradas para que el jugador aprenda sobre la velocidad de los impulsos nerviosos o la capacidad del corazón mientras se divierte.
