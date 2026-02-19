## Detect-Sleeping – English

### Overview

This project is a desktop application that uses the webcam and computer vision to detect driver drowsiness in real time.  
It tracks facial landmarks, computes the Eye Aspect Ratio (EAR) for both eyes, and raises an alert when the eyes remain closed for several consecutive frames.

The UI is built with Tkinter, while OpenCV and MediaPipe are used for video capture and face landmark detection.

---

### Features

- Real-time video capture using OpenCV  
- Face landmarks detection with MediaPipe Tasks (Face Landmarker)  
- Eye Aspect Ratio (EAR) based drowsiness detection  
- Tkinter GUI with:
  - Camera selection
  - Start/Stop camera button
  - Sensitivity slider (EAR threshold)
  - Status bar indicating current state (awake / drowsy)
- Automatic download of the `face_landmarker.task` model if it is not found locally

---

### Requirements

- Python 3.12 (or compatible with MediaPipe 0.10.x)  
- Operating system: Windows (tested)  

Python packages (see `requirements.txt` for exact versions):

- opencv-python  
- mediapipe  
- pillow  
- numpy  
- scipy  
- and related dependencies of these libraries  

---

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/heliocarrara/Detect-Sleeping.git
cd Detect-Sleeping
```

#### 2. Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` at the beginning of your terminal prompt after activation.

#### 3. Install dependencies

Recommended (using `requirements.txt`):

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Alternative (install only core libraries manually):

```powershell
pip install --upgrade pip
pip install opencv-python mediapipe pillow numpy scipy
```

---

### Running the Application

With the virtual environment activated:

```powershell
python main.py
```

The main window will open with:  
- A camera selector (default index 0)  
- A button to start/stop the camera  
- A slider to adjust EAR sensitivity  
- A video area showing processed frames  
- A status bar indicating if drowsiness is detected  
<img width="754" height="667" alt="image" src="https://github.com/user-attachments/assets/610b254d-09e6-447d-b6ba-1a9bffc23896" />
<img width="744" height="660" alt="image" src="https://github.com/user-attachments/assets/9cb0c566-430a-4fc6-8970-d9c36681d471" />

---

### How It Works

1. The application captures frames from the selected webcam.  
2. Each frame is resized to 640×480 and converted to RGB.  
3. MediaPipe Face Landmarker detects face landmarks (468 points).  
4. The eye landmarks are selected by index for left and right eyes.  
5. The Eye Aspect Ratio (EAR) is computed for each eye and averaged.  
6. If the EAR stays below the chosen threshold for a number of consecutive frames, the app triggers a drowsiness alert on the video frame and status bar.

Internally, the logic is implemented in the `DetectorSonoApp` class in `main.py`.

---

### Project Structure (simplified)

- `main.py`  
  - `DetectorSonoApp`: main Tkinter application class  
  - GUI setup (camera selector, buttons, slider, status label)  
  - MediaPipe Face Landmarker initialization and model download  
  - `process_frame`: reads camera, runs detection, draws landmarks, computes EAR, updates UI  
  - `calculate_ear`: helper method to compute the Eye Aspect Ratio  
  - `toggle_camera`: handles camera start/stop logic  
- `requirements.txt` – pinned Python dependencies  
- `.gitignore` – excludes `.venv`, build artifacts, and the model file  
- `README.md` – project documentation (English and Portuguese)  

---

### Notes

- The application automatically downloads the `face_landmarker.task` model to the project root if it is not found.  
- Make sure you have a working webcam and that no other application is using it.  
- If you experience performance issues, try:
  - lowering the camera resolution, or  
  - increasing the delay in the frame loop.  

---

### License

Define the license you want to use for this project (MIT, Apache 2.0, etc.) and add the corresponding text here.

---

## Detect-Sleeping – Português

### Visão Geral

Este projeto é uma aplicação desktop que usa a webcam e visão computacional para detectar sonolência do motorista em tempo real.  
Ele rastreia pontos faciais, calcula a razão de aspecto dos olhos (EAR) e dispara um alerta quando os olhos permanecem fechados por vários frames consecutivos.

