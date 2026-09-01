# VoltGest

Aplicación web para generar presupuestos de electricidad de forma rápida y cómoda. Funciona en cualquier dispositivo con navegador: ordenador, Android e iPhone.

## Características

* Creación de presupuestos de forma rápida y guiada: se elige el tipo de trabajo (obra nueva o reforma), se añaden los datos del cliente y los artículos con sus cantidades.
* Catálogo de artículos totalmente configurable: crear, editar y borrar artículos con su precio y ámbito (obra nueva, reforma o ambos), de modo que se adapta a prácticamente cualquier uso.
* Selección de IVA (10 % o 21 %) y cálculo automático de base imponible, IVA y total, con actualización en vivo mientras se añaden artículos.
* Generación de dos PDF por presupuesto a partir de los mismos datos: una versión para el cliente y una versión interna con el desglose de precios por línea.
* Historial de presupuestos guardados, con numeración automática correlativa por año. Cada presupuesto puede consultarse de nuevo.
* Datos del negocio y condiciones configurables, que aparecen en los PDF generados.
* Copia de seguridad automática de los datos, con recuperación ante archivos corruptos.

## Capturas

(en desarrollo)

## Stack técnico

* **Python + Flask** — backend que gestiona la lógica, los datos y la generación de documentos.
* **HTML, CSS y JavaScript** — interfaz de usuario en el navegador.
* **JSON local** — persistencia de datos sin base de datos externa.
* **fpdf2** — generación de los documentos PDF.

## Estado del proyecto

En desarrollo.

## Instalación para desarrollo

```bash
git clone https://github.com/JoseRuiz44/voltgest.git
cd voltgest
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Después, abre el navegador en `http://localhost:5000`.