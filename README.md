Projeto Controlando braço robótico com as mãos

Neste projeto vamos utilizar visão computacional e arduino

Toda a programação é feita em Python.
No Arduino, instale o firmware Firmata Standard para permitir a comunicação com o Python.

O passo a passo para instalação é mostrado no vídeo do Youtube.

## Requisitos

- Python 3.12 ou mais recente
- Arduino com Firmata Standard
- Webcam

Instale as bibliotecas com:

```bash
python -m pip install -r requirements.txt
```

O programa detecta automaticamente a porta do Arduino. Se houver mais de uma porta
serial, informe-a pela variavel `SERVO_PORT`, por exemplo:

```bash
SERVO_PORT=/dev/ttyACM0 python main.py
```

No Windows, use `SERVO_PORT=COM3`. Pressione `q` ou `Esc` para encerrar.

## Mapeamento dos dedos

Cada dedo usa um servo conectado ao pino digital correspondente:

| Dedo | Pino Arduino | Funcao no codigo |
| --- | ---: | --- |
| Polegar | 10 | `pin = 10` |
| Indicador | 9 | `pin = 9` |
| Medio | 8 | `pin = 8` |
| Anelar | 7 | `pin = 7` |
| Minimo | 6 | `pin = 6` |

Para testar os dedos individualmente, sem ligar a camera, execute:

```bash
python testar-dedos.py
```

![image](https://github.com/user-attachments/assets/01af0426-7514-437f-aecc-d2267797de2d)
