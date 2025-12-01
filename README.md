📦 3D Reconstruction System (SfM + Web App)

A full-stack project that converts 2D images into a 3D model using Python, OpenCV, Structure-from-Motion (SfM), Open3D, Poisson mesh reconstruction, and a React-based user interface.
The system allows a user to upload multiple images, process them on the server, and automatically download a .ply 3D model.

🚀 Project Overview

This project provides an end-to-end solution for generating 3D models from images:

Backend (Python + Flask)

Feature detection & matching (SIFT)

Camera pose estimation (Essential Matrix, RecoverPose)

Triangulation of 3D points

Point cloud creation

Poisson mesh reconstruction

Mesh cleaning & coloring

User login/register system (SQLite database)

API for uploading images and downloading the generated model

Frontend (React)

Upload multiple images

Preview selected images

Send images to the server

Automatic model download

3D viewer using Three.js + PLYLoader

Login & Sign-In pages

Styled UI in CSS

🧠 Technologies Used
Backend

Python

OpenCV

Open3D

NumPy

Flask

SQLite

rembg (optional background removal)

Frontend

React

JavaScript

Three.js

CSS

🗂 Project Structure
Backend (Python)
File	Description
main.py	Core engine: SfM pipeline, mesh reconstruction, coloring
SFM.py	Feature detection, matching, pose estimation, triangulation 

SFM


point_cloude.py	Mesh generation, Poisson reconstruction, normals, colors 

point_cloude


cut_object.py	Background removal for image preprocessing 

cut_object


server.py	Flask server, API routes, users DB, upload logic 

server

Frontend (React)
File	Description
buttons.js	Main UI: image upload, preview, send-to-server, download model 

buttons


model3D.js	Three.js viewer for 3D .ply models 

model3D


login.js	Login form and API request to backend 

login


signIn.js	Register form and API request 

signIn


history.js	UI placeholder for user action history 

history


picToServer.js	Old/alternative upload component 

picToServer


style.css	Styling for forms 

style


compnents.css	Global component styling 

compnents

🎯 Features
🔹 Image Upload

Users upload multiple images through a React interface.
Images are previewed before sending to the server.

🔹 Server Processing (SfM Pipeline)

Detect & match features

Estimate camera pose

Triangulate 3D points

Merge point clouds

Estimate normals

Poisson mesh reconstruction

Clean low-density areas

Apply vertex coloring

Export .ply model

🔹 Download 3D Model

The server returns the resulting mesh directly as a downloadable file.

🔹 User System

Register

Login

SQLite database for users

🔹 3D Viewer (Optional)

Load and rotate the PLY model using Three.js.

▶️ How It Works (Flow)
Frontend

User selects images

React component builds FormData

Sends images → POST /upload

Downloads model.ply automatically

Optional: displays model in 3D viewer

Backend

Saves uploaded images

Runs full 3D reconstruction pipeline

Outputs cleaned mesh

Sends mesh to user

🛠 How to Run
Backend
pip install -r requirements.txt
python server.py

Frontend
npm install
npm start

📁 Future Improvements

Full WebGL viewer page

Texture mapping

Multi-view display of uploaded images

User history for downloaded models
