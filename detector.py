import datetime
import os

import cv2
import imutils
import numpy as np


def process_videos(
    source_folder,
    output_folder,
    file_title,
    min_area,
    contrast,
    brightness,
    speed,
    time_that_has_to_pass,
    on_progress=None,
):
    """
    Process all video files in source_folder and write an activity report.

    For each video, logs the timestamps when movement starts and stops using
    frame-by-frame background subtraction. Brightness and contrast are applied
    before detection to handle variable lighting conditions such as infrared
    nest cameras.

    Args:
        source_folder: Path to the folder containing video files.
        output_folder: Path to the folder where the report .txt will be saved.
        file_title: Output filename without extension.
        min_area: Minimum contour area in pixels to count as movement.
        contrast: Contrast multiplier applied in HSV space before detection.
        brightness: Brightness offset applied in HSV space before detection.
        speed: Frame sampling rate — 1 checks every frame at native FPS,
               2 checks every other second, etc.
        time_that_has_to_pass: Seconds of inactivity before logging that
                               movement has stopped.
        on_progress: Optional callback(current, total) called once per video.
    """
    videos = os.listdir(source_folder)
    with open(f"{output_folder}/{file_title}.txt", "w") as f:
        for i, video_name in enumerate(videos):
            if on_progress:
                on_progress(i + 1, len(videos))
            f.write(f"{video_name}:\n")
            _process_single_video(
                os.path.join(source_folder, video_name),
                f,
                min_area,
                contrast,
                brightness,
                speed,
                time_that_has_to_pass,
            )


def _process_single_video(path, f, min_area, contrast, brightness, speed, time_that_has_to_pass):
    """Analyse a single video file and write activity timestamps to f."""
    vs = cv2.VideoCapture(path)
    if not vs.isOpened():
        f.write("El archivo no es un vídeo o no se puede abrir.\n\n")
        return

    fps = vs.get(cv2.CAP_PROP_FPS)
    firstFrame = None
    owlWas = False
    last_message = False
    time_without_change = 0
    frames = 1
    timestamp = "0:00:00"

    while True:
        _, frame = vs.read()
        if frame is None:
            break

        owlIs = False

        if firstFrame is None:
            frames -= 1
            last_message = False
            time_without_change = 0

        frames += 1
        time_without_change += 1

        if (frames - 1) % (fps * speed) == 0:
            frame = imutils.resize(frame, width=500)
            new_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            new_image[:, :, 2] = np.clip(contrast * new_image[:, :, 2] + brightness, 0, 255)
            new_image = cv2.cvtColor(new_image, cv2.COLOR_HSV2BGR)
            gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            duration = max(0, frames / fps) - 0.04
            timestamp = str(datetime.timedelta(seconds=duration))

            if firstFrame is None:
                firstFrame = gray
                owlWas = False
                f.write(f"No hay actividad: {timestamp}\n")

            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.dilate(
                cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1],
                None,
                iterations=2,
            )
            for c in imutils.grab_contours(
                cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            ):
                if cv2.contourArea(c) >= min_area:
                    owlIs = True
                    break

            if owlIs != owlWas:
                time_without_change = 0
                if owlIs and not last_message:
                    f.write(f"Empieza a haber actividad: {timestamp}\n")
                    last_message = True

            if not owlIs and time_without_change > fps * time_that_has_to_pass and last_message:
                f.write(f"Deja de haber actividad: {timestamp}\n")
                last_message = False

            owlWas = owlIs

    vs.release()
    f.write(f"Acaba el vídeo: {timestamp}\n\n")
