import os
import cv2

image_path = "/Users/ulrikisdahl/Desktop/ascend/annotate/annotated/images/"
labels_path = "/Users/ulrikisdahl/Desktop/ascend/annotate/outputs/labels/"
output_path_labels = "/Users/ulrikisdahl/Desktop/ascend/annotate/outputs_cropped/labels/"
output_path_images = "/Users/ulrikisdahl/Desktop/ascend/annotate/outputs_cropped/images/"

filenames = os.listdir("/Users/ulrikisdahl/Desktop/ascend/annotate/outputs/labels")


for filename in filenames:
    filename = filename.split(".")[0]
    
    img = cv2.imread(image_path + filename + ".png")
    height, width, channels = img.shape

    with open(labels_path + filename + ".txt", "r") as read_file:

        lines = read_file.readlines()

        for idx, line in enumerate(lines):

            output_file_path_labels = os.path.join(output_path_labels + filename + f"_{idx}" + ".txt")

            with open(output_file_path_labels, "w") as write_labels:
                write_labels.write(line)

            try:
                center_x = float(line.split(" ")[1]) * width
                center_y = float(line.split(" ")[2]) * height
                bbox_width = float(line.split(" ")[3]) * width
                bbox_height = float(line.split(" ")[4]) * height

                x1 = int(center_x - bbox_width / 2) - 20
                y1 = int(center_y - bbox_height / 2) - 20
                x2 = int(center_x + bbox_width / 2) + 20
                y2 = int(center_y + bbox_height / 2) + 20
            
                cropped_img = img[y1:y2, x1:x2]
                cv2.imwrite(output_path_images + filename + f"_{idx}" + ".png", cropped_img)
            except:
                print("coordinate out of bounds")

            #save image
            



            

    

