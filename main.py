import cv2
import numpy as np
from scipy.spatial import distance as dist
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os
import urllib.request
from mediapipe import Image as MpImage, ImageFormat
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

# =============================================================================
# CLASSE PRINCIPAL DA APLICAÇÃO
# =============================================================================
class DetectorSonoApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # ---------------------------------------------------------------------
        # CONFIGURAÇÕES DE DETECÇÃO (CONSTANTES E VARIÁVEIS)
        # ---------------------------------------------------------------------
        # Índices dos marcos faciais (Landmarks) do MediaPipe para os olhos
        # O MediaPipe mapeia o rosto em 468 pontos. Estes são os dos olhos.
        self.LEFT_EYE_IDXS = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE_IDXS = [362, 385, 387, 263, 373, 380]
        
        # Variáveis de Estado
        self.counter = 0            # Contador de frames consecutivos com olho fechado
        self.alarm_on = False       # Estado do alarme (visual)
        self.consec_frames = 15     # Quantos frames seguidos para disparar o alerta (aprox 0.5s a 30fps)
        self.camera_active = False  # Se a câmera está ligada ou não
        self.vid = None             # Objeto de captura de vídeo do OpenCV

        self.model_path = "face_landmarker.task"
        if not os.path.exists(self.model_path):
            url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task"
            urllib.request.urlretrieve(url, self.model_path)
        base_options = mp_python.BaseOptions(model_asset_path=self.model_path)
        options = mp_vision.FaceLandmarkerOptions(
            base_options=base_options,
            num_faces=1,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
        )
        self.face_mesh = mp_vision.FaceLandmarker.create_from_options(options)

        # ---------------------------------------------------------------------
        # INTERFACE GRÁFICA (LAYOUT)
        # ---------------------------------------------------------------------
        
        # --- PAINEL DE CONTROLE SUPERIOR ---
        self.top_frame = tk.Frame(window)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # 1. Dropdown (Combobox) para seleção de Câmera
        tk.Label(self.top_frame, text="Selecionar Câmera:").pack(side=tk.LEFT)
        self.camera_selector = ttk.Combobox(self.top_frame, values=[f"Câmera {i}" for i in range(5)])
        self.camera_selector.current(0) # Seleciona a 0 por padrão
        self.camera_selector.pack(side=tk.LEFT, padx=5)

        # 2. Botão de Iniciar/Parar
        self.btn_start = tk.Button(self.top_frame, text="Iniciar Câmera", width=15, command=self.toggle_camera)
        self.btn_start.pack(side=tk.LEFT, padx=5)

        # 3. Slider (Scale) de Sensibilidade (EAR Threshold)
        # Permite ajustar em tempo real o quão fechado o olho precisa estar
        tk.Label(self.top_frame, text="Sensibilidade (EAR):").pack(side=tk.LEFT, padx=(20, 5))
        self.slider_threshold = tk.Scale(self.top_frame, from_=0.15, to=0.40, resolution=0.01, orient=tk.HORIZONTAL, length=200)
        self.slider_threshold.set(0.25) # Valor padrão comum
        self.slider_threshold.pack(side=tk.LEFT)

        # --- ÁREA DE VÍDEO (CANVAS) ---
        # É aqui que a imagem processada será desenhada
        self.canvas_frame = tk.Label(window)
        self.canvas_frame.pack(side=tk.TOP, padx=10, pady=10)

        # --- BARRA DE STATUS INFERIOR ---
        self.status_label = tk.Label(window, text="Sistema pronto. Selecione a câmera e inicie.", font=("Arial", 14), fg="blue")
        self.status_label.pack(side=tk.BOTTOM, pady=20)

        # Inicia o loop principal da janela Tkinter
        self.window.mainloop()

    # =========================================================================
    # LÓGICA DE VISÃO COMPUTACIONAL
    # =========================================================================
    
    def calculate_ear(self, eye_landmarks):
        """
        Calcula a Razão de Aspecto do Olho (EAR - Eye Aspect Ratio).
        Fórmula baseada no paper de Soukupová & Čech (2016).
        EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
        """
        # Distâncias verticais (pálpebras)
        A = dist.euclidean(eye_landmarks[1], eye_landmarks[5])
        B = dist.euclidean(eye_landmarks[2], eye_landmarks[4])
        # Distância horizontal (canto a canto)
        C = dist.euclidean(eye_landmarks[0], eye_landmarks[3])

        # Evita divisão por zero
        if C == 0: return 0
        
        ear = (A + B) / (2.0 * C)
        return ear

    def process_frame(self):
        """
        Captura frame, processa IA, atualiza UI e agenda o próximo frame.
        """
        if not self.camera_active:
            return

        # 1. Leitura da Câmera
        ret, frame = self.vid.read()
        if not ret:
            print("Erro ao ler frame.")
            return

        # 2. Pré-processamento
        # O OpenCV usa BGR, mas o MediaPipe e o Tkinter preferem RGB
        frame = cv2.resize(frame, (640, 480))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = MpImage(image_format=ImageFormat.SRGB, data=rgb_frame)
        results = self.face_mesh.detect(mp_image)
        
        # Variável para desenhar na tela (EAR atual)
        ear_display = 0.0
        status_text = "Olhos Abertos"
        status_color = (0, 255, 0) # Verde no formato RGB

        if results.face_landmarks:
            for face_landmarks in results.face_landmarks:
                h, w, _ = frame.shape
                points = np.array([[int(l.x * w), int(l.y * h)] for l in face_landmarks])

                # Extrai coordenadas dos olhos
                left_eye = points[self.LEFT_EYE_IDXS]
                right_eye = points[self.RIGHT_EYE_IDXS]

                # Desenha os olhos no frame (feedback visual para o usuário)
                # cv2 desenha em BGR, então usamos cores BGR aqui
                cv2.polylines(frame, [left_eye], True, (0, 255, 0), 1)
                cv2.polylines(frame, [right_eye], True, (0, 255, 0), 1)

                # Calcula EAR
                leftEAR = self.calculate_ear(left_eye)
                rightEAR = self.calculate_ear(right_eye)
                ear_display = (leftEAR + rightEAR) / 2.0

                # Pega o valor atual do Slider da Interface
                threshold = self.slider_threshold.get()

                # 5. Lógica de Detecção de Sonolência
                if ear_display < threshold:
                    self.counter += 1
                    if self.counter >= self.consec_frames:
                        self.alarm_on = True
                        status_text = "ALERTA: SONO DETECTADO!"
                        status_color = (255, 0, 0) # Vermelho
                        
                        # Texto na imagem do vídeo
                        cv2.putText(frame, "ACORDE!", (200, 240), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                else:
                    self.counter = 0
                    self.alarm_on = False

        # 6. Conversão para Tkinter
        # Adiciona overlay de texto com dados técnicos
        color_bgr = (0, 255, 0) if not self.alarm_on else (0, 0, 255)
        cv2.putText(frame, f"EAR: {ear_display:.2f}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_bgr, 2)
        
        # Converte a imagem final (com desenhos) para formato compatível com Tkinter
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)

        # Atualiza o Canvas
        self.canvas_frame.imgtk = imgtk
        self.canvas_frame.configure(image=imgtk)
        
        # Atualiza label de status inferior
        self.status_label.config(text=status_text, fg=("red" if self.alarm_on else "green"))

        # 7. Loop
        # Agenda a execução desta mesma função em 10ms (gera ~30-60 FPS dependendo da CPU)
        if self.camera_active:
            self.window.after(10, self.process_frame)

    # =========================================================================
    # CONTROLE DE HARDWARE
    # =========================================================================

    def toggle_camera(self):
        """
        Liga ou desliga a webcam baseada no estado atual.
        """
        if self.camera_active:
            # Desligar
            self.camera_active = False
            self.btn_start.config(text="Iniciar Câmera")
            self.status_label.config(text="Câmera parada.", fg="black")
            if self.vid:
                self.vid.release()
            self.canvas_frame.config(image='') # Limpa a imagem
        else:
            # Ligar
            try:
                # Pega o índice do dropdown (ex: "Câmera 1" -> index 1)
                cam_index = self.camera_selector.current()
                if cam_index < 0: cam_index = 0 # Fallback
                
                self.vid = cv2.VideoCapture(cam_index)
                
                if not self.vid.isOpened():
                    raise ValueError("Não foi possível abrir a câmera selecionada.")
                
                self.camera_active = True
                self.btn_start.config(text="Parar Câmera")
                self.process_frame() # Inicia o loop
            except Exception as e:
                self.status_label.config(text=f"Erro: {e}", fg="red")
                print(f"[ERRO] {e}")

    def __del__(self):
        """
        Destrutor: Garante que a câmera seja liberada ao fechar o app.
        """
        if self.vid and self.vid.isOpened():
            self.vid.release()

# =============================================================================
# PONTO DE ENTRADA (MAIN)
# =============================================================================
if __name__ == "__main__":
    try:
        # Cria a janela raiz
        root = tk.Tk()
        # Inicializa a aplicação
        app = DetectorSonoApp(root, "Detector de Sonolência v1.0")
    except KeyboardInterrupt:
        sys.exit()
