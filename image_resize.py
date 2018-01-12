from PIL import Image
import os, re


class Error(Exception):
    pass

class FileFormatError(Error):
    pass

class ThumbnailSelectError(Error):
    pass


def main():
    new_width, new_height = inputSize()
    output_file = inputFileFormat()
    create_thumbnails, thumbnail_resize = inputThumbnail()
    resizeImage(new_width, new_height, output_file, create_thumbnails, thumbnail_resize)


def inputSize():
    while True:
        try:
            ui_width = int(input('Enter new image width in px: '))
            ui_height = int(input('Enter new image height in px: '))
        except ValueError:
            print('Not an integer! Try again!')
            continue
        else:
            return ui_width, ui_height
            break


def inputFileFormat():
    while True:
        try:
            ui_file_format = input('Choose output file format. Enter "j" for .jpeg or "p" for .png: ')
            if ui_file_format.lower() == 'j':
                file_format = 'jpeg'
            elif ui_file_format.lower() == 'p':
                file_format = 'png'
            else:
                raise FileFormatError
        except FileFormatError:
            print('Wrong file format. Try again!')
            continue
        else:
            return file_format
            break


def inputThumbnail():
    while True:
        try:            
            ui_thumb = input('Create thumbnail ? Enter "y" for yes or "n" for no: ')
            if ui_thumb.lower() == 'y':
                create_thumbnails = True
                while True:
                    try:
                        thumbnail_resize = int(input("Enter thumbnails resize in percent: "))
                    except ValueError:
                        print('Not an integer. Try again!')
                        continue
                    else:
                        return create_thumbnails, thumbnail_resize             

            elif ui_thumb.lower() == 'n':
                create_thumbnails = False
                thumbnail_resize = None
                return create_thumbnails, thumbnail_resize
                break
                            
            else:
                raise ThumbnailSelectError
        except ThumbnailSelectError:
            print('Wrong answer. Try again!')
            continue
            


def resizeImage(new_width, new_height, output_file, create_thumbnails, thumbnail_resize):
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
            resizeIm.save(file + '_small', output_file)

            if create_thumbnails:
                width, height = resizeIm.size
                resize_thumbnail = resizeIm.resize((int(width * (thumbnail_resize / 100)), 
                                                    int(height * (thumbnail_resize / 100))))
                resize_thumbnail.save(file + '_thumbnail', output_file)
        


if __name__ == '__main__':
    main()
    