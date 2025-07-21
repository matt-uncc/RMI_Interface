#!/usr/bin/env python
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize
import networkx as nx
import os

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")
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
    skeleton = (skeleton * 255).astype(np.uint8)
    return skeleton

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

def visualize_path(path, shape):
    canvas = np.zeros(shape, dtype=np.uint8)
    for x, y in path:
        canvas[x, y] = 255
    plt.imshow(canvas, cmap='gray')
    plt.title("One-Line Drawing")
    plt.axis('off')
    plt.show()

def main(image_path):
    print(f"[INFO] Loading image: {image_path}")
    gray = load_image(image_path)
    edges = detect_edges(gray)
    skeleton = skeletonize_image(edges)
    graph = build_graph(skeleton)
    longest_path = find_longest_path(graph)
    print(f"[INFO] Extracted {len(longest_path)} path points.")
    visualize_path(longest_path, gray.shape)
    return np.array(longest_path)

if __name__ == "__main__":
    IMAGE_PATH = r"C:\Users\Matt\Documents\robot_RMIU\RMI_Interface\oneline_drw\img\foreground_segmented.png"
    CSV_PATH = r"C:\Users\Matt\Documents\robot_RMIU\RMI_Interface\oneline_drw\csv\one_line_drawing.csv"

    pixel_path = main(IMAGE_PATH)

    # Delete the CSV file instead of saving
    if os.path.exists(CSV_PATH):
        print(f"[INFO] Deleting CSV: {CSV_PATH}")
        os.remove(CSV_PATH)
    else:
        print(f"[INFO] No CSV to delete at: {CSV_PATH}")
