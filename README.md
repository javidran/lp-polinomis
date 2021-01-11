# LP - Projecte Polinomis

Practica de LP Polinomis realizada por Javier Cabrera.
Incluye la clase ConvexPolygon.py, un lenguaje de programación y un bot de Telegram.

## Pre-requisitos

Para poder ejecutar los scripts es necesario tener instaladas las librerías definidas en el archivo "requirements.txt".
En él se encuentran las librerías con las correspondientes versiones utilizadas.

```
Pillow~=8.1.0
antlr4-python3-runtime~=4.9.1
python-telegram-bot~=13.1
```

## Como funciona

### ConvexPolygon

#### Estructura básica

Utilizar la clase ConvexPolygon es muy sencillo. 
Tan solo debe tenerse en cuenta como se conforma la lista de puntos de que el poligono recibe y como se estructuran.


Un **punto** es un tuple formado por floats -> (float, float)<br>
Ejemplo: (1, 0.2)


Una **lista de puntos** es lo que su nombre dice, una lista de puntos -> [(float. float), (float. float), ...]<br>
Ejemplo: [(0, 0), (0, 1), (1, 0)]

#### Inicialización

En el momento de definir un ConvexPolygon, será necesario proporcionarle una lista de puntos a procesar. 


```
lista = [(0, 0), (0, 1), (1, 0)]
poligono = ConvexPolygon(lista)
```

#### Métodos

Todos los métodos ofrecidos por la clase ConvexPolygon se encuentran documentados en la misma. Pueden consultar el código fuente para consultarlos y leer en la documentación que hacen.

Es importante recalcar que todos los métodos que devuelven puntos o lista de puntos se estructuraran bajo el mismo formato explicado anteriormente.

#### Script de ejemplo

Se encuentra a su disposición un script sencillo que crea dos poligonos y realiza la unión de los mismos en el archivo "test.py". Ejecutable mediante el comando:
```
python3 test.py
```

### Lenguaje de programación

#### Definición 
El lenguaje de programación no es necesario explicarlo, ya que cumple todos los requerimientos definidos en el enunciado de la practica de LP-Polinomis.

#### Scripts de ejemplo

Para comprobar su correcto funcionamiento, se recomienda el uso del bot explicado más adelante.

Igualmente se ofrecen 2 scripts para poder utilizar el lenguaje:
- Script que procesa todo el input definido en el archivo script.txt. Por defecto contiene el ejemplo definido en el enunciado:
```
python3 cl/test_grammar.py
```

- Script que procesa una sola linea provista a través del terminal durante su ejecución:
```
python3 cl/test_single_grammar.py
```

### Bot de Telegram

El bot de Telegram utiliza el lenguaje de programación creado. En caso de querer realizar pruebas, su uso es recomendado, ya que la instancia de los datos definidos se conserva en cada conversión de cada usuario.

#### Inicialización

Antes de poder hablar con el bot, será necesario inicializarlo. Para ello solamente será necesario ejecutar el script "bot.py":
```
python3 bot.py
```

#### Enlace y uso del bot

Se puede hablar con el bot a través de: [@JavierCPolinomisBot](t.me/JavierCPolinomisBot)

El primer paso es ejecutar el comando "/start".
<br>Una vez inicializado, el bot procesará todos los mensajes a través del lenguaje de programación creado. Se pueden enviar varias sentencias en un mismo mensaje. En caso de mandar varios mensajes, la instancia de los poligonos persistirá para el usuario.

## Autor

* **Javier Cabrera Rodríguez**