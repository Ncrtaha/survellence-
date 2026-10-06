import cv2
import time
import requests

API_URL = "https://7107.api.greenapi.com"
ID_INSTANCE = "710722748118"
API_TOKEN = "79bec6b75f914403bf2df793b4cca1707cf4fa5e5c874c80a1"

PHONE_NUMBER = "212755892454@c.us"

def send_whatsapp_image(image_path, caption_text):
    try:
        url = f"{API_URL}/waInstance{ID_INSTANCE}/sendFileByUpload/{API_TOKEN}"
        
        payload = {
            'chatId': PHONE_NUMBER,
            'caption': caption_text
        }
        
        with open(image_path, 'rb') as file:
            files = [('file', (image_path, file, 'image/jpeg'))]
            response = requests.post(url, data=payload, files=files)
        
        if response.status_code == 200:
            print("Photo w message WhatsApp tsifto b naja7 !")
        else:
            print(f"Erreur d'envoi Green API (Code {response.status_code}):", response.text)
    except Exception as e:
        print("Erreur :", e)

cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

last_alert_time = 0
cooldown_seconds = 60

try:
    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            motion_detected = True
            break

        current_time = time.time()
        if motion_detected and (current_time - last_alert_time > cooldown_seconds):
            print("Mouvement détecté !")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            image_filename = f"alert_{timestamp}.jpg"
            
            # Sauvegarde de l'image
            cv2.imwrite(image_filename, frame1)

            # Envoi de l'image + du message
            msg = f"bana chi hd rah daz men nhna hdi krk \nDate : {timestamp}"
            send_whatsapp_image(image_filename, msg)

            last_alert_time = current_time

        frame1 = frame2
        ret, frame2 = cap.read()

        if not ret:
            break

        if cv2.waitKey(10) & 0xFF == ord('q'):
            print("Arrêt du programme par l'utilisateur.")
            break

except KeyboardInterrupt:
    print("\nProgramme interrompu proprement.")

finally:
    cap.release()
    cv2.destroyAllWindows()