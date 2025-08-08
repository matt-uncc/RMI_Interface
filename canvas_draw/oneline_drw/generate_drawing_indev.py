import cv2
import mediapipe as mp
import numpy as np
import os
import networkx as nx
from skimage.morphology import skeletonize
from skimage.measure import label, regionprops
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

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

def donw_sample_points(points, step=5):
        return points[::step]
def filter_skeleton(skeleton, min_size=30):
    # Label connected components
    labeled = label(skeleton)
    filtered = np.zeros_like(skeleton)
    for region in regionprops(labeled):
        if region.area >= min_size:
            for coord in region.coords:
                filtered[coord[0], coord[1]] = 1
    return filtered    
    
def extract_path_from_image(img):
    gray = load_image(img)
    edges = detect_edges(gray)
    skeleton = skeletonize_image(edges)
    skeleton = filter_skeleton(skeleton, min_size=30)
    graph = build_graph(skeleton)
    all_paths = extract_all_paths(graph)
    result_paths = []
    for path in all_paths:
        points = np.array([[y, x] for x, y in path])
        down_sampled_points = down_sample_points(points)
        norm_path = normalize_and_center_points(down_sampled_points)
        result_paths.append(norm_path)
    print(f"[INFO] Extracted {len(result_paths)} separate paths.")
    return result_paths

def extract_all_paths(G):
    # Find all connected components
    components = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    all_paths = []
    for comp in components:
        nodes = list(comp.nodes)
        if not nodes:
            continue
        # Find the longest path in this component
        longest_path = []
        def dfs_path(start):
            path = nx.dfs_edges(comp, start)
            return [start] + [v for u, v in path]
        for start in nodes:
            path = dfs_path(start)
            if len(path) > len(longest_path):
                longest_path = path
        if len(longest_path) > 1:
            all_paths.append(longest_path)
    return all_paths

def extract_longest_path_from_image(img):
    gray = load_image(img)
    edges = detect_edges(gray)
    skeleton = skeletonize_image(edges)
    skeleton = filter_skeleton(skeleton, min_size=30)
    graph = build_graph(skeleton)
    longest_path = find_longest_path(graph)
    points = np.array([[y, x] for x, y in longest_path])
    down_sampled_points = down_sample_points(points)
    norm_path = normalize_and_center_points(down_sampled_points)
    print(f"[INFO] Extracted longest path with {len(norm_path)} points.")
    return norm_path

def extract_longest_path_from_face_mesh(image):
    results_face = face_mesh.process(image)
    graph = build_graph(results_face)
    longest_path = find_longest_path(graph)
    points = np.array([[y, x] for x, y in longest_path])
    down_sampled_points = down_sample_points(points)
    norm_path = normalize_and_center_points(down_sampled_points)
    print(f"[INFO] Extracted longest path from face mesh with {len(norm_path)} points.")
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
            mp_face_mesh = mp.solutions.face_mesh
            face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)
            results_face = face_mesh.process(image_rgb)

            mesh_paths = []
            if results_face.multi_face_landmarks:
                h, w, _ = frame.shape
                for face_landmarks in results_face.multi_face_landmarks:
                    feature_points = []
                    for idx in FEATURE_INDICES:
                        lm = face_landmarks.landmark[idx]
                        x, y = int(lm.x * w), int(lm.y * h)
                        feature_points.append([x, y])
                        cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
                    feature_points = np.array(feature_points)
                    norm_path = normalize_and_center_points(feature_points)
                    mesh_paths.append(norm_path)

            csv_path = r"C:\Users\Matt\Documents\robot_RMIU\RMI_Interface\canvas_draw\oneline_drw\csv\one_line_drawing_cleaned.csv"
            if os.path.exists(csv_path):
                os.remove(csv_path)
            # Save all mesh points as one block in the CSV
            with open(csv_path, "w") as f:
                for path in mesh_paths:
                    np.savetxt(f, path, delimiter=",", fmt="%.2f")
                    f.write("\n")
            plot_all_paths(mesh_paths, title="Eyes, Nose, and Mouth Features")
            print(f"[INFO] Saved {len(mesh_paths)} mesh paths to {csv_path}")
            break

    cap.release()
    cv2.destroyAllWindows()
    plot_all_paths(mesh_paths, title="Face Mesh Points")
    return mesh_paths

def plot_all_paths(paths, title="All Paths"):
    plt.figure(figsize=(8, 10))
    for path in paths:
        if len(path) > 1:
            plt.plot(path[:, 0], path[:, 1], marker='o')
    plt.gca().set_aspect('equal')
    plt.title(title)
    plt.axis('off')
    plt.show()

EYE_INDICES = list(range(36, 48))   # Both eyes
NOSE_INDICES = list(range(27, 36))  # Nose bridge and bottom
MOUTH_INDICES = list(range(48, 68)) # Outer and inner lips
FEATURE_INDICES = EYE_INDICES + NOSE_INDICES + MOUTH_INDICES


