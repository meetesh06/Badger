from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import argparse
from pathlib import Path
import os
import shutil

def ensure_folder_exists_and_clear(folder_path):
    os.makedirs(folder_path, exist_ok=True)    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove file or symbolic link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove directory and contents
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")


def find_max_font_size(draw, text, font_path, max_font_size, rect):
    # Try decreasing font size until text fits within the rectangle
    for font_size in range(max_font_size, 0, -1):
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        if text_width <= (rect[2] - rect[0]) and text_height <= (rect[3] - rect[1]):
            return font_size  # Found the maximum font size that fits
    return 0

def plotBox(draw, rect, font_path, font_size, text_to_print):
    font = ImageFont.truetype(font_path, font_size)
    bbox = draw.textbbox((0, 0), text_to_print, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (rect[0] + rect[2] - text_width) // 2
    text_y = (rect[1] + rect[3] - text_height) // 2
    text_position = (text_x, text_y)
    draw.text(text_position, text_to_print, font=font, fill="black")

def plotForEntry(img, name1, aff1, rect, rect_affiliation, font_path):
    draw = ImageDraw.Draw(img)
    max_font_size = 70
    font_size = find_max_font_size(draw, name1, font_path, max_font_size, rect)
    vertical_spacing = 15
    if font_size < 60:
        words = name1.split(" ")
        total_text_height = sum(
            ImageFont.truetype(font_path, font_size).getbbox(word)[3] for word in words
        )
        current_y = (rect[1] + rect[3] - total_text_height - (len(words) - 1) * vertical_spacing) // 2
        for word in words:
            font_size = 70
            font = ImageFont.truetype(font_path, font_size)
            bbox = draw.textbbox((0, 0), word, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_position = ((rect[0] + rect[2] - text_width) // 2, current_y)
            draw.text(text_position, word, font=font, fill="black")
            current_y += text_height + vertical_spacing
    else:
        plotBox(draw, rect, font_path, font_size, name1)

    plotBox(draw, rect_affiliation, font_path, 50, aff1)

def main():
    parser = argparse.ArgumentParser(description="PLλTO Badger, IITB")
    parser.add_argument("csv", type=str, help="path to CSV containing columns 'Name' and 'Affiliation'; all other columns will be ignored")
    parser.add_argument("template", type=str, help="path to template file to use, see PLACID2024.png for reference (we expect to print 6 ID's in an A4 Sheet)")
    parser.add_argument("font", type=str, help="path to the font file to use, Kollektif-Bold.ttf is a good choice...")
    parser.add_argument("--out", type=str, help="Path to the output folder (default='./outputs')", required=False, default="./outputs")
    parser.add_argument("--h-scale", type=float, help="Horizontal Scaling (default = 67.34006734)", required=False, default=67.34006734)
    parser.add_argument("--v-scale", type=float, help="Horizontal Scaling (default = 67.333333333)", required=False, default=67.333333333)
    args = parser.parse_args()
    csv_path = Path(args.csv)
    template_path = Path(args.template)
    font_path = Path(args.font)
    horizontal_scaling = args.h_scale
    vertical_scaling = args.v_scale
    outputs_path = args.out
    ensure_folder_exists_and_clear(outputs_path)
    df = pd.read_csv(csv_path)
    namesss = df['Name']
    addiliationnn = df['Affiliation']

    for x in range(0, len(namesss), 6):
        img = Image.open(template_path)
        name1 = namesss[x]
        aff1 = addiliationnn[x]
        rect = [1*horizontal_scaling, 4*vertical_scaling, 8.6*horizontal_scaling, 7.0*vertical_scaling]
        rect_affiliation = [1*horizontal_scaling, 6*vertical_scaling, 8.6*horizontal_scaling, 8.2*vertical_scaling]
        plotForEntry(img, name1, aff1, rect, rect_affiliation, font_path)

        name1 = namesss[x + 1]
        aff1 = addiliationnn[x + 1]
        rect = [1*horizontal_scaling, 14.5*vertical_scaling, 8.6*horizontal_scaling, 17.5*vertical_scaling]
        rect_affiliation = [1*horizontal_scaling, 16.5*vertical_scaling, 8.6*horizontal_scaling, 18.7*vertical_scaling]
        plotForEntry(img, name1, aff1, rect, rect_affiliation, font_path)

        name1 = namesss[x + 2]
        aff1 = addiliationnn[x + 2]
        rect = [11*horizontal_scaling, 4*vertical_scaling, 18.6*horizontal_scaling, 7*vertical_scaling]
        rect_affiliation = [11*horizontal_scaling, 6*vertical_scaling, 18.6*horizontal_scaling, 8.2*vertical_scaling]
        plotForEntry(img, name1, aff1, rect, rect_affiliation, font_path)

        name1 = namesss[x + 3]
        aff1 = addiliationnn[x + 3]
        rect = [11*horizontal_scaling, 14.5*vertical_scaling, 18.6*horizontal_scaling, 17.5*vertical_scaling]
        rect_affiliation = [11*horizontal_scaling, 16.5*vertical_scaling, 18.6*horizontal_scaling, 18.7*vertical_scaling]
        plotForEntry(img, name1, aff1, rect, rect_affiliation, font_path)

        name1 = namesss[x + 4]
        aff1 = addiliationnn[x + 4]
        rect = [21.1*horizontal_scaling, 4*vertical_scaling, 28.6*horizontal_scaling, 7*vertical_scaling]
        rect_affiliation = [21.1*horizontal_scaling, 6*vertical_scaling, 28.6*horizontal_scaling, 8.2*vertical_scaling]
        plotForEntry(img, name1, aff1, rect, rect_affiliation, font_path)

        name1 = namesss[x + 5]
        aff1 = addiliationnn[x + 5]
        rect = [21.1*horizontal_scaling, 14.5*vertical_scaling, 28.6*horizontal_scaling, 17.5*vertical_scaling]
        rect_affiliation = [21.1*horizontal_scaling, 16.5*vertical_scaling, 28.6*horizontal_scaling, 18.7*vertical_scaling]
        plotForEntry(img, name1, aff1, rect, rect_affiliation, font_path)

        img.save(f"{outputs_path}/generated-{x}-{x+3}.png")

if __name__ == "__main__":
    main()
