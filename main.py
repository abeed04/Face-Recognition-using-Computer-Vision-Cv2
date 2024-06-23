import cv2
import numpy as np
import face_recognition

video_capture = cv2.VideoCapture(0)

person1 = face_recognition.load_image_file('Dhoni.jpeg')
person2 = face_recognition.load_image_file('Virat-kohli.jpg')
person3 = face_recognition.load_image_file('Deepika Padukone.jpg')


p1_encoding = face_recognition.face_encodings(person1)[0]
p2_encoding = face_recognition.face_encodings(person2)[0]
p3_encoding = face_recognition.face_encodings(person3)[0]




known_face_encodings = [p1_encoding,p2_encoding,p3_encoding]
known_face_names = ['Dhoni', 'Virat', 'Deepika']

face_locations = []
face_encodings = []
s = True

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = np.ascontiguousarray((small_frame[:,:,::-1]))
    # actual part start here
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encodings,face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                y1, x2, y2, x1 = face_locations[0]  # TOP , RIGHT , BOTTOM , LEFT
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, name, (x1+6, y2-6), cv2.FONT_HERSHEY_PLAIN, 2, (120, 200, 255), 1)

    cv2.imshow('FaceRecognition',frame)
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
