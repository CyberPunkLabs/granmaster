# granmaestro
Tutor de ajedrez basado en Stockfish

### Requiere:
```
apt install stockfish
pip3 install stockfish

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
