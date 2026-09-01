# Instrucciones sobre FLET

## Índice
- **0. [Convenciones (tipos de dato que se repiten) y metodos Flet](#0-convenciones-tipos-de-dato-que-se-repiten-y-metodos-flet)**
  - 0.1 [Versión](#01-versión)
  - 0.2 [Convenciones](#02-convenciones)
  - 0.3 [Metodos de Flet](#03-metodos-de-flet)
- **1. [1. Estructura mínima](#1-estructura-mínima)**
  - 1.1 [Diferencia entre page.add() y page.update()](#11-diferencia-entre-pageupdate-y-pageadd)
  - 1.2 [Tema claro/oscuro](#12-tema-clarooscuro)
  - 1.3 [Eliminar contenido de una página](#13-eliminar-contenido-de-una-pagina)
  - 1.4 [Alineación vertical y horizontal](#14-alineacion-vertical-y-horizontal)
- **2. [Controles de mostrar](#2-controles-de-mostrar)**
  - 2.1 [ft.Text](#21-fttext)
  - 2.2 [ft.Icon](#22-fticon)
  - 2.3 [ft.Divider](#23-ftdivider)
- **3. [Botones y eventos](#3-botones-y-eventos)**
  - 3.1 [Botones](#31-botones)
  - 3.2 [Eventos](#32-eventos)
- **4. [Contenedores y colocación](#4-contenedores-y-colocación)**
  - 4.1 [Columnas](#41-columnas)
  - 4.2 [Filas](#42-filas)
  - 4.3 [Contenedores](#43-contenedores)
- **5. [Entrada de datos (formularios)](#5-entrada-de-datos-formularios)**
  - 5.1 [Campo de texto (TextField)](#51-campo-de-texto-textfield)
  - 5.2 [Campo de desplegable (Dropdown)](#52-campo-de-desplegable-dropdown)
  - 5.3 [Radio button (ft.RadioGroup)](#53-radio-button-ftradiogroup)
  - 5.4 [Opciones Checkbox](#54-opciones-checkbox)
  - 5.5 [Opciones Switch](#55-opciones-switch)
- **6. [Listas dinámicas](#6-listas-dinámicas)**
  - 6.1 [Listas (ListTile)](#61-listas-listtile)
  - 6.2 [Listas (ListView)](#62-listas-listview)
- **7. [Navegación entre pantallas](#7-navegación-entre-pantallas)**
  - 7.1 [Barra de navegación (NavigationBar)](#71-barra-de-navegación-navigationbar)
- **8. [Dialogo y confirmaciones](#8-dialogo-y-confirmaciones)**
  - 8.1 [Dialogos de alertas (AlertDialog)](#81-dialogos-de-alertas-alertdialog)
  - 8.2 [Dialogos de accion destructiva/no destructiva (SnackBar)](#82-dialogos-de-accion-destructivano-destructiva-snackbar)
- **9. [Mini-app integradora](#9-mini-app-integradora)**

---

## 0. Convenciones (tipos de dato que se repiten) y metodos Flet

### 0.1 Versión

Version para la que sirve este documento:

```py
Flet: 0.85.3
Flutter: 3.41.7
Pyodide: 0.27.7
```

### 0.2 Convenciones

Estos tipos aparecen en casi todos los controles. Se explican aquí una vez para no repetirlos en cada uno:

- **Colores** (`color`, `bgcolor`, `icon_color`, `selected_icon_color`...) → texto hexadecimal: `"#0B5563"`.
- **Catálogos** → listas cerradas de opciones que se sacan de la caja `ft`. No son números ni texto libre; el editor las autocompleta al escribir el punto. Los que usaremos:
    - `ft.Icons.*` → iconos (HOME, DELETE, ADD, EDIT, SETTINGS...).
    - `ft.FontWeight.*` → grosor de letra (NORMAL, BOLD, W_500...).
    - `ft.TextAlign.*` → alineación de texto (LEFT, CENTER, RIGHT, JUSTIFY).
    - `ft.MainAxisAlignment.*` → reparto en el eje principal (START, CENTER, END, SPACE_BETWEEN, SPACE_AROUND, SPACE_EVENLY).
    - `ft.CrossAxisAlignment.*` → alineación en el eje cruzado (START, CENTER, END).
    - `ft.KeyboardType.*` → teclado en móvil (TEXT, NUMBER, EMAIL, PHONE, MULTILINE).
    - `ft.ThemeMode.*` → tema (LIGHT, DARK, SYSTEM).
    - `ft.ScrollMode.*` → scroll (AUTO, ALWAYS, ADAPTIVE).
    - `ft.Alignment.*` → posición del contenido dentro de un Container (CENTER, TOP_LEFT, BOTTOM_RIGHT...).
- **Eventos** (`on_click`, `on_change`...) → una función, SIEMPRE sin paréntesis: `on_click=funcion`, nunca `funcion()`.
- **Booleanos** (`disabled`, `selectable`, `multiline`, `password`, `expand`...) → `True` / `False`.
- **`expand`** → `True` (ocupa el espacio disponible) o un número (`expand=2` reparte proporción frente a otros que compiten por el hueco).
- **`data`** → acepta cualquier cosa (texto, número, diccionario, objeto). El bolsillo oculto del control.
- **`.value`** → en campos de entrada (`TextField`) y textos, es SIEMPRE texto (`str`), aunque contenga números.

### 0.3 Metodos de Flet

``page.add(control)`` → añadir y pintar.

``page.update()`` → repintar tras modificar algo existente.

``page.controls.clear()`` → vaciar la pantalla (No borra el FAB ni el navigation_bar).

``page.theme_mode = ft.ThemeMode.LIGHT`` → tema (LIGHT, DARK, SYSTEM).

``page.floating_action_button = ft.FloatingActionButton()``/= None → mostrar/ocultar el FAB.


## 1. Estructura mínima

Antes de nada comprender que cuando hacemos `ft.Algo`, estamos fabricando ese algo y cuando hacemos `objeto.metodo()`, estamos usando un metodo/funcion del objeto en cuestión.

Cuando creamos la pagina con `ft.run(main)`, no se pone parentesis de main(), ya que daría error por querer ejecutarse al instante, lo dejamos sin parentesis y se ejecuta cuando se lo pedimos a la pagina. Otros similares son los botones, a los que tampoco se les pone el parentesis.

Para ejecutar el programa en consola se pone:

`flet run --web src/nombre.py`

Para ejecutar el programa y abrirlo desde el movil:

`flet run --web --host 0.0.0.0 --port 8551 src/nombre.py`

Desde el movil ir a la dirección: `TU_IP_REAL_PC:8551`

Si el archivo es main.py:

`flet run --web`

1. Importar flet al inicio del documento:

    `import flet as ft`

2. Declarar la función principal:

    `def main(page: ft.Page):`

3. Añadir contenido en la pagina dentro de la funcion principal:

    `page.add(ft.Text("Hola mundo"))`

4. Ejecutar la función principal al final del archivo:

    `ft.run(main)`

*Ejemplo:*
```py
import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("Hola mundo"))

ft.run(main)
```
### 1.1 Diferencia entre page.update() y page.add()
page.add() se utiliza para añadir contenido a la pagina, pero cuando cambiamos un valor de la pagina y ya estaba añadido previamente es necesario actualizar para que se muestre en la interfaz. Ejemplo:

Al añadir este contenido se muestra en pantalla
```py
titulo = ft.Text("Hola mundo")
page.add(titulo)
```
Al cambiar el valor de la variable es necesario actualizar la pagina con page.update()
```py
titulo.value = "Hola Flet"
page.update()
```
### 1.2 Tema claro/oscuro
Por defecto Flet viene con el tema oscuro, para cambiarlo a claro hay que poner esto al inicio de la función principal:

`page.theme_mode = ft.ThemeMode.LIGHT`

### 1.3 Eliminar contenido de una pagina
Para eliminar todo el contenido de una pagina se usa:

`page.controls.clear()`

### 1.4 Alineacion vertical y horizontal

La alineación global de la pagina se hace directamente en `page`, la pagina se comporta como una columna gigante y apila todo lo que se añade en vertical. 

El control fino de la alineación se hace con los contenedores, ya que esta es a nivel global de la página.

Ya que es la configuración global de la pagina éstas deben situarse al inicio de la función principal o a continuacion de la elección del `page.theme_mode`.

Se declaran de la siguiente forma:

```py
def main(page: ft.Page):
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER  
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.add(ft.Text("Estoy en el centro de la pantalla"))
```

## 2. Controles de mostrar
Algunos de los controles mas usados son:

### 2.1 ft.Text

`ft.Text(value, size, weight, color, italic, text_align, selectable, max_lines)`

```py
ft.Text(
    "Texto",  # Primer parametro siempre y es un string
    size=30,  # int o float, tamaño de letra
    weight=ft.FontWeight.BOLD,  # Tipo negrita
    color="#0c266b",  # Color del texto
    italic=True,  # Cursiva
    text_align=ft.TextAlign.*,  # Alineación del texto (LEFT,CENTER,RIGHT,JUSTIFY)
    selectable=True,  # El usuario puede seleccionar y copiar el texto
    max_lines=4,  # Limita cuántas líneas se muestran
    )
```

### 2.2 ft.Icon

`ft.Icon(name, color, size,)`

```py
ft.Icon(
    ft.Icons.ELECTRIC_BOLT,  # Catologo iconos en ft.Icons.*
    color="#CDCF33",  # Color del icono en hex
    size=30  # Tamaño del icono
    )
```

### 2.3 ft.Divider

`ft.Divider(height, thickness, color)`

```py
ft.Divider(
    height=30,  # Espacio vertical total que ocupa
    thickness=5,  # Grosor de la linea
    color="#CDCF33",  # Color de la linea en hex
    )
```

## 3. Botones y eventos

### 3.1 Botones

**1. Tipos de botones**

- Button `ft.Button(content, on_click, icon, color, bgcolor, disabled, data, tooltip)`

```py
ft.Button(
    content="Botón",  # Texto que aparece en el botón
    on_click=funcion,  # Función asignada a la accion de pulsar
    icon=ft.Icons.ADD,  # Añade un icono junto al content (ft.Icons.*)
    color="#CDCF33",  # Color del texto en hex
    bgcolor="#000000",  # Color de fondo del botón en hex
    disabled=False,  # True/False desactiva/activa el botón
    data=informacion,  # Cualquier cosa, campo oculto para guardar info.
    tooltip="texto",  # Mensaje que sale al pasar el ratón por encima
    )
```

- IconButton `ft.IconButton(icon, on_click, icon_size, selected, disabled, data, tooltip)`

```py
ft.IconButton(
    icon=ft.Icons.ADD,  # Añade un icono junto al content (ft.Icons.*)
    on_click=funcion,  # Función asignada a la accion de pulsar
    icon_color="#CDCF33",  # Color del icono en hex
    icon_size=30,  # Tamaño del icono
    selected=True,  # Aspecto del icono según este activado o no
    disabled=False,  # True/False desactiva/activa el botón
    data=informacion,  # Cualquier cosa, campo oculto para guardar info.
    tooltip="texto",  # Mensaje que sale al pasar el ratón por encima
    )
```

- FloatingActionButton `(page.floating_action_button = ft.FloatingActionButton(icon, text, on_click, bgcolor, tooltip, data))`

```py
page.floating_action_button = ft.FloatingActionButton(
    icon=ft.Icons.ADD,  # Añade un icono junto al content (ft.Icons.*)
    text="",  # Puede llevar texto ademas del icono o en lugar de el
    on_click=funcion,  # Función asignada a la accion de pulsar
    bgcolor="#000000",  # Color de fondo del botón en hex
    tooltip="texto",  # Mensaje que sale al pasar el ratón por encima
    data=informacion,  # Cualquier cosa, campo oculto para guardar info.
    )
```
    
    Este botón, al declararse con `page.`, no añade con `page.add()`.
    
    El FAB no está en `page.controls`, así que `page.controls.clear()` no lo borra. Para ocultarlo hay que asignarlo explícitamente a None: `page.floating_action_button = None` y hacer `page.update()`.

    Nota: dentro de un on_click, Flet suele hacer update() automáticamente al terminar la función, así que a veces parece innecesario. Ponlo igual siempre: no todos los casos se auto-actualizan de forma fiable, y en cuanto la función hace varias cosas deja de bastar. Depender del auto-update es frágil.

*Ejemplo de creacion de un Button:*

```py
saludo = ft.Text("Sin pulsar")

def cambiar(e):
    saludo.value = "¡Pulsado!"
    page.update()

boton = ft.Button(content="Púlsame", on_click=cambiar)

page.add(saludo, boton)
```

### 3.2 Eventos

Al pulsar un botón se envía un evento a la función asignada, este evento contiene información del botón pulsado, es por esto que una función puede asignarse a 'n' botones. Por tanto, podemos crear una función que al asignarsela al boton cambie por ejemplo, el contenido del mismo, pero solo el del boton pulsado.

El evento llega en el parámetro `e`. Su atributo `e.control` es el propio botón que se pulsó, desde ahí se puede acceder a todos los atributos del botón (`e.control.content`, `e.control.color`, `e.control.data`...)

- `e.control` es el botón que se pulsó (equivale a su variable, pero sin nombrarla). A partir de ahí se accede a los atributos del botón:
    - `content`: el texto visible del botón.
    - `color`: el color de ese texto.
    - `data`: un dato oculto que le guardas al botón al crearlo; no se ve en pantalla, pero lo recuperas con `e.control.data` para saber sobre qué actuar (ej. que artículo representa). 

*Ejemplo:*

```py
import flet as ft

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    def change_content(e):
        e.control.content = "Pulsado"
        e.control.color = "#FF0000"
        text = ft.Text(e.control.data)
        page.add(text)
        page.update()

    button1 = ft.Button(content="Sin pulsar", color="#ff0000", data="Botón Rojo")
    button2 = ft.Button(content="Sin pulsar", color="#0400ff", data="Botón Azul")
    button3 = ft.Button(content="Sin pulsar", color="#fbff00", data="Botón Amarillo")

    button1.on_click = change_content
    button2.on_click = change_content
    button3.on_click = change_content

    page.add(button1, button2, button3)

ft.run(main)
```

`data` también puede guardar un diccionario para llevar varios datos pegados al control (nombre, color original, etc.)

*Ejemplo con diccionario en data*
```py
import flet as ft

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    def change_content(e):
        e.control.content = "Pulsado"
        e.control.color = "#FF0000"
        text = ft.Text(e.control.data['name'], color=e.control.data['color'])
        page.add(text)
        page.update()

    buttons = [
        ft.Button(content="Sin pulsar", color="#ff0000", data={"name": "Botón Rojo", "color": "#ff0000"}, on_click=change_content),
        ft.Button(content="Sin pulsar", color="#0400ff", data={"name": "Botón Azul", "color": "#0400ff"}, on_click=change_content),
        ft.Button(content="Sin pulsar", color="#fbff00", data={"name": "Botón Amarillo", "color": "#fbff00"}, on_click=change_content),
        ]

    def clear(e):
        page.controls.clear()
        for btn in buttons:
            btn.content = "Sin pulsar"
            btn.color = btn.data['color']
        page.add(*buttons)
        page.update()

    page.floating_action_button = ft.FloatingActionButton(icon=ft.Icons.CLEAR, on_click=clear)
    page.add(*buttons)

ft.run(main)
```

## 4. Contenedores y colocación

### 4.1 Columnas

Son compartimentos en los que se agregan otros objetos que anidarán en forma de columna (verticalmente).

`horizontal_alignment` solo se nota si la columna es más ancha que su contenido (con width > contenido o expand=True).

La forma de declararlo es `ft.Column(controls, spacing, horizontal_alignment, alignment, width, height, expand, scroll, wrap)`

*Ejemplo*

```py
column = ft.Column(
        controls=[ # Aquí los objetos que quieras meter separados por coma
            ft.Text("Texto de prueba de columna 2"),
            ft.Text("Texto de prueba de columna 2"),
            ft.Text("Texto de prueba de columna 2"),
        ],
        spacing=10, # El espacio entre los objetos
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Alineacion eje perpendicular, en columnas, la horizontal.
        alignment=ft.MainAxisAlignment.CENTER,  # Alineacion eje principal, en columnas, la vertical.
        width=500, # Numero que indica ancho fijo de la pantalla, se usa width o expand, juntos nunca
        height=10,
        expand=True, # Extiende la columna a todo el ancho del padre
        scroll=ft.ScrollMode.AUTO,  # Permite scroll si el contenido se sale
        wrap=True,  # Si los hijos no caben saltan a otra columna
    )
```

### 4.2 Filas

Son compartimentos en los que se agregan otros objetos que anidarán en forma de fila (horizontalmente).

`alignment` solo se nota si la fila es más ancha que su contenido (con width > contenido o expand=True).

La forma de declararlo es `ft.Row(controls, spacing, alignment, vertical_alignment, width, height, expand, tight, wrap, scroll)`

*Ejemplo*

```py
rows = ft.Row(
        controls=[ # Aquí los objetos que quieras meter separados por coma
            ft.Text("Texto de prueba"),
            ft.Text("Texto de prueba"),
            ft.Text("Texto de prueba"),
        ],
        spacing=10, # El espacio entre los objetos
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, #  Alineacion del eje principal, en filas, la horizontal.
        vertical_alignment=ft.CrossAxisAlignment.CENTER, # Alineacion eje perpendicular, en filas, la vertical.
        expand=True, # Extiende la fila a todo el ancho del padre
        tight=True, # Si True la fila se encoge a lo justo de sus hijos.
        wrap=True, # Si True, cuando los hijos no caben saltan a la siguiente linea.
        scroll=ft.ScrollMode.AUTO, # Permite scroll horizontal si el contenido se sale
    )
```

NOTA: En Row, `alignment` es horizontal (main axis) y `vertical_alignment` vertical (cross axis). En Column es al revés: apila en vertical, así que su cross axis es el horizontal (`horizontal_alignment`). Regla: main axis = la dirección en que el contenedor apila; cross axis = la perpendicular.

### 4.3 Contenedores

Son compartimentos donde introducir o anidar otro contenedor, columna o fila (uno solo, no acepta listas), tambien añade fondo con `bgcolor`, relleno interno con `padding`, bordes redondeados con `border_radius`, ancho fijo con `width`...

`alignment` y `padding` solo se notan si el container tiene más espacio que su contenido.

La forma de declararlo es `ft.Container(content, padding, alignment, bgcolor, border_radius, width, height)`

*Ejemplo*

En el ejemplo column es una variable que representa otro contenedor en concreto `ft.Column`

```py
container = ft.Container(
        content=column, # Solo un control, no acepta listas
        padding=20, # Numero o ft.Padding.*
        margin=20,  # Numero o ft.Margin.*
        alignment=ft.Alignment.CENTER, # Alineacion dentro del contenedor
        bgcolor="#0400FF", # Color en hexadecimal
        border_radius=5, # A mayor número mas redondeadas las esquinas
        border=ft.Border.all(1, "#000000"),  # El primer número es el grosor del borde y el otro el color del mismo en hex.
        width=500, # Numero que indica el ancho
        height=500, # Numero que indica el alto
        on_click=funcion,  # Un container puede actuar como un botón (útil para tarjetas)
        ink=False,  # Efecto visual de "onda" al pulsar, si tiene on_click
    )
```

## 5. Entrada de datos (formularios)

### 5.1 Campo de texto (TextField)

El campo de texto en el que el usuario introduce "texto" se llama `TextField` y da igual que introduzca numero porque siempre se traduce a texto.

Se declara como `ft.TextField(label, hint_text, password, multiline, expand, width, on_change, keyboard_type, prefix_text, suffix_text, error_text)`

```py
campo = ft.TextField(
    label="Nombre",  # Etiqueta flotante sobre el campo
    hint_text="Tu nombre aquí",  # Texto gris de pista dentro del campo
    password=True,  # Oculta lo escrito con puntos (no usar a la vez que multiline)
    multiline=False,  # Permite varias líneas
    expand=True,  # Ocupa el espacio disponible,si se pone número ej: expand=2 reparte el espacio proporcionalmente entre los campos
    width=500,  # Indica el ancho del campo
    on_change=funcion,  # Validación en vivo en cada pulsación de tecla
    keyboard_type=ft.KeyboardType.TEXT, # Valor del catálogo EMAIL,PHONE, NUMBER...
    prefix_text="Algo antes del value",  # Prefijo, es tipo string
    suffix_text="Algo despues del value",  # sufijo, es tipo string
    error_text="Error",  # Texto que aparece en rojo bajo el campo, para ocultarlo se pone None.
)
```

### 5.2 Campo de desplegable (Dropdown)

Campo en el que aparece un desplegable con las opciones configuradas. El `Dropdown` tiene la particularidad de que sus opciones tienen dos caras, lo que ve el usuario y lo que guarda el programa, que casi siempre son distintas.

Se declara como `ft.Dropdown(value, label, options, hint_text, on_change, width, expand, disabled, error_text, text_size, color, bgcolor, tooltip, autofocus)`

```py
desplegable = ft.Dropdown(
    label="Artículos",  # Etiqueta del desplegable
    options=[  # Cada una de las opciones que tiene el desplegable.
        ft.dropdown.Option("key", "text"), # La primera es el `key` que se devuelve con `desplegable.value` y la segunda es `text` y se muestra con `desplegable.text`, si se escribe un valor solamente, el que se omite es el text.
        ft.dropdown.Option("key"), 
        ],
    hint_text="Elige un artículo",  # Pista gris cuando no hay nada seleccionado.
    on_change=funcion,  # Se dispara la funcion al seleccionar una opcion del desplegable.
    width=100,  # Ancho fijo.
    expand=True,  # En True ocupa el espacio disponible.
    disabled=False,  # Desactiva el desplegable.
    error_text="No elegiste nada",  # Mensaje en rojo debajo que indica que no hay nada seleccionado, se oculta con error_text=None.
    text_size=12,  # Tamaño del texto.
    color="#000000",  # Color del texto en hex.
    bgcolor="#000000",  # Color de fondo del desplegable en hex.
    tooltip="Artículos",  # Mensaje al pasar el ratón por el desplegable.
    autofocus=True,  # Si es True el desplegable recibe el foco al cargar la página.
    )
```

*Ejemplo de desplegable con botón; al seleccionar una opcion y pulsar el botón te muestra su ``.value`` y su ``.text``*

Nota: El ``.text`` es algo que funciona en mi version y podría no hacerlo en versiones futuras:

```py
import flet as ft

def main(page: ft.Page):
    page.theme_mode=ft.ThemeMode.LIGHT

    selector = ft.Dropdown(
        label="Artículos",
        options=[
            ft.dropdown.Option("light_point", "Punto de luz"),
            ft.dropdown.Option("plug", "Enchufe"),
            ft.dropdown.Option("displacement", "Desplazamiento")
        ],
    )

    texto = ft.Text("")

    def show_selection(e):

        if selector.value is None:
            texto.value = "Debes seleccionar una opción" 
        else:
            selection = selector.value + " -- " + selector.text
            texto.value = f"Has seleccionado {selection}"

        page.update()

    button = ft.Button(content="Aceptar", on_click=show_selection)
    column = ft.Column(controls=[selector, button, texto])
    page.add(column)

ft.run(main)
```
### 5.3 Radio button (ft.RadioGroup)

Esta opcion es la alternativa al desplegable (Dropdown), pero en lugar de mostrar las opciones al abrir el desplegable, todas las opciones están a la vista y solo tienes que pulsar la que corresponda. Al seleccionar otra cambia el valor y se desmarca la anterior automaticamente.

Para leer el valor del grupo se hace con ``grupo.value``, nunca con el ``Radio.value``, ha de mirarse el value del grupo entero de Radio.

```py
grupo = ft.RadioGroup(
    content=ft.Row(
        controls=[
            ft.Radio(value="new_build", label="Obra nueva"),
            ft.Radio(value="reform", label="Reforma"),
            ft.Radio(value="both", label="Ambos"),
        ]
    )
)
```
1. Siguiendo el ejemplo se observa que para este objeto es necesario declarar en primer lugar un `ft.RadioGroup`.
2. Despues dentro de content, un contenedor `ft.Row` que agrupa los Radios.
3. Y por ultimo dentro de controls se declaran los `ft.Radio`

RadioGroup se declara de la siguiente forma:

 `grupo = ft.RadioGroup(content, value, on_change)`

Radio se declara de la siguiente forma:

`ft.Radio(value, label, label_position, fill_color, active_color, disabled, autofocus, tooltip, data)`

Nota: La opcion .value puede ser confusa ya que aparece tanto en RadioGroup como Radio, sin embargo, en los Radio el atributo .value tiene un valor fijo que se le da y el RadioGroup tiene el valor del Radio seleccionado. Es decir, el value del radio elegido se convierte en el value del grupo. 

```py
grupo = ft.RadioGroup(
    content=ft.Row(  # Contiene un contenedor que agrupa los Radio.
        controls=[  # Aqui los objetos, en este caso los Radio.
            ft.Radio(
                value="new_build",
                label="Obra nueva",  # Lo que ve el usuario junto a la casilla.
                label_position=ft.LabelPosition.LEFT,  # Posicion de la etiqueta, puede ser LEFT o RIGHT.
                fill_color="#974545",  # Color de relleno del radio.
                active_color="#0246ff",  # Color cuando está seleccionado.
                disabled=False,  # Desactiva el control.
                autofocus=False,  # Recibe el foco al cargar la pantalla
                tooltip="Mensaje",  # Mensaje al pasar el ratón por encima. 
                data=CualquierCosa,  # Donde guardar cualquier dato util oculto.
            ),
            ft.Radio(value="reform", label="Reforma"),
            ft.Radio(value="both", label="Ambos"),
        ]
    ),  
    on_change=funcion,  # Se dispara al cambiar de opción.
    )
```

### 5.4 Opciones Checkbox

Un Checkbox es una casilla o casillas que puedes marcar o no al hacer click en ellas, sus estados son True/False.

El Checkbox se declara de la siguiente forma `casilla = ft.Checkbox(value, label, on_change, label_position, tristate, fill_color, check_color, disabled, autofocus, tooltip, data)`

```py
casilla = ft.Checkbox(
    label="Etiqueta",  # Etiqueta junto a la casilla.
    on_change=funcion,  # Función que se dispara al marcar la casilla.
    label_position=ft.LabelPosition.LEFT,  # Posicion de la etiqueta (LEFT, RIGHT)
    tristate=False,  # Si True, la casilla tiene 3 estados, marcado, desmarcado, indeterminado(None). Util para "Seleccionar todo".
    fill_color="#000000",  # Color de la casilla cuando está marcada.
    check_color="#000000",  # Color del check de dentro.
    disabled=False,  # Desactiva el control.
    autofocus=True,  # Recibe el foco al cargar la pantalla
    tooltip="Mensaje",  # Mensaje al pasar el ratón por encima.
    data=CualquierCosa,  # Donde guardar cualquier dato util oculto.
    )
```

### 5.5 Opciones Switch

Un Switch es una casilla que tiene dos estados Encendido/Apagado, True/False.

El ``Switch`` se declara de la siguiente forma `casilla = ft.Switch(value, label, on_change, label_position, active_color, inactive_thumb_color, track_color, disabled, autofocus, tooltip, data)`

```py
casilla = ft.Switch(
    label="Etiqueta",  # Etiqueta junto a la casilla.
    on_change=funcion,  # Función que se dispara al marcar la casilla.
    label_position=ft.LabelPosition.LEFT,  # Posicion de la etiqueta (LEFT, RIGHT)
    active_color="#230cf0",  # Color del interruptor cuando está encendido.
    inactive_thumb_color="#7a7676fd",  # Color del interruptor cuando está apagado.
    track_color="#000000",  # Color de la barra por la que desliza.
    disabled=False,  # Desactiva el control.
    autofocus=True,  # Recibe el foco al cargar la pantalla
    tooltip="Mensaje",  # Mensaje al pasar el ratón por encima.
    data=CualquierCosa,  # Donde guardar cualquier dato util oculto.
    )
```

## 6. Listas dinámicas

### 6.1 Listas (ListTile)

`ListTile` es un control especializado en filas de lista que ya trae los atributos o huecos colocados: uno para el título, otro para subtítulo, otro al final... esto te ahorra montar una Row a mano y tiene un aspecto profesional.

El `ListTile` se declara de la siguiente forma `ft.ListTile(title, subtitle, leading, trailing, on_click, data, dense, disabled, bgcolor, content_padding, toggle_inputs, selected, hover_color, icon_color, tooltip, url)`

Recuerda: Un control son objetos de Flet tales como ft.Text, ft.Icon, ft.Column, ft.Row...

```py
article_list = ft.ListTile(
    title=ft.Text(),  # Control principal de la fila.
    subtitle=ft.Text(),  # Control debajo del título, mas pequeño y color grisaceo.
    leading=ft.Text(),  # Control, lo que va al principio (izquierda).
    trailing=ft.Text(),  # Control, lo que va al final (derecha).
    on_click=funcion,  # Se dispara al pulsar la fila.
    data=CualquierCosa,  # Donde guardar cualquier dato util oculto.
    dense=True,  # Fila mas compacta.
    disabled=False,  # Desactiva la fila, no responde al click, se ve apagada.
    bgcolor="#000000",  # Color de fondo de la fila.
    content_padding=ft.Padding.*,  # Relleno interior de la fila.
    toggle_inputs=False,  # Si True y la fila contiene un Checkbox/Switch/Radio en leading/trailing, tocar la fila entera activa ese control.
    selected=False,  # Marca la fila como seleccionada (cambia su aspecto).
    hover_color="#000000",  # Color al pasar el ratón por encima.
    icon_color="#000000",  # Color de los iconos que tiene dentro.
    tooltip="Mensaje",  # Mensaje al pasar el ratón.
    url="www.voltgest.com",  # Si lo pones, al pulsar la fila abre la URL en el navegador.
    )
```

### 6.2 Listas (ListView)

ListView se utiliza para anidar las ListTile y poder hacer scroll.

Se declara `ft.ListView(controls, expand, spacing, padding, auto_scroll, horizontal, item_extent, first_item_prototype, divider_thickness, reverse, on_scroll)`

```py
ft.ListView(
    controls=lista,  # Lista de controles.
    expand=True,  # Para que ocupe el alto disponible. Necesario para activar scroll.
    spacing=1,  # Distancia entre elementos de la lista. Necesario para que divider_thickness se muestre.
    padding=ft.padding.*,  # Relleno interior alrededor de la lista.
    auto_scroll=False,  # La lista se desplaza hacia abajo automaticamente al añadir nuevos elementos, util para chats.
    horizontal=False,  # Para hacer scroll horizontal.
    item_extent=10,  # Fuerza una altura fija para cada elemento.
    first_item_prototype=False,  # Optimización para listas enormes.
    divider_thickness=1,  # Linea divisora entre elementos.
    reverse=False,  # Invierte el orden de scroll, empieza desde abajo.
    on_scroll=funcion,  # Funcion que se dispara al hacer scroll.
    )
```

*Ejemplo de lista dinámica usando ListTile y ListView*

```py
import flet as ft
from data import load_articles

def main(page: ft.Page):
    page.theme_mode=ft.ThemeMode.LIGHT

    articles = load_articles()

    def printer(e):
        data = e.control.data
        print(f"{data['name']} - {data['scope']} - {data['price']}")

    article_list = [ft.ListTile(
        title=ft.Text(f"{article['name']}"),
        leading=ft.Icon(ft.Icons.BOLT),
        subtitle=ft.Text(f"{article['scope']}"),
        trailing=ft.Text(f"{article['price']}"),
        on_click=printer,
        data=article,
    ) for article in articles]

    column = ft.ListView(controls=article_list, expand=True, spacing=1, divider_thickness=1)

    page.add(column)

ft.run(main)
```

## 7. Navegación entre pantallas

### 7.1 Barra de navegación (NavigationBar)

Es una barra de navegación fija en la parte inferior de la pantalla que nos permite movernos entre ellas.

Se declara como `ft.NavigationBar(destinations, selected_index, on_change, bgcolor)`

```py
ft.NavigationBar(
    destinations=Documentado abajo,  # Los botones de la barra.
    selected_index=0,  # Número que indica la pestaña que está activa.
    on_change=funcion,  # Se dispara al clicar en una pestaña distinta a la seleccionada actualmente.
    bgcolor="#000000",  # Color de fondo de la barra.
    )
```

Y dentro de destinations -> `destinations=ft.NavigationBarDestination(icon, label, selected_icon)`

```py
destinations=ft.NavigationBarDestination(
    icon=ft.Icon(ft.Icons.*),  # Icono de la pestaña.
    label="Home",  # El texto debajo del icono.
    selected_icon=ft.Icon(ft.Icons.*),  # Icono alternativo para cuando la pestaña está seleccionada.
    )
```

*Ejemplo de navegación entre pantalas con FAB incluido(floating_action_button)*

```py
import flet as ft

def main(page: ft.Page):
    page.theme_mode=ft.ThemeMode.LIGHT

    def change_screen(e):
        indice = e.control.selected_index
        if indice == 0:
            home()
        elif indice == 1:
            catalog()
        elif indice == 2:
            record()
        elif indice == 3:
            settings()

    def home():
        page.controls.clear()
        page.floating_action_button=None
        content = ft.Text("Estás en HOME")
        page.add(content)
        page.update()

    def catalog():
        page.controls.clear()
        page.floating_action_button=ft.FloatingActionButton(icon=ft.Icons.ADD)
        content = ft.Text("Estás en CATÁLOGO")
        page.add(content)
        page.update()

    def record():
        page.controls.clear()
        page.floating_action_button=None
        content = ft.Text("Estás en HISTORIAL")
        page.add(content)
        page.update()

    def settings():
        page.controls.clear()
        page.floating_action_button=None
        content = ft.Text("Estás en AJUSTES")
        page.add(content)
        page.update()

    page.navigation_bar=ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icon(ft.Icons.HOME), label="Home"),
            ft.NavigationBarDestination(icon=ft.Icon(ft.Icons.VIEW_LIST), label="Catálogo"),
            ft.NavigationBarDestination(icon=ft.Icon(ft.Icons.WORK_HISTORY), label="Historial"),
            ft.NavigationBarDestination(icon=ft.Icon(ft.Icons.SETTINGS), label="Ajustes"),
        ],
        on_change=change_screen,
    )

    home()
ft.run(main)
```

## 8. Dialogo y confirmaciones

### 8.1 Dialogos de alertas (AlertDialog)

Ventana emergente que aparece encima de la pantalla, oscurece el fondo y bloquea el resto de la app hasta que el usuario responde. Su uso principal es confirmar acciones destructivas (borrar, sobrescribir), como red de seguridad ante errores irreversibles.

Se fabrica con ``ft.AlertDialog(...)``, se muestra con ``page.show_dialog(dialogo)`` y se cierra con ``page.pop_dialog()``.

Se declara como ``ft.AlertDialog(title, content, actions, modal, on_dismiss)``

```py
dialog = ft.AlertDialog(
    title=ft.Text("¿Eliminar artículo?"),   # Control (ft.Text). El título de la ventana.
    content=ft.Text("Esta acción no se puede deshacer."),  # Control. El cuerpo/mensaje del diálogo.
    actions=[  # Lista de controles (botones). Los botones de acción del diálogo.
        ft.Button(content="Cancelar", on_click=cancel),
        ft.Button(content="Eliminar", on_click=confirm_delete),
    ],
    modal=True,  # True/False. Si True, obliga a pulsar un botón (no se cierra tocando fuera).
    on_dismiss=funcion,  # Función que se dispara si el diálogo se cierra tocando fuera (solo si modal=False).
)
page.show_dialog(dialog)   # Abre el diálogo
```

*Ejemplo:*

```py
def ask_delete(e):
    article = e.control.data

    def confirm_delete(e):
        articles.remove(article)   # borra el dato
        page.pop_dialog()          # cierra el diálogo
        catalog()                  # refresca la pantalla

    def cancel(e):
        page.pop_dialog()          # solo cierra

    dialog = ft.AlertDialog(
        title=ft.Text("¿Eliminar artículo?"),
        content=ft.Text(f"Vas a eliminar '{article['name']}'. ¿Estás seguro?"),
        actions=[
            ft.Button(content="Cancelar", on_click=cancel),
            ft.Button(content="Eliminar", on_click=confirm_delete),
        ],
    )
    page.show_dialog(dialog)
```

### 8.2 Dialogos de accion destructiva/no destructiva (SnackBar)

Mensaje que aparece brevemente en la parte inferior de la pantalla y desaparece solo tras unos segundos. A diferencia del AlertDialog, no bloquea la app ni exige respuesta — solo informa. Su uso es para confirmaciones no destructivas

Se fabrica con ``ft.SnackBar(...)`` y se muestra con ``page.show_dialog(...)``

Se declara como ``ft.SnackBar(content, duration, bgcolor, action)``

```py
snack = ft.SnackBar(
    content=ft.Text("Artículo guardado"),  # Control (ft.Text). El mensaje que se muestra.
    duration=3000,  # Número en milisegundos. Cuánto tiempo permanece visible (3000 = 3 seg).
    bgcolor=ACCENT,  # Color de fondo del mensaje en hex.
    action="Deshacer",  # Texto (str). Botón opcional de acción a la derecha (ej. "Deshacer").
    on_action=funcion, # Función. Se dispara si el usuario pulsa el botón `action`.
)
page.show_dialog(snack)   # lo muestra
```

## 9. Mini-app integradora

