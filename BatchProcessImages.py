from typing import List
from PIL import Image
import os

"""
Module for editing a batch of images. Atributes:
- self.images - a dictionary of opened Image objects(image) and their paths(path)
"""
class ImageBatch(object):
    """ Runs a function fn with every item of self.images. Makes no changes to original dictionary. """
    def map(self, fn):
        for item in self.images:
            fn(item)

    """ Loads all the images specified in path_list """
    def loadImages(self, path_list):
        self.images = self.__loadimages(path_list)

    """ Loads all images found in given folder """
    def loadFolder(self, folder_path):
        # todo: creates path_list -> _loadImages
        return NotImplementedError

    """
    Loads images from given path and returns a dictionary consisting of the images and their paths.
    Raises error if image can not be found.
    """
    def __loadimages(self, path_list):
        image_list = []
        for path in path_list:
            try:
                image = Image.open(path)
                image_list.append({
                    "image": image,
                    "path": path
                    })
            except FileNotFoundError:
                print("File %s not found." % path)
                continue
        return image_list

    """ 
    Saves all opened images.
    save_over - When enabled, saves image over and ignores argument path_fn.
    path_fn - String function that changes save path. If left as None and save_over is False, then the function will use the default save path.
    """
    # todo enable option to save images to new folder
    def save(self, save_over = False, path_fn = None):
        if save_over == True and path_fn != None:
            print("\nWARNING: Are you sure you want to save over? Variable path_fn is set. Nothing has been saved.\n")
            return
        for file in self.images:
            path = file["path"]
            if save_over == False and path_fn == None:
                filepath, extension = os.path.splitext(path)
                path = filepath + " (1)" + extension
            elif save_over == False:
                path = path_fn(path)
            print(path)
            self.__save(file, path)

    def __save(self, file, path):
        file["image"].save(path)

    """ Closes all opened images """
    def close(self):
        self.map(self.__close)

    def __close(self,file):
        file["image"].close()

    """ Shows image from given index"""
    def show(self,index):
        self.images[index]["image"].show()

    def resize(self, size):
        for file in self.images:
            file["image"] = file["image"].resize(size, Image.BILINEAR)
