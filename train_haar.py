import urllib.request
import cv2
import numpy as np
import os
neg_images_Urls = ''

positive_vehicle_images=  "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n06255081"
negative_images ='http://image-net.org/api/text/imagenet.synset.geturls?wnid=n03792782'

def store_raw_images(link, type):
    neg_images_link = link

    try:
        req = urllib.request.Request(neg_images_link)
        response = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        print(e.reason)


    neg_images_Urls = response.read().decode()
    if not os.path.exists('./' + type):
        os.makedirs('./' + type)
    # print neg_images_Urls
    pic_num = 1

    for i in neg_images_Urls.split('\n'):
        try:
            print(i)
            full_name = "./"+type+"/" + str(pic_num) + ".jpg"
            urllib.request.urlretrieve(i, full_name)
            img = cv2.imread(full_name, cv2.IMREAD_GRAYSCALE)
            print (img.shape[0])
            resized_image = cv2.resize(img, ( 100,100))
            cv2.imwrite(full_name, resized_image)
            pic_num += 1
        except     urllib.error.URLError as e:
            print(" !!!!!!!!!! " + str(e.reason))

        except     :
            print(" !other reasons!!!! " )

def resize(folder, fileName):
    filePath = os.path.join(folder, fileName)
    im = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE)
    resized_image = cv2.resize(im, (100, 100))

    cv2.imwrite(filePath, resized_image)


def bulkResize(imageFolder):
    imgExts = ["png", "bmp", "jpg"]
    for path, dirs, files in os.walk(imageFolder):
        for fileName in files:
            ext = fileName[-3:].lower()
            if ext not in imgExts:
                continue

            resize(path, fileName)

store_raw_images(negative_images, 'neg')

#bulkResize("./cars_test")
#bulkResize("./cars_test")
