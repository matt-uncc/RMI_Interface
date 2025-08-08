import cv2
import mediapipe as mp
import numpy as np
import os
import networkx as nx
from skimage.morphology import skeletonize
import matplotlib.pyplot as plt

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

        def load_image(image):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return gray

        def detect_edges(gray_image):
            edges = cv2.adaptiveThreshold(
                gray_image, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV,
                11, 2)
            return edges

        def skeletonize_image(edges):
            _, binary = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY)
            skeleton = skeletonize(binary // 255)
            return (skeleton * 255).astype(np.uint8)

        def build_graph(skeleton):
            G = nx.Graph()
            h, w = skeleton.shape
            for i in range(h):
                for j in range(w):
                    if skeleton[i, j] > 0:
                        G.add_node((i, j))
                        for di in [-1, 0, 1]:
                            for dj in [-1, 0, 1]:
                                if (di != 0 or dj != 0) and 0 <= i + di < h and 0 <= j + dj < w:
                                    if skeleton[i + di, j + dj] > 0:
                                        G.add_edge((i, j), (i + di, j + dj))
            return G

        def find_longest_path(G):
            nodes = list(G.nodes)
            longest_path = []
            for start in nodes:
                path = nx.dfs_edges(G, start)
                path = [start] + [v for u, v in path]
                if len(path) > len(longest_path):
                    longest_path = path
            return longest_path

        def normalize_and_center_points(points, target_width=180.0, target_height=240.0, margin_x=40.0, margin_y=40.0):
            min_xy = np.min(points, axis=0)
            points_shifted = points - min_xy
            max_xy = np.max(points_shifted, axis=0)
            width, height = max_xy[0], max_xy[1]
            scale = min(target_width / width, target_height / height)
            points_scaled = points_shifted * scale

            center = np.mean(points_scaled, axis=0)
            rotated = np.zeros_like(points_scaled)
            rotated[:, 0] = points_scaled[:, 1] - center[1]
            rotated[:, 1] = -(points_scaled[:, 0] - center[0])
            rotated += center

            final_min = np.min(rotated, axis=0)
            final_max = np.max(rotated, axis=0)
            final_width = final_max[0] - final_min[0]
            final_height = final_max[1] - final_min[1]

            offset_x = margin_x + (target_width - final_width) / 2 - final_min[0]
            offset_y = margin_y + (target_height - final_height) / 2 - final_min[1]

            centered = rotated + np.array([offset_x, offset_y])
            return centered

        
        
        def plot_path(points, title="Path"):
            plt.figure(figsize=(8, 10))
            plt.plot(points[:, 0], points[:, 1], '-o', linewidth=1, markersize=2, color='blue')
            plt.gca().invert_yaxis()  # Match image coordinates
            plt.axis('equal')
            plt.title(title)
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
            
            
        def process(segmented_image):
            gray = load_image(segmented_image)
            edges = detect_edges(gray)
            skeleton = skeletonize_image(edges)
            # Display the skeleton image
            cv2.imshow("Skeleton", skeleton)
            cv2.waitKey(0)
            cv2.destroyWindow("Skeleton")
            graph = build_graph(skeleton)
            longest_path = find_longest_path(graph)
            points = np.array([[y, x] for x, y in longest_path])  # convert to (x, y)
            norm_path = normalize_and_center_points(points)
            plot_path(norm_path, title="One-Line Drawing Path")
            return norm_path
        
       

        output_dir = r"C:\Users\Matt\Documents\robot_RMIU\RMI_Interface\oneline_drw\img"
        os.makedirs(output_dir, exist_ok=True)
        img_path = os.path.join(output_dir, "foreground_segmented.png")
        cv2.imwrite(img_path, segmented_image)

        # Face Mesh processing
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)
        results_face = face_mesh.process(image_rgb)

        if results_face.multi_face_landmarks:
            for face_landmarks in results_face.multi_face_landmarks:
                h, w, _ = segmented_image.shape
                for lm in face_landmarks.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)
                    cv2.circle(segmented_image, (x, y), 1, (0, 0, 255), -1)  # Red dots for face features

        final_path = process(segmented_image)

        csv_path = r"C:\Users\Matt\Documents\robot_RMIU\RMI_Interface\oneline_drw\csv\one_line_drawing_cleaned.csv"
        if os.path.exists(csv_path):
            os.remove(csv_path)
        np.savetxt(csv_path, final_path, delimiter=",", fmt="%.2f")
        print(f"[INFO] Saved path to {csv_path}")
        break

cap.release()
cv2.destroyAllWindows()