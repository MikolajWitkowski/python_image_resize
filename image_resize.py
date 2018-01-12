from PIL import Image
import os, re

new_width = int(input("Enter new image width in px: "))
new_height = int(input("Enter new image height in px: "))

thumbnail_resize = int(input("Thumbnail resize in percent: "))

for photo in os.listdir('.'):
    if re.match('.*\jpeg|.*\.png', photo):
        file, ext = os.path.splitext(photo)
        image = Image.open(photo)

        width, height = image.size

        if width < height:
            img_x = min(new_width, new_height)
            img_y = max(new_width, new_height)

        elif width > height:
            img_x = max(new_width, new_height)
            img_y = min(new_width, new_height)

        crop_width = width % img_x
        crop_height = height % img_y

        crop_width_ratio = (width - crop_width) / img_x
        crop_height_ratio = (height - crop_height) / img_y
        
        if crop_width_ratio < crop_height_ratio:
            crop_height = height - (crop_width_ratio * img_y)
        else:
            crop_width = width -  (crop_height_ratio * img_x)
       
        croppedIm = image.crop((int(width / 2 - (width - crop_width) / 2),
                                int(height / 2 - (height - crop_height) / 2),
                                int(width / 2 + (width - crop_width) / 2),
                                int(height / 2 + (height - crop_height) / 2)))

        width_cropped, height_cropped = croppedIm.size
        
        resizeIm = croppedIm.resize((int(width_cropped / int((width_cropped / img_x))), 
                                int(height_cropped / int((height_cropped / img_y)))))       
        resizeIm.save(file + '_small', 'jpeg')

        width, height = resizeIm.size
        resize_thumbnail = resizeIm.resize((int(width * (thumbnail_resize / 100)), int(height * (thumbnail_resize / 100))))
        resize_thumbnail.save(file + '_thumbnail', 'jpeg')
        



