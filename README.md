# Python Face Detector

A simple, self-contained face detection tool built with **Python + OpenCV**.
It detects human faces in photos (or a live webcam feed) and draws a
bounding box around each one.

No extra model download is required for the Haar cascade detector — the
classifier files are bundled directly in this project's `cascades/`
folder. Note: this uses OpenCV's `CascadeClassifier`, which requires
the `opencv-contrib-python` package (see Setup and Troubleshooting
below) rather than plain `opencv-python`.

## Setup

```bash
pip install -r requirements.txt
```

Requires Python 3.7+.

## Usage

### Detect faces in a single image

```bash
python face_detect.py --image path/to/photo.jpg
```

The result is saved to `output/detected_photo.jpg` by default. Use
`--output` to choose a different path:

```bash
python face_detect.py --image photo.jpg --output result.jpg
```

### Detect faces in every image in a folder

```bash
python face_detect.py --folder path/to/photos --output path/to/results
```

Supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`

### Live webcam detection

```bash
python face_detect.py --webcam
```

Press `q` to close the webcam window. (Requires a connected camera and
a local display — this mode won't work on a headless server.)

### Catch side-profile faces too

Add `--profile` to any of the commands above to also run a
side-profile face detector (slightly slower, but catches faces that
aren't looking straight at the camera):

```bash
python face_detect.py --image group_photo.jpg --profile
```

## How it works

1. The image is converted to grayscale and contrast-normalized
   (`cv2.equalizeHist`), which improves detection in uneven lighting.
2. OpenCV's Haar Cascade classifier scans the image at multiple scales
   to find face-like patterns.
3. Detected regions are drawn as green rectangles with a "Face" label,
   and the count of faces found is printed to the console.

## Notes & tips

- Haar cascades are fast and lightweight but can miss faces at extreme
  angles, low light, or heavy occlusion (masks, sunglasses). For higher
  accuracy on difficult images, consider swapping in a deep-learning
  model such as OpenCV's DNN face detector, MTCNN, or MediaPipe Face
  Detection — the `detect_faces()` function is written so it's easy to
  swap the detector.
- Adjust `scaleFactor` and `minNeighbors` in `face_detect.py` to
  trade off speed vs. accuracy (smaller `scaleFactor` and higher
  `minNeighbors` = more accurate but slower).

## Troubleshooting

### `AttributeError: module 'cv2' has no attribute 'CascadeClassifier'`

**Cause:** As of **OpenCV 5.0** (released mid-2026), the Haar cascade
face detector (`CascadeClassifier`) was moved out of the plain
`opencv-python` package and into `opencv-contrib-python`. If you `pip
install opencv-python` today, you'll get OpenCV 5.x without
`CascadeClassifier` — this is a packaging change, not a bug in your
setup, and not a Python-version problem.

**Fix:** install the contrib package instead:

```bash
pip uninstall opencv-python -y
pip install opencv-contrib-python
```

Then run the script again — no code changes needed.
`requirements.txt` in this project already points to
`opencv-contrib-python` for this reason.

The script also checks for this at startup and will print the exact
cause and fix instead of a raw traceback.

### Still broken after installing opencv-contrib-python?

This can happen if opencv-contrib-python doesn't yet have a prebuilt
wheel for a brand-new Python release. In that case, use Python 3.11
or 3.12, which are the most reliable versions for OpenCV right now:

```powershell
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

(macOS/Linux: `python3.12 -m venv venv && source venv/bin/activate`)

### Webcam window doesn't open / no camera found

- Make sure you're running this on the physical machine with the
  webcam attached (not a remote/cloud terminal).
- On Windows, check Settings → Privacy & Security → Camera → allow
  desktop apps to access the camera.
- If you have more than one camera, the default (index 0) might not
  be the right one — let us know and we can add a `--camera-index`
  option.

## Files

```
face-detector/
├── face_detect.py                              # Main script
├── requirements.txt                            # Dependencies
├── README.md                                   # This file
└── cascades/
    ├── haarcascade_frontalface_default.xml     # Frontal face model
    └── haarcascade_profileface.xml             # Side-profile face model
```
