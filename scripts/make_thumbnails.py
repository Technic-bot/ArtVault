import argparse
import os

from PIL import Image

def proc_opts():
    parser = argparse.ArgumentParser(
            description="Make thumbnails from all images in a dir"
            )
    parser.add_argument('folder')
    parser.add_argument('outfolder')
    return parser.parse_args()


class ImgResizer():
    def __init__(self, in_dir:str , out_dir:str):
        self.in_dir = in_dir
        self.out_dir = out_dir

    def get_all_images(self):
        images = []
        for file in os.listdir(self.in_dir):
            images.append(file)

        print(f"Got {len(images)} files")
        return images

    def get_cache(self):
        self.cache= set()
        for file in os.listdir(self.out_dir):
            self.cache.add(file)

        print(f"Got {len(self.cache)} thumbnails")
        return

    def resize_imgs(self, images):
        proccessed_imgs = 0
        for img_file in images:
            if img_file in self.cache:
                continue

            input_path = self.in_dir + img_file
            if not os.path.isfile(input_path):
                print(f'{input_path} not and image')
                continue
            img = Image.open(input_path)
            img.thumbnail([300,300])
            out_path = self.out_dir + img_file
            try:
                proccessed_imgs += 1
                print(f'Saving {self.out_dir + img_file}')
                img.save(out_path)
            except ValueError as e:
                print(e)
                print(f'Error saving {out_path}')
            except PIL.UnidentifiedImageError as e:
                print(e)
                print(f'Error saving {out_path}')
        return

if __name__=="__main__":
    args = proc_opts()
    resizer = ImgResizer(args.folder, args.outfolder)
    imgs = resizer.get_all_images()
    resizer.get_cache()
    resizer.resize_imgs(imgs)
