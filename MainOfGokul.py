import cv2
import numpy as np
import time
net = cv2.dnn.readNet("weights/yolov3.weights", "yolov3.cfg")
classes = ["Weapon"]
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i- 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))
font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time() - 11
running = True
cap = cv2.VideoCapture(0)
if running == False:
    cv2.destroyAllWindows()
flag=0
while running:
    ret, frame = cap.read()
    if ret:
        height, width, channels = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
				# Evaluating detections
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                                        # If detection confidance is above 98% a weapon was detected
                if confidence > 0.5:

							# Calculating coordinates
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
							# Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.6, 0.4)

				#Draw boxes around detected objects
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                color = (256, 0, 0)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label + " {0:.1%}".format(confidence), (x, y - 20), font, 3, color, 3)
                elapsed_time = starting_time - time.time()

						#Save detected frame every 10 seconds
                if elapsed_time <= -10:
                    starting_time = time.time()
                    cv2.imwrite("saved_frame/frame.jpg", frame)
                    print('Frame Saved')
                    import smtplib,email 
                    from email.message import EmailMessage
                    msg = EmailMessage()
                    msg.set_content("Your chair is ready to sit")
                    #Enter user path of saved frame 
                    with open("[Enter_Your_Saved_Frame_Path]", "rb") as fp:
                        msg.add_attachment(fp.read(), maintype="image", subtype="jpg")
                    msg['subject'] = "Weapon detected!"
                    msg['to'] = "[YOUR_MAIL_ID]" # change this mail id to who you want to send the mail
                    
                    user = "minorproject002@gmail.com" #dont change this mail id 
                    msg['from'] = user
                    password = "bflvgiwtazakvktc"
                    server =smtplib.SMTP("smtp.gmail.com",587)
                    server.starttls()
                    server.login(user, password)
                    server.send_message(msg)
                    server.quit()
                    # do a bit of cleanup
                    flag=1
                    
    if flag==1:
        break
    else:
        pass
    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('Object Detection ', frame)
    cv2.waitKey(1)
cv2.destroyAllWindows()
cap.release()
