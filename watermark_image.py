from PIL import Image, ImageDraw, ImageFont


def watermark_text(input_image_path, output_image_path, text, font_path=None, font_size=40, color=(255, 255, 255, 128),
                   position=(0, 0)):
    """Adds a text watermark to an image using Pillow."""
    base = Image.open(input_image_path).convert('RGBA')

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

    # get a font
    try:
        # Use a specific font file if provided, otherwise default (may need 'arial.ttf' in the directory)
        fnt = ImageFont.truetype(font_path or 'arial.ttf', font_size)
    except IOError:
        print(f"Font not found. Using default font.")
        fnt = ImageFont.load_default()

    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text with transparency (e.g., 128 for semi-transparent white)
    d.text(position, text, font=fnt, fill=color)

    # Combine the base image and the transparent text layer
    watermarked = Image.alpha_composite(base, txt)

    # Convert back to RGB for saving as JPG if needed, then save
    watermarked = watermarked.convert('RGB')

    watermarked.save(output_image_path)
    # print(f"Watermarked image saved to {output_image_path}")
