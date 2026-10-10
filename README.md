# Mao robotica controlada por gestos no Windows

Projeto de controle de uma mao robotica usando a camera de um tablet, MediaPipe,
Python e um Arduino com o firmware Firmata Standard. O tablet deve aparecer no
Windows como uma webcam. O programa nao acessa diretamente a camera do tablet
pela rede: use um aplicativo que crie uma webcam virtual no Windows.

## 1. Materiais

- Arduino compativel com Firmata.
- Cinco servomotores.
- Tablet com camera e aplicativo de webcam para Windows.
- Fonte externa adequada para os servomotores.
- Fios e estrutura mecanica da mao robotica.

### Alimentacao dos servos

Nao alimente cinco servos pelo pino `5V` do Arduino. Use uma fonte externa
dimensionada para os motores e conecte o `GND` da fonte ao `GND` do Arduino.
Com o Arduino desligado, conecte o fio de sinal de cada servo conforme a tabela:

| Dedo | Pino digital | Funcao no codigo |
| --- | ---: | --- |
| Polegar | 10 | `abrir_fechar(10, estado)` |
| Indicador | 9 | `abrir_fechar(9, estado)` |
| Medio | 8 | `abrir_fechar(8, estado)` |
| Anelar | 7 | `abrir_fechar(7, estado)` |
| Minimo | 6 | `abrir_fechar(6, estado)` |

O fio de sinal normalmente e amarelo ou laranja. Consulte o fabricante do seu
servo para identificar `VCC`, `GND` e `sinal` antes de ligar.

## 2. Gravar o Firmata no Arduino

1. Instale e abra o [Arduino IDE](https://www.arduino.cc/en/software).
2. Conecte o Arduino por USB sem conectar ainda a alimentacao externa dos servos.
3. No IDE, abra **Arquivo > Exemplos > Firmata > StandardFirmata**.
4. Em **Ferramentas > Placa**, selecione o modelo correto do Arduino.
5. Em **Ferramentas > Porta**, selecione a porta USB do Arduino.
6. Clique em **Carregar** e aguarde a mensagem de conclusao.
7. Feche o Monitor Serial do Arduino IDE antes de executar o Python, pois apenas
	 um programa pode usar a porta serial por vez.

O Firmata e gravado uma vez. Depois disso, o Python envia os angulos dos servos
pela porta USB.

## 3. Preparar o Python 3.12 no Windows

Instale o Python 3.12 ou mais recente pelo site oficial:

https://www.python.org/downloads/windows/

Durante a instalacao, marque **Add python.exe to PATH**. Depois abra o PowerShell
e confirme a versao:

```bash
python --version
```

Entre na pasta do projeto e crie um ambiente virtual no PowerShell:

```powershell
cd caminho\para\mao-robotica-mediapipe-main
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

Atualize o instalador e instale as bibliotecas:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

As bibliotecas usadas são OpenCV, MediaPipe, pyFirmata e pySerial.

## 4. Fazer o tablet funcionar como camera

Escolha um aplicativo que transforme a camera do tablet em webcam para o
Windows, como DroidCam ou Iriun Webcam. Instale o aplicativo no tablet e o
cliente correspondente no Windows, seguindo as instrucoes do aplicativo.

1. Conecte o tablet ao Windows por USB ou pela mesma rede Wi-Fi, conforme o
	aplicativo escolhido.
2. Abra o aplicativo no tablet e o cliente no Windows.
3. Autorize o acesso a camera e confirme que a imagem aparece no cliente.
4. Abra o aplicativo **Camera** do Windows e verifique se a imagem do tablet
	aparece como uma camera disponivel.
5. Feche o aplicativo Camera antes de iniciar o Python, para liberar o acesso.

O projeto usa por padrao a camera de indice `0`. Se o tablet tiver outro indice,
defina `CAMERA_INDEX` no PowerShell. Os indices normalmente comecam em `0`:

```powershell
$env:CAMERA_INDEX = "1"
```

Se nao souber o indice, teste `0`, `1`, `2` e assim por diante ate a janela
`Imagem` mostrar o tablet.

## 5. Identificar a porta serial

O programa tenta detectar automaticamente o Arduino. Se houver mais de uma
porta serial, informe a porta manualmente. Descubra a porta em **Gerenciador de
Dispositivos > Portas (COM e LPT)** e execute no PowerShell:

```powershell
$env:SERVO_PORT = "COM3"
python testar-dedos.py
```

## 6. Testar os dedos sem camera

Antes de usar o MediaPipe, conecte a fonte dos servos e execute:

```bash
python testar-dedos.py
```

O programa coloca todos os servos na posicao inicial e, em seguida, movimenta
cada dedo individualmente, fechando e abrindo um de cada vez. Ao final, mostra:
`Teste dos dedos concluido.`

Mantenha as maos afastadas da estrutura durante o primeiro teste. Se algum servo
forcar o mecanismo, desligue a alimentacao e ajuste a montagem ou os angulos em
`servo_braco3d.py`.

## 7. Executar o controle pela camera do tablet

1. Posicione o tablet de frente para a mao.
2. Deixe boa iluminacao e mantenha apenas uma mao visivel.
3. Abra o aplicativo do tablet e confirme a imagem no Windows.
4. Conecte o Arduino e a fonte dos servos.
5. Feche qualquer programa que esteja usando a camera ou a porta serial.
6. Execute:

```powershell
python main.py
```

Com a porta do Arduino e a camera definidas manualmente:

```powershell
$env:SERVO_PORT = "COM3"
$env:CAMERA_INDEX = "1"
python main.py
```

Uma janela chamada `Imagem` mostrara a camera e os pontos detectados pelo
MediaPipe. Os dedos levantados comandam os servos na posicao aberta; dedos
abaixados comandam a posicao fechada.

Pressione `q` ou `Esc` na janela da camera para encerrar. O programa libera a
webcam e fecha a conexao com o Arduino automaticamente.

## 7. Solucao de problemas

### Arduino nao encontrado

- Confirme o cabo USB e a porta selecionada no Arduino IDE.
- Feche o Monitor Serial e outros programas que usam a porta.
- Defina `SERVO_PORT` manualmente.

### Camera nao abre

- Confirme que o cliente do aplicativo do tablet esta aberto no Windows.
- Verifique se a imagem aparece no aplicativo Camera do Windows.
- Feche o aplicativo Camera e outros programas que possam estar usando a camera.
- Teste outro indice com `$env:CAMERA_INDEX = "0"`, depois `"1"` ou `"2"`.
- Verifique as permissoes em **Configuracoes > Privacidade e seguranca > Camera**.

### Servos tremem ou Arduino reinicia

- Use fonte externa apropriada para os servos.
- Una o `GND` da fonte externa ao `GND` do Arduino.
- Nao conecte a alimentacao dos motores invertida.

### Movimento invertido ou limite incorreto

Os angulos de abertura e fechamento dependem da montagem mecanica. Ajuste
`ANGULOS_FECHADO` em `servo_braco3d.py` e teste novamente com:

```bash
python testar-dedos.py
```
