import cv2
import time

font = cv2.FONT_HERSHEY_DUPLEX
fontScale = 0.75
orgin = (5, 30)
color = (0, 255, 0)
thickness = 1

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gauss = cv2.GaussianBlur(gray, (25, 25), 0)

    return gauss

def detect_motion(contours, hierarchy, num_return=1):
    contourSizes = [(c, cv2.contourArea(c)) for c in contours]
    contourSizes = sorted(contourSizes, key=lambda x: x[1], reverse=True)
    return contourSizes[:num_return]

cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)

dimensions_text = f'Dimensions: {width}x{height}'

fourcc = cv2.VideoWriter_fourcc(*'XVID')
writer = cv2.VideoWriter('detections.avi', fourcc, fps, (int(width), int(height)))

prev = None

while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    processed_frame = process_frame(frame)

    if prev is None:
        prev = processed_frame

    diff = cv2.absdiff(processed_frame, prev)
    threshold = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    dilated = cv2.dilate(threshold, None, iterations=2)

    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    sizes = detect_motion(contours, hierarchy, num_return=1)

    min_x, min_y = width, height
    max_x = max_y = 0

    # computes the bounding box for the contour, and draws it on the frame,
    for contour, size in sizes:
        if size > 8000:
            # (x,y,w,h) = cv2.boundingRect(contour)
            # min_x, max_x = min(x, min_x), max(x+w, max_x)
            # min_y, max_y = min(y, min_y), max(y+h, max_y)
            # if w > 80 and h > 80:
            #     cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)

            # elif max_x - min_x > 0 and max_y - min_y > 0:
            #     cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
            print(size)
            now = time.strftime("%H:%M:%S", time.localtime())
            # print(now)
            frame = cv2.putText(frame, now, orgin, font, fontScale, color, thickness, cv2.LINE_AA)
            writer.write(frame)

    diff = cv2.putText(frame, dimensions_text, orgin, font, fontScale, color, thickness, cv2.LINE_AA)
    
    # cv2.imshow('Spi', frame)
    cv2.imshow('Processed Frame', dilated)

    # prev = processed_frame

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
writer.release()