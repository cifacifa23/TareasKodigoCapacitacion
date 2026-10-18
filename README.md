======================================================================
                 DOCUMENTO DE ENTREGA: PROYECTO VIBECODING
======================================================================
[!] -------------------------------------------------------------- [!]
                       ⚠️ INFORMACIÓN IMPORTANTE ⚠️
[!] -------------------------------------------------------------- [!]
     PUEDES VER LA PRESENTACION SI LO QUIERES VER MAS INTERACTIVO
[!] -------------------------------------------------------------- [!]






[!] -------------------------------------------------------------- [!]
                       ⚠️ INFORMACIÓN GENERAL ⚠️
[!] -------------------------------------------------------------- [!]
  Materia: AI for Developers
  Proyecto: Vibecoding Guiado: Desarrollo de una Aplicación o Mini-Juego 
            con IA como Copiloto
  Archivo Principal: space_arcade.py
[!] -------------------------------------------------------------- [!]


1. MINI-JUEGO FUNCIONAL (DESCRIPCIÓN Y CARACTERÍSTICAS)
----------------------------------------------------------------------
Se desarrolló un videojuego arcade 2D completo titulado "Space Arcade" utilizando 
Python y la librería gráfica pygame. Presenta una interfaz moderna con una 
resolución base de 800x800 píxeles, con soporte completo para ventanas 
redimensionables y alternancia a pantalla completa (tecla F).

Características Técnicas Implementadas:
- Selección de Dificultad: Menú interactivo que escala paramétricamente las 
  vidas iniciales y la velocidad de los obstáculos (Fácil, Normal, Difícil).
- Sistema de Jefes Dinámicos: Jefes finales que aparecen cada 30 puntos con 
  barras de salud interactivas, movimiento ondulatorio (patrón senoide) y 
  ataques en abanico.
- Power-ups y Progresión: Aparición aleatoria de mejoras flotantes para armas 
  (niveles 1 a 3), escudos temporales y recuperación de vidas.
- Efectos Visuales y Audio: Sistema de partículas físicas para explosiones y 
  un generador de audio procedural integrado mediante pygame.mixer (sin 
  necesidad de archivos externos).
- Persistencia de Datos: Almacenamiento local de la puntuación máxima histórica 
  mediante archivos JSON (highscore.json).


2. EVIDENCIA DE VIBECODING (PROMPTS UTILIZADOS)
----------------------------------------------------------------------
Prompt 1:
"Eres un desarrollador de videojuegos senior con experiencia en Python y Pygame. 
Necesito un script base, claro y ejecutable, de un pequeño shooter de naves en 2D.

Requisitos del juego:
- Ventana redimensionable de 800x800 píxeles, con título descriptivo.
- Una nave espacial controlada por el teclado, que se mueve con las flechas 
  del teclado o con WASD (ambos deben funcionar a la vez).
- La nave debe mantenerse dentro de los límites de la ventana durante todo 
  el movimiento.
- Disparos frontales: la nave dispara hacia arriba al pulsar la barra 
  espaciadora, con una cadencia limitada para que no se disparen de forma 
  continua e instantánea.
- Meteoros que caen desde la parte superior de la ventana en posiciones 
  aleatorias, con velocidades variables, y que se eliminan al salir por 
  la parte inferior.
- Los disparos deben poder destruir meteoros al impactar; los disparos que 
  salen de la pantalla se eliminan.

Expectativas del código:
- Un único archivo .py autocontenido, ejecutable con python space_arcade.py.
- Usa un bucle principal estándar de Pygame con control de FPS mediante 
  pygame.time.Clock.
- Organiza el código con clases simples para la nave, los disparos y los 
  meteoros, y comenta brevemente las partes clave en español.
- Gestiona el cierre de la ventana y la tecla Escape para salir limpiamente.
- No añadas puntuación, menús, sonidos ni imágenes externas salvo que sea 
  imprescindible: usa figuras geométricas dibujadas con Pygame."

Por qué se ajustó o refinó: Este prompt se utilizó para establecer la arquitectura 
inicial del bucle de juego (game loop), el control de eventos de redimensionamiento 
de ventana y el renderizado geométrico base.

