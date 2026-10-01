import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import random


# init de mediapipe pour detection de la main

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils



# config de la fenetre pour le coté rose mimi

root = tk.Tk()

root.title("✨ Cute Pixel Air Painter ✨")

root.geometry("900x700")

root.configure(bg="#ffb6c1")



# header

header_frame = tk.Frame(
    root,
    bg="#ff69b4",
    bd=4,
    relief="ridge"
)

header_frame.pack(
    fill=tk.X,
    padx=10,
    pady=10
)


title_label = tk.Label(
    header_frame,
    text="🌸 DESSINE AVEC TA MAIN 🌸",
    font=("Courier New",16,"bold"),
    bg="#ff69b4",
    fg="white"
)

title_label.pack(pady=5)



# cadre vidéo

canvas_frame = tk.Frame(
    root,
    bg="#ff1493",
    bd=4,
    relief="ridge"
)

canvas_frame.pack(
    padx=10,
    pady=5
)


video_label = tk.Label(
    canvas_frame,
    bg="#fff0f5"
)

video_label.pack()



# Instructions

footer_label = tk.Label(
    root,
    text="✋ Effacer | ✌️ Bloquer | 🤏 Déplacer | 🖕 Paillettes",
    font=("Courier New",10,"bold"),
    bg="#ffb6c1",
    fg="#8b008b"
)

footer_label.pack(pady=10)




# webcame et dessins

cap = cv2.VideoCapture(0)


canvas = None


# Position précédente du doigt

prev_x = 0
prev_y = 0



# variables a ajouter pour les ouveau settings de mouvements


# Etat du verrouillage

drawing_locked = False


# Evite que le peace sign active 30 fois

previous_peace = False



# déplacement du dessin

dragging = False

drag_start_x = 0
drag_start_y = 0



# liste des paillettes

particles = []




# detection des doigts

def detect_fingers(hand_landmarks):

    lm = hand_landmarks.landmark


    fingers = []


    # Index, majeur, annulaire, auriculaire

    tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]


    pips = [
        mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP,
        mp_hands.HandLandmark.PINKY_PIP
    ]



    for tip,pip in zip(tips,pips):

        if lm[tip].y < lm[pip].y:
            fingers.append(True)

        else:
            fingers.append(False)



    # Pouce

    if lm[
        mp_hands.HandLandmark.THUMB_TIP
    ].x > lm[
        mp_hands.HandLandmark.THUMB_IP
    ].x:

        fingers.insert(0,True)

    else:

        fingers.insert(0,False)



    return fingers

# maj de la cam

def update_frame():

    global canvas
    global prev_x, prev_y
    global drawing_locked
    global previous_peace
    global dragging
    global drag_start_x, drag_start_y
    global particles


    # Lire la caméra

    success, frame = cap.read()

    if not success:

        root.after(10, update_frame)
        return



    # Effet miroir

    frame = cv2.flip(frame,1)


    h,w,c = frame.shape



    # création du calque de dessin

    if canvas is None:

        canvas = np.zeros(
            (h,w,3),
            dtype=np.uint8
        )



    # Conversion pour MediaPipe

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    result = hands.process(rgb_frame)



    # detection de la main

    if result.multi_hand_landmarks:


        hand_landmarks = result.multi_hand_landmarks[0]


        # dessiner les points de la main

        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_draw.DrawingSpec(
                color=(255,192,203),
                thickness=4,
                circle_radius=4
            ),
            mp_draw.DrawingSpec(
                color=(255,105,180),
                thickness=2
            )
        )



        # Position de l'index

        index_tip = hand_landmarks.landmark[
            mp_hands.HandLandmark.INDEX_FINGER_TIP
        ]


        x = int(index_tip.x*w)

        y = int(index_tip.y*h)



        fingers = detect_fingers(hand_landmarks)



        # --- MAIN OUVERTE = EFFACER ---

        hand_open = all(fingers)


        if hand_open:


            canvas = np.zeros(
                (h,w,3),
                dtype=np.uint8
            )



        # peace pour lock

        peace = (
            fingers[1]
            and fingers[2]
            and not fingers[3]
            and not fingers[4]
        )


        if peace and not previous_peace:

            drawing_locked = not drawing_locked


        previous_peace = peace



        if drawing_locked:

            cv2.putText(
                frame,
                "DRAW LOCKED",
                (30,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,0,255),
                3
            )



        # doigt te3 noss pailletes

        middle_only = (
            fingers[2]
            and not fingers[1]
            and not fingers[3]
            and not fingers[4]
        )


        if middle_only:


            for i in range(8):

                particles.append(
                    [
                        x,
                        y,
                        random.randint(-5,5),
                        random.randint(-5,5),
                        30
                    ]
                )



        # pincement pour dep le dessin

        thumb_tip = hand_landmarks.landmark[
            mp_hands.HandLandmark.THUMB_TIP
        ]


        distance = np.hypot(
            index_tip.x-thumb_tip.x,
            index_tip.y-thumb_tip.y
        )



        if distance < 0.05:


            if not dragging:

                dragging = True

                drag_start_x = x

                drag_start_y = y



            else:

                dx = x - drag_start_x

                dy = y - drag_start_y



                matrix = np.float32(
                    [
                        [1,0,dx],
                        [0,1,dy]
                    ]
                )


                canvas = cv2.warpAffine(
                    canvas,
                    matrix,
                    (w,h)
                )


                drag_start_x = x

                drag_start_y = y



        else:

            dragging = False



        # dessin indexe

        if (
            not drawing_locked
            and not hand_open
            and distance >= 0.05
        ):


            if prev_x == 0 and prev_y == 0:

                prev_x = x

                prev_y = y



            cv2.line(
                canvas,
                (prev_x,prev_y),
                (x,y),
                (255,105,180),
                8
            )


            prev_x = x

            prev_y = y



    else:

        prev_x = 0
        prev_y = 0




    # paillettes

    for p in particles:


        p[0] += p[2]

        p[1] += p[3]

        p[4] -= 1



        cv2.circle(
            frame,
            (p[0],p[1]),
            5,
            (
                random.randint(150,255),
                random.randint(100,255),
                255
            ),
            -1
        )



    particles = [
        p for p in particles
        if p[4] > 0
    ]



    # dessin sur video

    frame = cv2.add(
        frame,
        canvas
    )



    # Conversion pour Tkinter

    frame_rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    img = Image.fromarray(frame_rgb)


    imgtk = ImageTk.PhotoImage(
        image=img
    )


    video_label.imgtk = imgtk

    video_label.configure(
        image=imgtk
    )



    root.after(
        10,
        update_frame
    )





#fermeture propre zhma

def close_app():

    cap.release()

    cv2.destroyAllWindows()

    root.destroy()



root.protocol(
    "WM_DELETE_WINDOW",
    close_app
)



#lancement

root.after(
    10,
    update_frame
)


root.mainloop()