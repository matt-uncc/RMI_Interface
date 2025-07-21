import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize
import networkx as nx
import os



# Initialize MediaPipe Selfie Segmentation
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

print("Press SPACE to capture image, ESC to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.imshow('Webcam Feed', frame)
    key = cv2.waitKey(1)

    if key == 27:  # ESC key to quit
        break
    elif key == 32:  # SPACE key to capture
        # Convert to RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run segmentation
        results = segmentation.process(image_rgb)
        mask = results.segmentation_mask
        condition = mask > 0.6

        # Create white background
        bg_image = np.ones(frame.shape, dtype=np.uint8) * 255

        # Apply mask
        segmented_image = np.where(condition[:, :, None], frame, bg_image)

        # Save result
        import os
        output_dir = r"C:\Users\Matt\Documents\robot_RMIU\RMI_Interface\oneline_drw\img"
        os.makedirs(output_dir, exist_ok=True)
        cv2.imwrite(os.path.join(output_dir, "foreground_segmented.png"), segmented_image)
        print("Saved: foreground_segmented.png")
        break

cap.release()
cv2.destroyAllWindows()
