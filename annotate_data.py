import matplotlib.pyplot as plt
import cv2
import os
import PIL
import matplotlib.patches as patches



path = "annotated"
label_path = path + "/labels"
image_path = path + "/images"

output_path = "/Users/ulrikisdahl/Desktop/ascend/annotate/outputs"

filenames = os.listdir(path + "/images")
filenames = [filename.split(".")[0] for filename in filenames]

#print(filesnames)

valid_shapes = ["circle", "semicircle", "quarter circle", "triangle", "rectangle", "pentagon", "star", "cross"]
valid_colors = ["white", "black", "red", "blue", "green", "purple", "brown", "orange"]
valid_symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

valid_shape_entries = ["cir", "sem", "qua", "tri", "rec", "pen", "star", "cross"]
valid_color_entries = ["w", "blk", "r", "b", "g", "p", "br", "o"]

def validate_input2(inp):
    inp_split = inp.split(" ")
    if not inp_split[0] in valid_shapes:
        print("WRONG shape")
        return False
    if not inp_split[1] in valid_colors:
        print("WRONG shape color")
        return False
    if not inp_split[2] in valid_symbols:
        print("WRONG alphanumeric")
        return False
    if not inp_split[-1] in valid_colors:
        print("WRONG alphanumeric color")
        return False
    return True


def validate_input(input):
    inp_split = input.split(" ")
    if not inp_split[0] in valid_shape_entries:
        print("WRONG shape")
        return False
    if not inp_split[1] in valid_color_entries:
        print("WRONG shape color")
        return False
    if not inp_split[2].upper() in valid_symbols:
        print("WRONG alphanumeric")
        return False
    if not inp_split[3] in valid_color_entries:
        print("WRONG alphanumeric color")
        return False
    print("Success, features added:", end=" ")
    return True

def remove_spaces(input):
    parts = input.split(" ")
    parts = list(filter(lambda x: x.strip() != "", parts))
    new_string = " ".join(parts)

    return new_string


def generate_string(input):
    inp_split = input.split(" ")
    shape_index = valid_shape_entries.index(inp_split[0])
    shape_color_index = valid_color_entries.index(inp_split[1])
    an_color_index = valid_color_entries.index(inp_split[3])

    return valid_shapes[shape_index] + " " + valid_colors[shape_color_index] + " " + inp_split[2].upper() + " " + valid_colors[an_color_index]


def print_help_plz():
    print()
    print("New BBOX for " + filename + ".")
    print("Shapes: ", end=" ")

    shape_string = ""
    for i in range(len(valid_shapes)):
        shape_string += valid_shape_entries[i] + " = " + valid_shapes[i] + "; "
    print(shape_string)
    print()

    print("Colors: ", end=" ")

    color_string = ""
    for j in range(len(valid_colors)):
        color_string += valid_color_entries[j] + " = " + valid_colors[j] + "; "
    print(color_string)
    print()


def zoom_to_bbox(ax, bbox_x, bbox_y, bbox_width, bbox_height, padding=0.1):
    # Calculate the limits for the zoomed-in region
    xlim_min = bbox_x - padding * bbox_width - 40
    xlim_max = bbox_x + (1 + padding) * bbox_width + 40
    ylim_min = bbox_y - padding * bbox_height - 40
    ylim_max = bbox_y + (1 + padding) * bbox_height + 40
    
    # Set the limits for the x and y axes
    ax.set_xlim(xlim_min, xlim_max)
    ax.set_ylim(ylim_min, ylim_max)

rectangle_patch = None
rect = None

for filename in filenames:
    txt_file_path = label_path + "/" + filename + ".txt"

    output_file_path_labels = os.path.join(output_path + "/labels", filename + ".txt")

    with open(txt_file_path, "r") as read_bbox, open(output_file_path_labels, "w") as write_labels:
        lines = read_bbox.readlines()
        print(lines)
        
        img = cv2.imread(image_path + "/" + filename + ".png")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channels = img.shape

        fig, ax = plt.subplots(figsize=(9, 9))
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax.set_title(filename)

        plt.ion()


        for bbox_line in lines:
            valid_input = False


            if rect:
                rect.remove()

            bbox = [x.replace("\n", "") for x in bbox_line.split(" ")]
            bbox_width = float(bbox[3]) * width
            bbox_height = float(bbox[4]) * height
            bbox_x = float(bbox[1]) * width - bbox_width // 2
            bbox_y = float(bbox[2]) * height - bbox_height // 2
            
            #rectangle_patch = plt.gca().add_patch(plt.Rectangle((bbox_x, bbox_y), bbox_width, bbox_height, facecolor="none", edgecolor="r", linewidth=1,  fill="False"))


            rect = patches.Rectangle((bbox_x, bbox_y), bbox_width, bbox_height, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

            zoom_to_bbox(ax, bbox_x, bbox_y, bbox_width, bbox_height)

            #plt.imshow(img_rgb)

            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            plt.axis('off')
            plt.draw()
            plt.pause(0.001)
            print_help_plz()
            
            while not valid_input:
                object = input("Enter shape shape_color an an_color: ") # figure, figure-color, alphanumeric, alphanumeric-color
                feat_string = remove_spaces(object)
                valid_input = validate_input(feat_string)
                

            
            features = generate_string(feat_string)
            print(features)
            bbox.append(features)
            bbox_labeled_line = " ".join(bbox)
            write_labels.write(bbox_labeled_line + "\n")
    plt.close()
    
    
    #break
