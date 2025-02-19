import cv2
from pyzbar import pyzbar
import requests

def login_and_get_token():
    login_url = "https://mad-shop.onrender.com/api/auth/local"
    login_data = {
        "identifier": "vm1@shipping.com",
        "password": "123456"
    }
    response = requests.post(login_url, json=login_data)
    if response.status_code == 200:
        return response.json().get('jwt')
    else:
        print(f"Login failed: {response.status_code}")
        return None

def capture_and_decode_qr():
    
    cap = cv2.VideoCapture(0)

    token = login_and_get_token()
    if not token:
        print("Unable to proceed without authentication token.")
        return

    while True:
        ret, frame = cap.read()

        decoded_objects = pyzbar.decode(frame)

        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print(f"QR Code Data: {qr_data}")

            url = f"https://mad-shop.onrender.com/api/pickups/{qr_data}?populate=items"
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                print("Response Data:", response.json())
            else:
                print(f"Failed to fetch data: {response.status_code}")

            cap.release()
            cv2.destroyAllWindows()
            return

        cv2.imshow('QR Code Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
capture_and_decode_qr()
