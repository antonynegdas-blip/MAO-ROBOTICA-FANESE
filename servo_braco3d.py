from pyfirmata import Arduino,SERVO
import time
import os
from serial.tools import list_ports

PINOS = (10, 9, 8, 7, 6)
ANGULOS_FECHADO = {10: 150, 9: 180, 8: 140, 7: 140, 6: 140}

def encontrar_porta():
    porta_configurada = os.getenv("SERVO_PORT")
    if porta_configurada:
        return porta_configurada

    portas = list(list_ports.comports())
    preferidas = []
    for porta in portas:
        identificacao = f"{porta.device} {porta.description or ''}".lower()
        if any(nome in identificacao for nome in ("arduino", "ttyacm", "ttyusb", "usb serial")):
            preferidas.append(porta.device)

    if preferidas:
        return preferidas[0]
    if len(portas) == 1:
        return portas[0].device
    return None

porta = encontrar_porta()
if porta is None:
    raise RuntimeError(
        "Arduino nao encontrado. Conecte-o ou defina a porta na variavel SERVO_PORT "
        "(ex.: SERVO_PORT=/dev/ttyACM0 ou SERVO_PORT=COM3)."
    )

board = Arduino(porta)
for pino in PINOS:
    board.digital[pino].mode = SERVO

_angulos_atuais = {}

def rotateServo(pino, angle):
    if pino not in PINOS:
        raise ValueError(f"Pino de servo invalido: {pino}")
    angle = max(0, min(180, int(angle)))
    if _angulos_atuais.get(pino) == angle:
        return
    board.digital[pino].write(angle)
    _angulos_atuais[pino] = angle
    time.sleep(0.015)

def abrir_fechar(pin, on_off):
    if pin not in PINOS:
        raise ValueError(f"Pino de servo invalido: {pin}")
    if on_off not in (0, 1):
        raise ValueError("on_off deve ser 0 (fechar) ou 1 (abrir)")
    rotateServo(pin, 0 if on_off else ANGULOS_FECHADO[pin])

def testeTodos():
    for pino in PINOS:
        rotateServo(pino, 0)
    time.sleep(1)

    for pino in PINOS:
        rotateServo(pino, ANGULOS_FECHADO[pino])
        time.sleep(1)
        rotateServo(pino, 0)
        time.sleep(1)

def fechar():
    board.exit()