A interface é construída com Tkinter, enquanto o OpenCV e o MediaPipe são usados para captura de vídeo e detecção de pontos faciais.

---

### Funcionalidades

- Captura de vídeo em tempo real com OpenCV  
- Detecção de pontos faciais com MediaPipe Tasks (Face Landmarker)  
- Detecção de sonolência baseada na razão de aspecto dos olhos (EAR)  
- Interface Tkinter com:
  - Seleção de câmera
  - Botão para iniciar/parar câmera
  - Slider de sensibilidade (limiar de EAR)
  - Barra de status indicando estado atual (acordado / sonolento)
- Download automático do modelo `face_landmarker.task` caso ele não exista localmente

---

### Requisitos

- Python 3.12 (ou compatível com MediaPipe 0.10.x)  
- Sistema operacional: Windows (testado)  

Pacotes Python (consulte `requirements.txt` para versões exatas):

- opencv-python  
- mediapipe  
- pillow  
- numpy  
- scipy  
- e dependências relacionadas a essas bibliotecas  

---

### Instalação

#### 1. Clonar o repositório

```bash
git clone https://github.com/heliocarrara/Detect-Sleeping.git
cd Detect-Sleeping
```

#### 2. Criar e ativar o ambiente virtual

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Você deve ver `(.venv)` no início do prompt do terminal após a ativação.

#### 3. Instalar dependências

Recomendado (usando `requirements.txt`):

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Alternativa (instalar apenas bibliotecas principais manualmente):

```powershell
pip install --upgrade pip
pip install opencv-python mediapipe pillow numpy scipy
```

---

### Execução da Aplicação

Com o ambiente virtual ativado:

```powershell
python main.py
```

A janela principal será aberta com:  
- Um seletor de câmera (índice padrão 0)  
- Um botão para iniciar/parar a câmera  
- Um slider para ajustar a sensibilidade do EAR  
- Uma área de vídeo mostrando os frames processados  
- Uma barra de status indicando se foi detectada sonolência  

---

### Como Funciona

1. A aplicação captura frames da webcam selecionada.  
2. Cada frame é redimensionado para 640×480 e convertido para RGB.  
3. O MediaPipe Face Landmarker detecta pontos faciais (468 pontos).  
4. Os pontos dos olhos esquerdo e direito são selecionados por índice.  
5. A razão de aspecto dos olhos (EAR) é calculada para cada olho e, depois, feita a média.  
6. Se o EAR permanecer abaixo do limiar escolhido por um número de frames consecutivos, a aplicação aciona um alerta de sonolência no frame de vídeo e na barra de status.

Internamente, essa lógica é implementada na classe `DetectorSonoApp` em `main.py`.

---

### Estrutura do Projeto (simplificada)

- `main.py`  
  - `DetectorSonoApp`: classe principal da aplicação Tkinter  
  - Configuração da GUI (seletor de câmera, botões, slider, status)  
  - Inicialização do MediaPipe Face Landmarker e download do modelo  
  - `process_frame`: lê a câmera, roda a detecção, desenha os pontos, calcula EAR, atualiza a interface  
  - `calculate_ear`: função auxiliar que calcula a razão de aspecto dos olhos  
  - `toggle_camera`: lógica para ligar/desligar a câmera  
- `requirements.txt` – dependências Python com versões fixadas  
- `.gitignore` – exclui `.venv`, artefatos de build e o arquivo de modelo  
- `README.md` – documentação do projeto (inglês e português)  

---

### Observações

- A aplicação baixa automaticamente o modelo `face_landmarker.task` para a raiz do projeto se ele não for encontrado.  
- Certifique-se de que você possui uma webcam funcional e que nenhum outro programa esteja usando a câmera.  
- Se houver problemas de desempenho, tente:
  - diminuir a resolução da câmera, ou  
  - aumentar o atraso no loop de processamento dos frames.  

---

### Licença

Defina a licença que deseja usar para este projeto (MIT, Apache 2.0, etc.) e adicione o texto correspondente aqui.
