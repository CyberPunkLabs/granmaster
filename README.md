# granmaestro
Tutor de ajedrez basado en Stockfish

### Requiere:
```
apt install stockfish
pip3 install stockfish
```

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
