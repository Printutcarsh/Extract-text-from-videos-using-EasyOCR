import easyocr
import cv2

#Download pre-trained model
reader = easyocr.Reader(['en'])

cap = cv2.VideoCapture("Moving_pipe_OCR.mp4")

while cap.isOpened():
    _, frame = cap.read()
    #From here these are some few steps which might not be required for different videos
    frame2 = cv2.flip(frame, -1)

    #Creating a region of interest as the text is very small in this video
    x1 = int(0.5*frame2.shape[0])
    y1 = 10
    x2 = frame2.shape[0] + 150
    y2 = int(0.35*frame2.shape[0])

    roi = frame2[y1:y2, x1:x2]
    roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    #The readtext function will return a list which will contain bounding box, text and confident level
    # Also, here I have applied this function to the roi only but in other
    # case you can directly apply it to the frame
    output = reader.readtext(roi)

    #If we set detail=0 then we will only get text
    text = reader.readtext(roi, detail=0)

    #This if-else condition is useful for this video only for better results
    #Directly jump to for loop for other videos
    if len(output)>1:
        if (len(text)==4):
            for i in range(len(output)):

                #To draw bounding box we take the coordinates of bounding box
                cord = output[i][0]

                x_min, y_min = [min(idx) for idx in zip(*cord)]
                x_max, y_max = [max(idx) for idx in zip(*cord)]
                cv2.rectangle(roi, (x_min, y_min), (x_max, y_max), (255,0,0), 1)

                cv2.putText(roi,str(text), (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,255), 2)
                cv2.imshow("roi", roi)
                cv2.imshow("frame", frame)
        else:
            cv2.imshow("roi", roi)
            cv2.imshow("frame", frame)

    else:
        cv2.imshow("roi", roi)
        cv2.imshow("frame", frame)

    if cv2.waitKey(40) == 27:
        break

cap.release()
cv2.destroyAllWindows()
