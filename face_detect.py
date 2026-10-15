import os, sys, cv2

# 1) Load cascade (own folder first, then OpenCV's built-in copy)
here = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(here, "haarcascade_frontalface_default.xml")
if not os.path.exists(path):
    path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(path)
print("OpenCV version:", cv2.__version__)
print("Cascade loaded:", not cascade.empty())

# 2) Find a working camera (tries several indexes and backends)
if sys.platform.startswith("win"):
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
elif sys.platform == "darwin":
    backends = [cv2.CAP_AVFOUNDATION, cv2.CAP_ANY]
else:
    backends = [cv2.CAP_V4L2, cv2.CAP_ANY]

cam = None
for be in backends:
    for i in range(4):
        c = cv2.VideoCapture(i, be)
        if c.isOpened():
            for _ in range(10):          # let the camera warm up
                ok, frame = c.read()
            if ok and frame is not None:
                print(f"Camera found: index={i}, backend={be}")
                cam = c
                break
        c.release()
    if cam:
        break

if cam is None:
    sys.exit("NO CAMERA FOUND. Close Zoom/Teams/browser tabs using the camera, "
             "check OS camera permission for your terminal/editor, then retry.")

# 3) Detect and display
while True:
    ok, frame = cam.read()
    if not ok:
        print("Lost camera frame")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(frame, f"Faces: {len(faces)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    try:
        cv2.imshow("Face Detection (q to quit)", frame)
    except cv2.error as e:
        cv2.imwrite("snapshot.jpg", frame)
        sys.exit("Cannot show a window (" + str(e).splitlines()[0] + ").\n"
                 "Saved snapshot.jpg instead. Fix: pip uninstall opencv-python-headless, "
                 "then pip install opencv-python")
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()