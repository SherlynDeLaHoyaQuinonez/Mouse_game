import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

color_mouse_pointer = (255, 0, 255)

# Puntos de la pantalla 
SCREEN_GAME_X_INI = 200
SCREEN_GAME_X_INI = 180
SCREEN_GAME_X_FIN = 200 + 740
SCREEN_GAME_X_FIN = 180 + 420



with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5) as hands:
    
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                x = int(hand_landmarks.landmark[9].x * width)
                y = int(hand_landmarks.landmark[9].y * height)
                
                cv2.circle(frame, (x, y), 10, color_mouse_pointer, 3)
                cv2.circle(frame, (x, y), 5, color_mouse_pointer, -1)
        
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()
         