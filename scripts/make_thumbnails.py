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

    def resize_imgs(self, images):
        for img_file in images:
            input_path = self.in_dir + img_file
            if not os.path.isfile(input_path):
                continue
            img = Image.open(input_path)
            img.thumbnail([300,300])
            out_path = self.out_dir + img_file
            if not os.path.isfile(out_path):
                print(f'Saving {self.out_dir + img_file}')
                img.save(out_path)
        return

if __name__=="__main__":
    args = proc_opts()
    resizer = ImgResizer(args.folder, args.outfolder)
    imgs = resizer.get_all_images()
    resizer.resize_imgs(imgs)