Prompt 2:
Qué se pidió a la IA: "Añade un menú de selección de dificultad al inicio (Fácil, 
Normal, Difícil), un sistema de persistencia de récords máximos utilizando un 
archivo JSON local, y un sistema de partículas rectangulares con velocidad y 
vida decreciente para simular explosiones al destruir meteoros."

Por qué se ajustó o refinó: Se refinó para introducir mecánicas de juego 
duraderas, escalabilidad de dificultad y un salto cualitativo en el apartado 
visual con efectos de partículas.

Prompt 3:
Qué se pidió a la IA: "Integra un sistema de audio procedural usando buffers de 
pygame.mixer para generar efectos de sonido sintéticos de disparos y explosiones, 
power-ups flotantes de mejora de armas, y un jefe final con movimiento ondulatorio 
en senoide y disparos en abanico."

Por qué se ajustó o refinó: Necesario para dotar al juego de un diseño de mecánicas 
avanzadas y pulidas (game polish), logrando un producto funcional autónomo en un 
único archivo de código.


3. ITERACIÓN Y VALIDACIÓN DEL RESULTADO
----------------------------------------------------------------------
Modificación principal: El proyecto evolucionó de un script básico y estático de 
consola/ventana a una aplicación modular basada en clases orientadas a objetos 
(Player, Meteor, Boss, Particle, PowerUp). Se optimizó el bucle de renderizado 
para soportar cambios dinámicos de tamaño de pantalla en tiempo real (pygame.VIDEORESIZE) 
y controles de pausa avanzados mediante las teclas P y ESC.

Error o limitación identificada: Durante las pruebas en equipos sin tarjeta de 
sonido o con controladores de audio inactivos, la inicialización estricta de 
pygame.mixer podía lanzar excepciones críticas y detener el programa. 
Ajuste realizado: Se envolvieron las funciones de síntesis de audio procedural 
en bloques de control de excepciones (try-except), asegurando que el juego 
mantenga una ejecución estable y fluida aunque el dispositivo de audio no esté disponible.


4. REFLEXIÓN FINAL
----------------------------------------------------------------------
- Qué aprendió usando IA para programar: Aprendí que el desarrollo asistido por 
  IA (vibecoding) es una herramienta sumamente potente para prototipar sistemas 
  complejos (como matemáticas de partículas, síntesis de audio procedural y gestión 
  de archivos JSON) en cuestión de minutos, siempre y cuando se estructure el 
  desarrollo por etapas y requerimientos claros.

- Ventajas y límites del vibecoding:
  * Ventajas: Agilidad extrema para integrar librerías externas avanzadas (pygame) 
    y resolver problemas lógicos o de sintaxis al instante.
  * Límites: La IA requiere supervisión humana constante para equilibrar las reglas 
    de juego (game balance), adaptar los límites dinámicos de las pantallas 
    redimensionables y manejar excepciones de hardware específicas del sistema operativo.

- Partes del código que comprende y cuáles necesita reforzar:
  * Comprendo: La gestión del bucle principal de actualización por fotogramas 
    (CLOCK.tick(60)), la manipulación de listas de objetos dinámicos y la lectura/escritura 
    de datos estructurados en formato JSON.
  * Necesito reforzar: Técnicas avanzadas de optimización de renderizado gráfico de 
    alta frecuencia para manejar cientos de partículas simultáneas sin pérdida de 
    fotogramas en equipos de bajos recursos.


5. INSTALACIÓN Y EJECUCIÓN
----------------------------------------------------------------------
Requisitos externos:
   -> pip install pygame

Librerías nativas utilizadas (no requieren instalación adicional):
   -> random, sys, json, os, math, array

Cómo ejecutar el proyecto:
   -> python space_arcade.py

Controles del juego:
- Movimiento: Teclas de Flechas [↑ ↓ ← →] o [W, A, S, D]
- Disparar: Barra Espaciadora [SPACE]
- Pausar: Tecla [P] o [ESC]
- Pantalla Completa: Tecla [F]
- Salir / Volver al menú: Tecla [Q]
======================================================================
