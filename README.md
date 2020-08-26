# GranMaster
Tutor de ajedrez basado en Stockfish

## Versión de desarrollo
Funciona con monitor estándar, sin requerir de pantalla LCD.<br>
El output a la LCD esta delimitado por "INICIO PANTALLA" y "FIN PANTALLA".

###Funcionalidades
<ul>
  <li>Configura partida nueva o carga perfil de usuario</li>
  <li>Permite configurar profundidad (0-20) y habilidad (0-20) de la máquina. Valores ~ 20 equivalen a ELO ~ 3500 (ELO Kasparov: 2500)</li>
  <li>Perfil de usuario permite escribir (e) y leer (l) partidas</li>
  <li>Función deshacer (d) permite deshacer jugadas. (t) y permiten ver el tablero y , respectivamente.</li>
  <li>Función análisis genera análisis de Stockfish de 4 ramas simultáneas, con profundidad = 15 y nivel = 20</li>
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
En GranMaster.py, sustituir linea XX por ubicacion de Stockfish. Por ejemplo, luego de

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
