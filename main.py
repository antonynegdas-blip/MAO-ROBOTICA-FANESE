import cv2
import mediapipe as mp
import servo_braco3d as mao

LARGURA = 640
ALTURA = 480

def abrir_camera():
    backend = cv2.CAP_DSHOW if hasattr(cv2, "CAP_DSHOW") and __import__("sys").platform == "win32" else cv2.CAP_ANY
    cap = cv2.VideoCapture(0, backend)
    if not cap.isOpened():
        cap.release()
        raise RuntimeError("Nao foi possivel abrir a camera. Verifique o indice ou a permissao do dispositivo.")
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

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

cap.set(3,640)
cap.set(4,480)

hands = mp.solutions.hands
Hands = hands.Hands(max_num_hands=1)
mpDwaw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    frameRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = Hands.process(frameRGB)
    handPoints = results.multi_hand_landmarks
    h, w, _ = img.shape
    pontos = []
    if handPoints:
        for points in handPoints:
            mpDwaw.draw_landmarks(img, points,hands.HAND_CONNECTIONS)
            #podemos enumerar esses pontos da seguinte forma
            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x * w), int(cord.y * h)
                # cv2.putText(img, str(id), (cx, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                cv2.circle(img,(cx,cy),4,(255,0,0),-1)
                pontos.append((cx,cy))

            if pontos:
                distPolegar = abs(pontos[17][0] - pontos[4][0])
                distIndicador = pontos[5][1] - pontos[8][1]
                distMedio = pontos[9][1] - pontos[12][1]
                distAnelar = pontos[13][1] - pontos[16][1]
                distMinimo = pontos[17][1] - pontos[20][1]

                # print(distPolegar)

                if distPolegar <80:

                    mao.abrir_fechar(10,0)
                else:
                    mao.abrir_fechar(10,1)

                if distIndicador >=1:
                    mao.abrir_fechar(9,1)
                else:
                    mao.abrir_fechar(9,0)

                if distMedio >=1:
                    mao.abrir_fechar(8,1)
                else:
                    mao.abrir_fechar(8,0)

                if distAnelar >=1:
                    mao.abrir_fechar(7,1)
                else:
                    mao.abrir_fechar(7,0)

                if distMinimo >=1:
                    mao.abrir_fechar(6,1)
                else:
                    mao.abrir_fechar(6,0)


    cv2.imshow('Imagem',img)
    cv2.waitKey(1)
