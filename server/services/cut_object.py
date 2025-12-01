import os
from rembg import remove, new_session

session = new_session() 

def remove_background_from_folder(input_folder, output_folder):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        if os.path.isfile(input_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                with open(input_path, 'rb') as f:
                    input_data = f.read()

                output_data = remove(input_data, session=session) 

                with open(output_path, 'wb') as f:
                    f.write(output_data)


remove_background_from_folder(r"C:\Users\OWNER\Desktop\ImageToConvert\check\immm", r"C:\Users\OWNER\Desktop\ImageToConvert\check\without")