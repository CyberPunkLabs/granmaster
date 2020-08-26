# GranMaster
Tutor de ajedrez basado en Stockfish

## Versión de desarrollo
Funciona con monitor estándar, sin requerir de pantalla LCD.

### Funcionalidades
<ul>
  <li>Configura partida nueva o carga perfil de usuario</li>
  <li>Permite configurar profundidad (0-20) y habilidad (0-20) de la máquina. Valores ~ 20 equivalen a ELO ~ 3500 (ELO Kasparov: 2500)</li>
  <li>El código del modelo Replicante es "habilidad.profundidad" (ej "Replicante 10.8" tiene habilidad 10 y profundidad 8).
  <li>Perfil de usuario permite escribir (e) y leer (l) partidas</li>
  <li>Función deshacer (d) permite deshacer jugadas; (t) permite ver el tablero.</li>
  <li>Función análisis (a) genera análisis de Stockfish de 4 ramas simultáneas, con profundidad = 15 y nivel = 20</li>
  <li>Análisis muestra ganancia relativa (centipeones / 100) y rama ([+1.03] [e2e4 e7e5] equivale a 1.03 peones a favor de las blancas luego de seguir esa rama)
  <li>El output a la LCD esta delimitado por "INICIO PANTALLA" y "FIN PANTALLA".</li>
  </ul>

### Por implementar:
<ul>
  <li>Libro de aperturas, basado en Modern Chess Openings (Nick de Firmian)</li>
  <li>Tutor nivel intermedio basado en My System (Ninwikovich)</li>
  <li>Paso simple de una funcionalidad a otra: ej de modo juego a modo apertura y luego a modo de análisis, o viceversa</li>
  <li><b>Mucha potencialidad educativa!</b></li>
  </ul>
    
    
### Detalles a mejorar:
<ul>
  <li>Formatear PGN cuando HUM es blancas</li>
  <li>Auditar análisis Stockfish (programado depth=15 pero entrega depth=7)</li>
  <li>Auditar análisis Stockfish (revisar que signo de cp esté en lo correcto)
  </ul>

### Requiere:
```
apt install stockfish

sudo apt-get install python3-pip
pip3 install RPi-GPIO
pip3 install spidev
```

### Utiliza
https://github.com/e-tinkers/LCD-5110-Raspberry-Library


### Tutorial librerías
Explicacion librerías (para Arduino):<br>
https://www.e-tinkers.com/2017/11/how-to-use-lcd-5110-pcd-8544-with-arduino/

Implementación en Raspberry:<br>
https://www.e-tinkers.com/2017/11/how-to-use-lcd-5110-pcd-8544-with-raspberry-pi/


### Ubicación motor Stockfish

#### En Linux
En GranMaster.py, sustituir linea ```stockfish = Stockfish("")``` por ubicacion de Stockfish. Por ejemplo, luego de

```
which stockfish
/usr/games/stockfish
```

declarar
```
stockfish = Stockfish("/usr/games/stockfish")
```

#### En Windows
Completar
