## Drowsiness Detector (Look Eyes) / Detector de Sonolência (Look Eyes)

This project is a desktop application that uses the webcam and computer vision to detect driver drowsiness in real time. It tracks facial landmarks, computes the Eye Aspect Ratio (EAR) for both eyes, and raises an alert when the eyes remain closed for several consecutive frames.

Este projeto é uma aplicação desktop que usa a webcam e visão computacional para detectar sonolência do motorista em tempo real. Ele rastreia pontos faciais, calcula a razão de aspecto dos olhos (EAR) e dispara um alerta quando os olhos permanecem fechados por vários frames consecutivos.

---

### Features / Funcionalidades

- Real-time video capture using OpenCV  
- Face landmarks detection with MediaPipe Tasks (Face Landmarker)  
- Eye Aspect Ratio (EAR) based drowsiness detection  
- Tkinter GUI with:
  - Camera selection
  - Start/Stop camera button
  - Sensitivity slider (EAR threshold)
  - Status bar indicating current state (awake / drowsy)

- Captura de vídeo em tempo real com OpenCV  
- Detecção de pontos faciais com MediaPipe Tasks (Face Landmarker)  
- Detecção de sonolência baseada na razão de aspecto dos olhos (EAR)  
- Interface Tkinter com:
  - Seleção de câmera
  - Botão para iniciar/parar câmera
  - Slider de sensibilidade (limiar de EAR)
  - Barra de status indicando estado atual (acordado / sonolento)

---

### Requirements / Requisitos

- Python 3.12 (ou compatível com MediaPipe 0.10.x)  
- Sistema operacional: Windows (testado)  

Python packages / Pacotes Python:

- opencv-python  
- mediapipe  
- pillow  
- numpy  
- scipy  

---

### Setup / Configuração

#### 1. Clone the repository / Clone o repositório

```bash
git clone https://seu-usuario/seu-repositorio.git
cd look-eyes
```

*(Ajuste a URL acima para o repositório real após publicá-lo.)*  
*(Adjust the URL above to your actual repository after publishing.)*

#### 2. Create and activate virtual environment / Criar e ativar o ambiente virtual

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### 3. Install dependencies / Instalar dependências

```powershell
pip install --upgrade pip
pip install opencv-python mediapipe pillow numpy scipy
```

---

### Running the Application / Executando a Aplicação

With the virtual environment activated / Com o ambiente virtual ativado:

```powershell
python main.py
```

The main window will open with:  
- A camera selector (default index 0)  
- A button to start/stop the camera  
- A slider to adjust EAR sensitivity  
- A video area showing processed frames  
- A status bar indicating if drowsiness is detected  

A janela principal será aberta com:  
- Um seletor de câmera (índice padrão 0)  
- Um botão para iniciar/parar a câmera  
- Um slider para ajustar a sensibilidade do EAR  
- Uma área de vídeo mostrando os frames processados  
- Uma barra de status indicando se foi detectada sonolência  

---

### How It Works / Como Funciona

1. The application captures frames from the selected webcam.  
2. Each frame is resized to 640x480 and converted to RGB.  
3. MediaPipe Face Landmarker detects face landmarks (468 points).  
4. The eye landmarks are selected by index for left and right eyes.  
5. The Eye Aspect Ratio (EAR) is computed for each eye and averaged.  
6. If the EAR stays below the chosen threshold for a number of consecutive frames, the app triggers a drowsiness alert on the video frame and status bar.

1. A aplicação captura frames da webcam selecionada.  
2. Cada frame é redimensionado para 640x480 e convertido para RGB.  
3. O MediaPipe Face Landmarker detecta pontos faciais (468 pontos).  
4. Os pontos dos olhos esquerdo e direito são selecionados por índice.  
5. A razão de aspecto dos olhos (EAR) é calculada para cada olho e depois feita a média.  
6. Se o EAR permanecer abaixo do limiar escolhido por um número de frames consecutivos, a aplicação aciona um alerta de sonolência no frame de vídeo e na barra de status.

---

### Main Components / Componentes Principais

- `main.py`  
  - `DetectorSonoApp`: main Tkinter application class  
  - GUI setup (camera selector, buttons, slider, status label)  
  - MediaPipe Face Landmarker initialization  
  - `process_frame`: reads camera, runs detection, draws landmarks, computes EAR, updates UI  
  - `calculate_ear`: helper method to compute Eye Aspect Ratio  
  - `toggle_camera`: handles camera start/stop logic  

- `main.py`  
  - `DetectorSonoApp`: classe principal da aplicação Tkinter  
  - Configuração da GUI (seletor de câmera, botões, slider, status)  
  - Inicialização do MediaPipe Face Landmarker  
  - `process_frame`: lê a câmera, roda a detecção, desenha landmarks, calcula EAR, atualiza a interface  
  - `calculate_ear`: função auxiliar que calcula a razão de aspecto dos olhos  
  - `toggle_camera`: lógica para ligar/desligar a câmera  

---

### Notes / Observações

- The application currently downloads the `face_landmarker.task` model automatically if it is not found in the project directory.  
- Make sure you have a working webcam and that no other application is using it.  
- If you experience performance issues, try lowering the camera resolution or increasing the delay in the frame loop.

- A aplicação atualmente baixa o modelo `face_landmarker.task` automaticamente se ele não for encontrado no diretório do projeto.  
- Certifique-se de que você possui uma webcam funcional e que nenhum outro programa esteja usando a câmera.  
- Se houver problemas de desempenho, tente reduzir a resolução da câmera ou aumentar o atraso no loop de frames.

---

### License / Licença

Define the license you want to use for this project (MIT, Apache 2.0, etc.) and add the corresponding text here.

Defina a licença que deseja usar para este projeto (MIT, Apache 2.0, etc.) e adicione o texto correspondente aqui.

