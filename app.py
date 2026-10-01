import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# --- INITIALISATION MEDIAPIPE (Détection de la main) ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# --- CONFIGURATION DE LA FENÊTRE (CUTE & PIXEL) ---
root = tk.Tk()
root.title("✨ Cute Pixel Air Painter ✨")
root.geometry("900x700")
root.configure(bg="#ffb6c1")  # Rose pastel doux

# Header style pixel / cute
header_frame = tk.Frame(root, bg="#ff69b4", bd=4, relief="ridge")
header_frame.pack(fill=tk.X, padx=10, pady=10)

title_label = tk.Label(
    header_frame, 
    text="🌸 DESSINE AVEC TA MAIN 🌸", 
    font=("Courier New", 16, "bold"), 
    bg="#ff69b4", 
    fg="#ffffff"
)
title_label.pack(pady=5)

# Cadre pour la vidéo
canvas_frame = tk.Frame(root, bg="#ff1493", bd=4, relief="ridge")
canvas_frame.pack(padx=10, pady=5)

video_label = tk.Label(canvas_frame, bg="#fff0f5")
video_label.pack()

# Instructions footer
footer_label = tk.Label(
    root, 
    text="✨ Indice : Lève l'index pour dessiner, ferme le poing pour effacer ! ✨", 
    font=("Courier New", 10, "bold"), 
    bg="#ffb6c1", 
    fg="#8b008b"
)
footer_label.pack(pady=10)

# --- CAPTURE WEBCAM & VARIABLES DE DESSIN ---
cap = cv2.VideoCapture(0)
canvas = None
prev_x, prev_y = 0, 0

def update_frame():
    global canvas, prev_x, prev_y
    
    success, frame = cap.read()
    if not success:
        root.after(10, update_frame)
        return

    # Miroir horizontal pour plus de naturel
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    # Initialisation du calque de dessin aux dimensions de la vidéo
    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    # Conversion de l'image en RGB pour MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    drawing_color = (255, 105, 180) # Rose vif en BGR

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Récupérer la position de l'index (bout: landmark 8) et du pouce (landmark 4)
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            
            x, y = int(index_tip.x * w), int(index_tip.y * h)
            
            # Dessiner les landmarks de la main style kawaii
            mp_draw.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(color=(255, 192, 203), thickness=4, circle_radius=4),
                mp_draw.DrawingSpec(color=(255, 105, 180), thickness=2, circle_radius=2)
            )

            # Logique de dessin : si l'index bouge et qu'on est en mode actif
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = x, y

            # Distance simple entre index et pouce pour effacer (pincement)
            distance = np.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)
            
            if distance < 0.05:
                # Si les doigts se touchent -> Effacer le canvas
                canvas = np.zeros((h, w, 3), dtype=np.uint8)
            else:
                # Sinon on dessine une jolie ligne rose
                cv2.line(canvas, (prev_x, prev_y), (x, y), drawing_color, 8)

            prev_x, prev_y = x, y
    else:
        prev_x, prev_y = 0, 0

    # Fusionner l'image de la webcam et le calque de dessin
    # On ajoute une teinte rose pastel transparente à l'arrière-plan pour l'effet cute
    pink_tint = np.full(frame.shape, (255, 220, 240), dtype=np.uint8)
    frame = cv2.addWeighted(frame, 0.7, pink_tint, 0.3, 0)
    
    # Appliquer le dessin sur la vidéo
    frame = cv2.add(frame, canvas)

    # Conversion pour Tkinter
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    # Boucle de rafraîchissement (environ 30 FPS)
    root.after(10, update_frame)

# Lancer la boucle de l'application
root.after(10, update_frame)
root.mainloop()

# Libération des ressources à la fermeture
cap.release()
cv2.destroyAllWindows()