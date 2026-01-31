import os
from werkzeug.utils import secure_filename
from PIL import Image
from watermark_image import watermark_text


def allowed_file(filename, allowed_extensions):
    return (
            '.' in filename and
            filename.rsplit('.', 1)[1].lower() in allowed_extensions
    )


def save_image(
        file,
        upload_folder,
        allowed_extensions,
        resize_to=(300, 300),
        thumb_size=(100, 100)
):
    if not file or file.filename == '':
        return 'no file'

    if not allowed_file(file.filename, allowed_extensions):
        return 'invalid file'

    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)

    original_path = os.path.join(upload_folder, filename)
    resized_path = os.path.join(upload_folder, f"resized_{name}{ext}")
    thumb_path = os.path.join(upload_folder, f"thumb_{name}{ext}")

    file.save(original_path)

    watermark_text(original_path, original_path, "Sok Piseth",font_size=20, position=(20,20))

    image = Image.open(original_path)

    resized = image.copy()
    resized.thumbnail(resize_to)
    resized.save(resized_path)

    thumb = image.copy()
    thumb.thumbnail(thumb_size)
    thumb.save(thumb_path)

    return {
        "original": filename,
        "resized": f"resized_{name}{ext}",
        "thumbnail": f"thumb_{name}{ext}"
    }
