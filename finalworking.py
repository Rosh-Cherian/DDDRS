import cv2
import time
import serial
from geopy.geocoders import Nominatim
import geocoder
from twilio.rest import Client

arduino_port = 'COM3'
baud_rate = 9600
try:
    arduino = serial.Serial(port=arduino_port, baudrate=baud_rate)
    print(f"Connected to Arduino on port {arduino_port} at {baud_rate} baud")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

def get_current_location():
    geolocator = Nominatim(user_agent="eye_tracking_app")
    g = geocoder.ip('me')
    curr_loc = f"{8.4700516}, {76.9802530}"
    print(curr_loc)
    location = geolocator.geocode(curr_loc, language="en")
    return location.address if location else "Location not available"

account_sid = 'SID'
auth_token = 'token'
client = Client(account_sid, auth_token)
emergency_contact = 'mynumber'

def send_twilio_message(message, location):
    client.messages.create(
        body=f"{message}\nLocation: {location}",
        from_='+19292389660',
        to=emergency_contact
    )

eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
last_eye_detected_time = time.time()
FIRST_ALERT_TIME = 5
SECOND_ALERT_TIME = 10
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(eyes) > 0:
        last_eye_detected_time = time.time()
        arduino.write(b'0')
        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)  # Yellow color
        if len(eyes) == 0:
            cv2.putText(frame, 'Eyes Closed', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'Eyes Open', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    if time.time() - last_eye_detected_time > FIRST_ALERT_TIME:
        print("Sleep Alert")
        arduino.write(b'1')
    if time.time() - last_eye_detected_time > SECOND_ALERT_TIME:
        print("Danger")
        current_location = get_current_location()
        #send_twilio_message("Emergency: Eyes not detected for more than 10 seconds", current_location)
        break
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()