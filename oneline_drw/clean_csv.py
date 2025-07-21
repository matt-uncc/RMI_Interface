import numpy as np
import matplotlib.pyplot as plt

def load_points_from_csv(csv_path):
    points = np.loadtxt(csv_path, delimiter=',')
    down_sampled_points = points[::15]  # downsample
    return down_sampled_points


def normalize_and_center_points(points, target_width=180.0, target_height=240.0, margin_x=40.0, margin_y=40.0):
    # Step 1: Shift to origin
    min_xy = np.min(points, axis=0)
    points_shifted = points - min_xy

    # Step 2: Scale to fit target dimensions (keep aspect ratio)
    max_xy = np.max(points_shifted, axis=0)
    width, height = max_xy[0], max_xy[1]
    scale = min(target_width / width, target_height / height)
    points_scaled = points_shifted * scale

    # Step 3: Rotate 90° clockwise around the center
    center = np.mean(points_scaled, axis=0)
    rotated = np.zeros_like(points_scaled)
    rotated[:, 0] = points_scaled[:, 1] - center[1] 
    rotated[:, 1] = -(points_scaled[:, 0] - center[0]) 
    rotated += center  # shift back

    # Step 4: Center in the target area
    final_min = np.min(rotated, axis=0)
    final_max = np.max(rotated, axis=0)
    final_width = final_max[0] - final_min[0]
    final_height = final_max[1] - final_min[1]

    offset_x = margin_x + (target_width - final_width) / 2 - final_min[0]
    offset_y = margin_y + (target_height - final_height) / 2 - final_min[1]

    centered = rotated + np.array([offset_x, offset_y])
    return centered



def nearest_neighbor_path(points):
    n = len(points)
    print(f"Total points: {n}")
    visited = [False] * n
    path = []

    current_idx = 0  # start from first point
    path.append(points[current_idx])
    visited[current_idx] = True

    for _ in range(n - 1):
        current_point = points[current_idx]
        dists = np.linalg.norm(points - current_point, axis=1)
        dists = [d if not visited[i] else np.inf for i, d in enumerate(dists)]
        next_idx = np.argmin(dists)
        path.append(points[next_idx])
        visited[next_idx] = True
        current_idx = next_idx

    return np.array(path)

def plot_path(points, path):
    plt.figure(figsize=(10, 8))
    plt.scatter(points[:, 0], points[:, 1], color='red', label='Original Points')

    for idx, (x, y) in enumerate(path):
        plt.text(x, y, str(idx), fontsize=6, color='blue')

    plt.plot(path[:, 0], path[:, 1], color='blue', linewidth=1, label='Path')
    plt.axis('equal')
    plt.legend()
    plt.title("One-Line Path Scaled and Centered to A4")
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    csv_path = r"C:\Users\Matt\Documents\robot_RMIU\RMI_Interface\oneline_drw\csv\one_line_drawing.csv"
    points = load_points_from_csv(csv_path)
    
    # Fit to A4 printable area with 20mm margin
    centered_points = normalize_and_center_points(points)

    path = nearest_neighbor_path(centered_points)

    np.savetxt(
        r"C:\Users\Matt\Documents\robot_RMIU\RMI_Interface\oneline_drw\csv\one_line_drawing_clean.csv",
        path, delimiter=',', fmt='%.2f'
    )

    plot_path(centered_points, path)
