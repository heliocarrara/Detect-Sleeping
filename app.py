"""
Tkinter-based desktop UI for the drowsiness detector.

This module is responsible for:
    * Creating and arranging all Tkinter widgets (buttons, labels, sliders)
    * Managing the webcam lifecycle (open, close, release)
    * Calling the vision logic implemented in ``detection.DrowsinessDetector``
      on each frame and updating the UI accordingly.

The goal is to keep UI responsibilities here and computer-vision logic
inside ``detection.py`` so that the code is easier to read and maintain.
"""

import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from detection import DrowsinessDetector


class DetectorSonoApp:
    def __init__(self, window, window_title):
        """
        Build the UI, initialize state and start the Tkinter main loop.

        Parameters
        ----------
        window:
            Tk root window created by ``main.py``.
        window_title:
            Text displayed in the window title bar.
        """

        self.window = window
        self.window.title(window_title)

        self.camera_active = False
        self.vid = None
        # Object that encapsulates all MediaPipe and EAR logic.
        self.detector = DrowsinessDetector()

        # Top frame that holds the camera selector, start button and slider.
        self.top_frame = tk.Frame(window)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Camera selection dropdown. For now we just populate indices 0..4.
        tk.Label(self.top_frame, text="Selecionar Câmera:").pack(side=tk.LEFT)
        self.camera_selector = ttk.Combobox(self.top_frame, values=[f"Câmera {i}" for i in range(5)])
        self.camera_selector.current(0)
        self.camera_selector.pack(side=tk.LEFT, padx=5)

        # Button that starts or stops the webcam capture.
        self.btn_start = tk.Button(self.top_frame, text="Iniciar Câmera", width=15, command=self.toggle_camera)
        self.btn_start.pack(side=tk.LEFT, padx=5)

        # Slider that controls the EAR threshold used to decide when
        # the eyes are considered closed.
        tk.Label(self.top_frame, text="Sensibilidade (EAR):").pack(side=tk.LEFT, padx=(20, 5))
        self.slider_threshold = tk.Scale(self.top_frame, from_=0.15, to=0.40, resolution=0.01, orient=tk.HORIZONTAL, length=200)
        self.slider_threshold.set(0.25)
        self.slider_threshold.pack(side=tk.LEFT)

        # Label that will display the processed video frames.
        self.canvas_frame = tk.Label(window)
        self.canvas_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Status bar at the bottom of the window.
        self.status_label = tk.Label(window, text="Sistema pronto. Selecione a câmera e inicie.", font=("Arial", 14), fg="blue")
        self.status_label.pack(side=tk.BOTTOM, pady=20)

        # Start Tkinter's event loop. From this point on, the program
        # is event-driven and controlled by callbacks.
        self.window.mainloop()

    def process_frame(self):
        """
        Read a frame from the camera, run drowsiness detection and update UI.

        This method is called repeatedly using ``window.after`` while
        ``self.camera_active`` is True. It delegates all heavy computer
        vision work to ``self.detector`` and only handles converting the
        result to an image that Tkinter can show.
        """
        if not self.camera_active:
            return

        ret, frame = self.vid.read()
        if not ret:
            print("Erro ao ler frame.")
            return

        # Get current EAR threshold from the slider and send the frame
        # to the detector module.
        threshold = self.slider_threshold.get()
        processed_frame, ear_display, status_text, alarm_on = self.detector.process_frame(frame, threshold)

        # Convert the processed OpenCV BGR frame to a Tkinter-compatible image.
        img_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)

        # Keep a reference to avoid image being garbage-collected.
        self.canvas_frame.imgtk = imgtk
        self.canvas_frame.configure(image=imgtk)

        # Update the text in the bottom status bar.
        self.status_label.config(text=status_text, fg=("red" if alarm_on else "green"))

        if self.camera_active:
            self.window.after(10, self.process_frame)

    def toggle_camera(self):
        """
        Start or stop webcam capture depending on the current state.

        When starting:
            * Opens the selected camera index using OpenCV.
            * Updates the button label.
            * Schedules the first call to ``process_frame``.

        When stopping:
            * Stops the processing loop.
            * Releases the camera resource.
            * Clears the video area and updates the status label.
        """
        if self.camera_active:
            self.camera_active = False
            self.btn_start.config(text="Iniciar Câmera")
            self.status_label.config(text="Câmera parada.", fg="black")
            if self.vid:
                self.vid.release()
            self.canvas_frame.config(image="")
        else:
            try:
                cam_index = self.camera_selector.current()
                if cam_index < 0:
                    cam_index = 0

                self.vid = cv2.VideoCapture(cam_index)

                if not self.vid.isOpened():
                    raise ValueError("Não foi possível abrir a câmera selecionada.")

                # Flag that the camera is active and kick off the frame loop.
                self.camera_active = True
                self.btn_start.config(text="Parar Câmera")
                self.process_frame()
            except Exception as e:
                self.status_label.config(text=f"Erro: {e}", fg="red")
                print(f"[ERRO] {e}")

    def __del__(self):
        """
        Ensure that the camera resource is released when the object dies.

        This is a safety net in case the window is closed without
        calling ``toggle_camera`` to stop the capture explicitly.
        """
        if self.vid and self.vid.isOpened():
            self.vid.release()

