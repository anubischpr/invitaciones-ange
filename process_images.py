from PIL import Image
import os

def make_transparent(img, threshold=235):
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        # If all RGB values are above threshold, make transparent
        if item[0] >= threshold and item[1] >= threshold and item[2] >= threshold:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    return img

def process_single(input_path, output_path):
    img = Image.open(input_path)
    trans = make_transparent(img)
    trans.save(output_path)
    print(f"Processed {input_path} -> {output_path}")

def split_and_process(input_path):
    img = Image.open(input_path)
    w, h = img.size
    # Quadrants:
    # Top-Left: Balloons, Top-Right: Clouds
    # Bottom-Left: Sello, Bottom-Right: Cesped
    boxes = [
        (0, 0, w//2, h//2),
        (w//2, 0, w, h//2),
        (0, h//2, w//2, h),
        (w//2, h//2, w, h)
    ]
    names = [
        "assets/balloons.png",
        "assets/clouds.png",
        "assets/sello.png",
        "assets/cesped.png"
    ]
    for box, name in zip(boxes, names):
        cropped = img.crop(box)
        trans = make_transparent(cropped)
        trans.save(name)
        print(f"Processed quadrant from {input_path} -> {name}")

if __name__ == "__main__":
    process_single("assets/naruto.jpg", "assets/naruto.png")
    process_single("assets/kurama.jpg", "assets/kurama.png")
    split_and_process("assets/balloons-clouds-sello-cesped.jpg")
