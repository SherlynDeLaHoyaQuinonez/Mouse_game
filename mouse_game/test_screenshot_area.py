import cv2
import numpy as np
import pyautogui

# Bucle que se ejecuta continuamente hasta que el usuario presione ESC 

while True: 
    screenshot = pyautogui.screenshot(region=(200, 180, 740, 420)) # Captura una captura de pantalla de la zona de juego definida 
    screenshot = np.array(screenshot) # Se convierte la captura en un objeto de matriz numpy 
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR) # y se cambia el espacio de color RGB a BGR 
    cv2.imshow("screenshot", screenshot)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows() # Se cierra la ventana