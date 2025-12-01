import cv2
import numpy as np
import os
import sys
import open3d as o3d

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.SFM import (
    detect_and_match_features,
    estimate_pose,
    triangulate_points,
    estimate_K_from_exif
)
from services.point_cloude import (
    estimate_normals,
    generate_poisson_mesh,
    crop_mesh_by_density,
    get_colors_from_image
)

from services.cut_object import remove_background_from_folder

DB = r"C:\Users\OWNER\Desktop\programming\convert 3D\conerting\DB"
folder = r"C:\Users\OWNER\Desktop\programming\convert 3D\convert3D\dl\images"
OUTPUT_MESH_PATH = r"C:\Users\OWNER\Desktop\programming\convert 3D\convert3D\dl\output\colored_mesh.ply"


def load_images_from_folder(folder):
    images = []
    image_paths = []
    for filename in sorted(os.listdir(folder)):
        path = os.path.join(folder, filename)
        img = cv2.imread(path)
        if img is not None:
            images.append(img)
            image_paths.append(path)
    return images, image_paths

sift = cv2.SIFT_create()

def generate_3d_model(images_folder, output_path):
    images, image_paths = load_images_from_folder(images_folder)

    if len(images) < 2:
        raise Exception("Need at least 2 images for SfM")

    # remove_background_from_folder(folder, output_folder=folder)

    K = estimate_K_from_exif(image_paths[0])
    all_pts3d = []
    all_colors = []

    for i in range(len(images) - 1):
            img1 = images[i]
            img2 = images[i + 1]

            pts1, pts2 = detect_and_match_features(img1, img2, sift)

            if len(pts1) < 5 or len(pts2) < 5:
                print(f"Skipping image pair {i} due to insufficient matches.")
                continue

            R, t = estimate_pose(K, pts1, pts2)
            pts3d = triangulate_points(K, R, t, pts1, pts2)
            all_pts3d.append(pts3d)

            colors1 = get_colors_from_image(img1, pts1)
            colors2 = get_colors_from_image(img2, pts2)
            colors = (colors1 + colors2) / 2
            all_colors.append(colors)

    pts1, pts2 = detect_and_match_features(images[-1], images[0], sift)
    if len(pts1) < 5 or len(pts2) < 5:
        print(f"Skipping image pair (last and first) due to insufficient matches.")
    else:
        R, t = estimate_pose(K, pts1, pts2)
        pts3d = triangulate_points(K, R, t, pts1, pts2)
        all_pts3d.append(pts3d)
        colors = get_colors_from_image(images[-1], pts1)
        all_colors.append(colors)


    if len(all_pts3d) == 0:
        raise Exception("No valid point clouds were created.")

    merged_pts3d = np.vstack(all_pts3d)
    merged_colors = np.vstack(all_colors)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(merged_pts3d)
    pcd = estimate_normals(pcd)


    print(f"Number of points in the point cloud: {len(pcd.points)}")

    mesh, densities = generate_poisson_mesh(pcd, depth=9)
    threshold = np.percentile(densities, 10)

    clean_mesh = crop_mesh_by_density(mesh, densities, threshold)
    
    pcd_tree = o3d.geometry.KDTreeFlann(pcd)
    mesh_vertex_colors = []

    avg_color = np.mean(merged_colors, axis=0)

    mesh_vertex_colors = np.tile(avg_color, (len(clean_mesh.vertices), 1))

    clean_mesh.vertex_colors = o3d.utility.Vector3dVector(mesh_vertex_colors)


    clean_mesh.vertex_colors = o3d.utility.Vector3dVector(np.array(mesh_vertex_colors))
    o3d.io.write_triangle_mesh(output_path, clean_mesh)
    o3d.visualization.draw_geometries([clean_mesh])

if __name__ == "__main__":

    generate_3d_model(folder, OUTPUT_MESH_PATH)

