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
    # Open the built-in camera
    cap = cv2.VideoCapture(0)

    # Login and get JWT token
    token = login_and_get_token()
    if not token:
        print("Unable to proceed without authentication token.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Find and decode QR codes in the frame
        decoded_objects = pyzbar.decode(frame)

        for obj in decoded_objects:
            # Extract the data from the QR code
            qr_data = obj.data.decode('utf-8')
            print(f"QR Code Data: {qr_data}")

            # Resolve data from the URL using the JWT token
            url = f"https://mad-shop.onrender.com/api/pickups/{qr_data}?populate=items"
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                # Print the response data
                print("Response Data:", response.json())
            else:
                print(f"Failed to fetch data: {response.status_code}")

            # Break the loop after processing the first QR code
            cap.release()
            cv2.destroyAllWindows()
            return

        # Display the resulting frame
        cv2.imshow('QR Code Scanner', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_decode_qr()