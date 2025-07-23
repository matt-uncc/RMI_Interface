import cv2
import mediapipe as mp
import numpy as np
import os
import networkx as nx
from skimage.morphology import skeletonize
from concurrent.futures import ThreadPoolExecutor

# Initialize MediaPipe Selfie Segmentation
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

def load_image(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def detect_edges(gray_image):
    return cv2.adaptiveThreshold(
        gray_image, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2)

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
    def dfs_path(start):
        path = nx.dfs_edges(G, start)
        return [start] + [v for u, v in path]

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(dfs_path, nodes))

    for path in results:
        if len(path) > len(longest_path):
            longest_path = path
    return longest_path

def down_sample_points(points, step=5):
    return points[::step]

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

def extract_path_from_image(img):
    gray = load_image(img)
    edges = detect_edges(gray)
    skeleton = skeletonize_image(edges)
    graph = build_graph(skeleton)
    longest_path = find_longest_path(graph)
    points = np.array([[y, x] for x, y in longest_path])
    down_sampled_points = down_sample_points(points)
    print(f"[INFO] Extracted {len(down_sampled_points)} path points after downsampling.")
    norm_path = normalize_and_center_points(down_sampled_points)
    return norm_path

def capture_and_process_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    print("Press SPACE to capture image, ESC to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.namedWindow('Webcam Feed', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Webcam Feed', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)    
        cv2.imshow('Webcam Feed', frame)
        key = cv2.waitKey(1)

        if key == 27:  # ESC
            break
        elif key == 32:  # SPACE
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = segmentation.process(image_rgb)
            mask = results.segmentation_mask
            condition = mask > 0.6

            bg_image = np.ones(frame.shape, dtype=np.uint8) * 255
            segmented_image = np.where(condition[:, :, None], frame, bg_image)

            output_dir = r"C:\Users\Matt\Documents\robot_RMIU\RMI_Interface\canvas_draw\oneline_drw\img"
            os.makedirs(output_dir, exist_ok=True)
            img_path = os.path.join(output_dir, "foreground_segmented.png")
            cv2.imwrite(img_path, segmented_image)

            final_path = extract_path_from_image(segmented_image)

            csv_path = r"C:\Users\Matt\Documents\robot_RMIU\RMI_Interface\canvas_draw\oneline_drw\csv\one_line_drawing_cleaned.csv"
            if os.path.exists(csv_path):
                os.remove(csv_path)
            np.savetxt(csv_path, final_path, delimiter=",", fmt="%.2f")
            print(f"[INFO] Saved path to {csv_path}")
            break

    cap.release()
    cv2.destroyAllWindows()
    return final_path
