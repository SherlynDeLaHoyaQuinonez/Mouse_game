# Se importan bibliotecas que se usaran en todo el codigo 
import cv2 # Para capturar imagenes de la camara web y procesarlas para rastrear las manos 
import mediapipe as mp # rastrear mano y posiciones de los dedos 
import numpy as np # Proporciona soporte para matrices de manera rapida 
import pyautogui # Controla el cursor del mouse y realiza clics 

# Se establecen alias para las funciones de mediapipe que se utilizan para dibujar la deteccion de las manos 
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Establece conexion con la camara de la computadora 

# Representa el color que tendra el cursor en la mano 
color_mouse_pointer = (255, 0, 255)

# Puntos de la pantalla, coordenadas de los puntos de la pantalla donde se iniciara el juego
SCREEN_GAME_X_INI = 200
SCREEN_GAME_Y_INI = 180
SCREEN_GAME_X_FIN = 200 + 740
SCREEN_GAME_Y_FIN = 180 + 420

# Calcula la relacion de aspecto de la pantalla juego, calcula dividiendo el ancho de la pantalla por su altura 
aspect_ratio_screen = (SCREEN_GAME_X_FIN - SCREEN_GAME_X_INI) / (SCREEN_GAME_Y_FIN - SCREEN_GAME_Y_INI)
print("aspect_ratio_screen:", aspect_ratio_screen) 

X_Y_INI = 100

# Toma 4 argumentos dentro de la funcion 
def calculate_distance(x1, y1, x2, y2):
    p1 = np.array([x1, y1])
    p2 = np.array([x2, y2])
    return np.linalg.norm(p1 - p2) # Crea dos elementos numpy y con np.linialg.norm calcula la longitud de un vector 

# Recibe como entrada esta funcion  
def detect_finger_down(hand_landmarks): # recibe como entrada los puntos clave de una mano detectada 
    finger_down = False
    color_base = (255, 0, 112)  # Inicializar con un valor predeterminado
    color_index = (255, 198, 82)
    
    # estas bases se usan multiplicando las coordenadas normalizadas de los landmarks por el ancho y la altura de la imagen entrada 
    x_base1 = int(hand_landmarks.landmark[0].x * width) # base de la mano
    y_base1 = int(hand_landmarks.landmark[0].y * height)

    x_base2 = int(hand_landmarks.landmark[9].x * width) # Base del dedo medio 
    y_base2 = int(hand_landmarks.landmark[9].y * height)

    x_index = int(hand_landmarks.landmark[8].x * width) # la punta del dedo indice 
    y_index = int(hand_landmarks.landmark[8].y * height)

    d_base = calculate_distance(x_base1, y_base1, x_base2, y_base2) # se están calculando las distancias entre los puntos de la mano identificados por sus coordenadas
    d_base_index = calculate_distance(x_base1, y_base1, x_index, y_index) # se utiliza para calcular la distancia entre dos puntos.

# Si la distancia del dedo indice es menor que la distancia base cambia de color 
    if d_base_index < d_base:
        finger_down = True
        color_base = (255, 0, 255)
        color_index = (255, 0, 255)
# Se dibujan circulos en las coordenadas con radio de 5 pixeles con grosor de 3 pixeles 
    cv2.circle (output, (x_base1, y_base1), 5, color_base, 2)
    cv2.circle (output, (x_index, y_index), 5, color_index, 2)
    cv2.line (output, (x_base1, y_base1), (x_base2, y_base2), color_base, 3)
    cv2.line (output, (x_base1, y_base1), (x_index, y_index), color_index, 3)
# la funcion retorna a un valor booleano e indica que el dedo indice esta hacia abajo 
    return finger_down


# inicia el detector de manos empezando la deteccion en tiempo real 
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5) as hands:
# se ejecuta continuamente mientras que la camara siga capturando imagenes 
    while True:
# si no lee ningun frame sale del bucle con un break 
        ret, frame = cap.read()
        if ret == False:
            break
# Se obtienen las dimensiones 
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1) # Se pone horizontalmente el frame 

        #Dibujando un area proporcionada a la del juego
        area_width = width - X_Y_INI * 2
        area_height = int(area_width / aspect_ratio_screen)
        aux_image = np.zeros(frame.shape, np.uint8)
# Crea un rectangulo azul en la imagen de entrada 
        aux_image = cv2.rectangle(aux_image, (X_Y_INI, X_Y_INI), (X_Y_INI + area_width, X_Y_INI + area_height), (255, 0, 0, 1)) # Se crea imagen inicializada en ceros y se dibuja un rectangulo sobre la imagen auxiliar 
        output =cv2.addWeighted(frame, 1, aux_image, 0.7, 0) # el resultado se almacena en la variable 
 
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = hands.process(frame_rgb) # Procesa la imagen rgb y se almacena en la variable 
        
# Contiene el ciclo principal del programa 
        if results.multi_hand_landmarks is not None: # Si es nulo se detectaron manos en el cuadro actual 
            for hand_landmarks in results.multi_hand_landmarks: # el ciclo itera sobre la mano detectada y procesa cada una de ellas 
                x = int(hand_landmarks.landmark[9].x * width)
                y = int(hand_landmarks.landmark[9].y * height)
                xm = np.interp(x, (X_Y_INI, X_Y_INI + area_width), (SCREEN_GAME_X_INI, SCREEN_GAME_X_FIN))
                ym = np.interp(y, (X_Y_INI, X_Y_INI + area_height), (SCREEN_GAME_Y_INI, SCREEN_GAME_Y_FIN))
                pyautogui.moveTo(int(xm), int(ym))
                if detect_finger_down (hand_landmarks): # Detecta si el dedo indice esta apuntando hacia abajo 
                    pyautogui.click() # y si es asi se emula un clic
                cv2.circle(output, (x, y), 10, color_mouse_pointer, 3) # se dibujan circulos en la ubicacion actual del dedo 
                cv2.circle(output, (x, y), 5, color_mouse_pointer, -1)
# muestra en ventanas separadas con los nombres respectivos 
        cv2.imshow('Frame', frame)
        cv2.imshow('output', output)
        if cv2.waitKey(1) & 0xFF == 27: # Se espera que el usuario presione ESC para salir del ciclo y este se rompa
            break
cap.release() # Se libera el objeto que se esta capturando en el video
cv2.destroyAllWindows() # Se cierran las ventanas abiertas con la funcion