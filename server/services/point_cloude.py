import numpy as np
import open3d as o3d

def estimate_normals(pcd):

    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
        radius=0.05, max_nn=30))
    pcd.normalize_normals()
    return pcd

def generate_poisson_mesh(pcd, depth=9):
    print("[INFO] Running Poisson Reconstruction...")

    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=depth)
    return mesh, densities

def crop_mesh_by_density(mesh, densities, threshold_value):

    densities = np.asarray(densities)
    vertices_to_keep = densities > threshold_value
    mesh = mesh.select_by_index(np.where(vertices_to_keep)[0])
    return mesh


def save_and_visualize_mesh(mesh, filename="output_mesh.ply"):

    o3d.io.write_triangle_mesh(filename, mesh)
    print(f"[INFO] Mesh saved to: {filename}")
    o3d.visualization.draw_geometries([mesh])

def get_colors_from_image(image, keypoints):

    colors = []
    h, w, _ = image.shape
    for pt in keypoints:

        x, y = int(round(pt[0])), int(round(pt[1]))
        if 0 <= x < w and 0 <= y < h:
            colors.append(image[y, x] / 255.0)
        else:
            colors.append([0, 0, 0])
    return np.array(colors)

