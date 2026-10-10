import os

import cv2
import mediapipe as mp
import servo_braco3d as mao

LARGURA = 640
ALTURA = 480
INDICE_CAMERA = int(os.getenv("CAMERA_INDEX", "0"))

def abrir_camera():
    cap = cv2.VideoCapture(INDICE_CAMERA, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap.release()
        raise RuntimeError(
            f"Nao foi possivel abrir a camera {INDICE_CAMERA}. "
            "Verifique se o tablet esta conectado como webcam e ajuste CAMERA_INDEX."
        )
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, LARGURA)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, ALTURA)
    return cap

def executar():
    cap = abrir_camera()
    hands = mp.solutions.hands
    desenho = mp.solutions.drawing_utils

    try:
        with hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        ) as detector:
            while True:
                success, img = cap.read()
                if not success or img is None:
                    print("Nao foi possivel ler um frame da camera.")
                    continue

                frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                resultados = detector.process(frame_rgb)
                pontos = []
                altura, largura = img.shape[:2]

                if resultados.multi_hand_landmarks:
                    for mao_detectada in resultados.multi_hand_landmarks:
                        desenho.draw_landmarks(img, mao_detectada, hands.HAND_CONNECTIONS)
                        pontos = [
                            (int(ponto.x * largura), int(ponto.y * altura))
                            for ponto in mao_detectada.landmark
                        ]
                        for cx, cy in pontos:
                            cv2.circle(img, (cx, cy), 4, (255, 0, 0), -1)

                        dist_polegar = abs(pontos[17][0] - pontos[4][0])
                        estados = {
                            10: dist_polegar >= 80,
                            9: pontos[5][1] - pontos[8][1] >= 1,
                            8: pontos[9][1] - pontos[12][1] >= 1,
                            7: pontos[13][1] - pontos[16][1] >= 1,
                            6: pontos[17][1] - pontos[20][1] >= 1,
                        }
                        for pino, aberto in estados.items():
                            mao.abrir_fechar(pino, int(aberto))

                cv2.imshow("Imagem", img)
                tecla = cv2.waitKey(1) & 0xFF
                if tecla in (ord("q"), 27):
                    break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        mao.fechar()

if __name__ == "__main__":
    executar()
