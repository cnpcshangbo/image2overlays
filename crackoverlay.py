import cv2
import os
import configparser

# Load the INI file and parse it
config = configparser.ConfigParser()
config.read("config.ini")  # Replace with the actual path to your INI file

# Paths for the mask images, raw images, and output images
# Read from the INI file
mask_dir = config["CrackSegmentation"]["mask_directory"].replace("crackmask", "filteredCrackMasks")
raw_dir = config["Settings"]["image_path"]
output_dir = config["CrackOverlay"]["overlay_directory"].replace("crackoverlay", "filteredCrackOverlays")

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over the files in the mask directory
for mask_name in os.listdir(mask_dir):
    # Extract the image name from the filename
    raw_name = mask_name.split(".")[0] + ".jpg"

    # Load the mask and raw images
    mask = cv2.imread(os.path.join(mask_dir, mask_name), cv2.IMREAD_GRAYSCALE)
    raw = cv2.imread(os.path.join(raw_dir, raw_name))

    if mask is None or raw is None:
        print(f"Error reading {mask_name} or {raw_name}. Skipping...")
        continue

    print(raw.shape)
    print(mask.shape)

    # Where the mask is white, set the raw image to red
    raw[mask == 38] = [0, 255, 0]

    # Save the overlaid image to the output directory
    output_name = os.path.join(output_dir, raw_name)
    cv2.imwrite(output_name, raw)
    print(f"Saved {output_name}")

print("Processing complete!")
