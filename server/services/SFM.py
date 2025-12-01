import cv2
import numpy as np
import os
import open3d as o3d
import matplotlib.pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS

def detect_and_match_features(img1, img2, sift):

    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.8 * n.distance:
            good_matches.append(m)

    pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches])
    
    return pts1, pts2



def estimate_pose(K, pts1, pts2):
    pts1 = np.ascontiguousarray(pts1, dtype=np.float32)
    pts2 = np.ascontiguousarray(pts2, dtype=np.float32)
    
    E, mask = cv2.findEssentialMat(pts1, pts2, K)
    _, R, t, mask = cv2.recoverPose(E, pts1, pts2, K)
    return R, t


def triangulate_points(K, R, t, pts1, pts2):

    proj1 = K @ np.hstack((np.eye(3), np.zeros((3, 1))))
    proj2 = K @ np.hstack((R, t))

    pts4d = cv2.triangulatePoints(proj1, proj2, pts1.T, pts2.T)

    pts3d = pts4d / pts4d[3]
    return pts3d[:3].T

def save_pointcloud_as_ply(points_3d, filename='output.ply'):

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points_3d)
    o3d.io.write_point_cloud(filename, point_cloud)

def visualize_point_cloud(pcd):
    o3d.visualization.draw_geometries([pcd])

def drawMatches(img1, img2, kp1, kp2, matches):

    matched_img = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    plt.figure(figsize=(12, 6))
    plt.imshow(matched_img)
    plt.title(f"Good Matches Found: {len(matches)}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()



def get_exif_data(image_path):
    img = Image.open(image_path)
    exif_data = {}
    if hasattr(img, '_getexif'):
        exifinfo = img._getexif()
        if exifinfo is not None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value
    return exif_data

def estimate_K_from_exif(image_path, sensor_width_mm=6.17, sensor_height_mm=4.55):

    exif = get_exif_data(image_path)
    focal_length_mm = None
    if 'FocalLength' in exif:
        f = exif['FocalLength']

        if isinstance(f, tuple):
            focal_length_mm = f[0] / f[1]
        else:
            focal_length_mm = float(f)
    else:
        focal_length_mm = 4.0 

    img = Image.open(image_path)
    width, height = img.size

    fx = (width * focal_length_mm) / sensor_width_mm
    fy = (height * focal_length_mm) / sensor_height_mm
    cx = width / 2
    cy = height / 2

    K = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0, 0, 1]
    ])
    return K
