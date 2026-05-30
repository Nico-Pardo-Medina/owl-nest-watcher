# Owl Nest Watcher

A desktop GUI tool that processes batches of video files and produces a timestamped activity report for each one — logging exactly when movement starts and stops throughout the footage.

Originally built for wildlife biologists who needed to avoid watching hours of nest-camera recordings manually. Given a folder of overnight videos, the tool generates a text report per session showing when an owl entered and left the nest. The detection logic is general-purpose and works for any scenario where you need to know *when* something moved in a video, not just *whether* it did.

---

## How it works

For each video in the selected folder, the tool:

1. Samples frames at a configurable rate (not every frame — efficient on long recordings)
2. Applies brightness and contrast adjustments to handle poor or variable lighting conditions
3. Converts each sampled frame to grayscale and applies a Gaussian blur
4. Computes the absolute difference against a reference frame to detect pixel-level changes
5. Identifies contours above a minimum area threshold (filters out noise and small insects)
6. Logs the timestamp when activity begins and when it has been absent for long enough to count as stopped

All results are written to a single `.txt` report file with one entry per video.

---

## Requirements

```
pip install opencv-python imutils numpy
```

Tkinter is included with standard Python installations.

---

## Usage

```bash
python main.py
```

A GUI window will open. Set the parameters, select your folders, and click **Ejecutar** (Run).

---

## Parameters

| Parameter | Description | Default |
|---|---|---|
| **Nombre del archivo** | Output report filename (without extension) | `activity_log` |
| **Brillo** (Brightness) | Brightness adjustment applied before detection. Useful for dark footage | `50` |
| **Contraste** (Contrast) | Contrast multiplier applied before detection | `1.25` |
| **Velocidad** (Speed) | Frame sampling rate — `1` checks every frame at native FPS, `2` checks every other second, etc. Higher = faster but less precise | `1` |
| **Área mínima** (Min area) | Minimum contour area in pixels to count as movement. Filters out noise and small objects | `500` |
| **Tiempo sin actividad** | Seconds of inactivity required before logging that movement has stopped. Prevents brief pauses from splitting one event into many | `0` |

---

## Output

A `.txt` file in the selected output folder, with one section per video:

```
video_001.mp4:
No hay actividad: 0:00:00
Empieza a haber actividad: 0:04:32
Deja de haber actividad: 0:11:17
Empieza a haber actividad: 0:23:45
Acaba el vídeo: 1:02:10
```

---

## Origin

The tool was built to help biologists studying barn owls (*Tyto alba*) avoid manually reviewing hours of nest-box camera footage. The configurable inactivity threshold was added specifically to avoid logging brief exits as separate events — a requirement that emerged from understanding how owls actually move in and out of nests. Variable names like `owlIs` and `owlWas` in the source are a nod to the original use case.

---

## Limitations

- **GUI is in Spanish** — the interface uses Spanish labels reflecting the original user base.
- **One-way comparison** — motion is detected relative to the first frame of each video (background subtraction). Camera shake or lighting changes can affect accuracy.
- **Local files only** — processes video files on disk; no streaming support.
- **No GPU acceleration** — processing is CPU-bound; very long or high-resolution videos will be slow.
