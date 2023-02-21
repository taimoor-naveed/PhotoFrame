import os
import threading
import random
import queue
import time
import requests
import json
from PIL import Image
from pillow_heif import register_heif_opener
from watchdog.observers import Observer
from FileEventHandler import FileEventHandler

import os
import subprocess

def getRotationData(fileName):
    try:
        exifdata = subprocess.check_output(['exiftool', fileName], shell=False, text=True)
        exifdata = exifdata.splitlines()
        exif = dict()
        for i, each in enumerate(exifdata):
            tag,val = each.split(': ', 1)
            exif[tag.strip()] = val.strip()
        
        if "Orientation" not in exif:
            print("no orientation data found")
            return 0
        
        if exif["Orientation"] == "Rotate 90 CW":
            return 90.0
        elif exif["Orientation"] == "Rotate 180":
            return 180.0
        elif exif["Orientation"] == "Rotate 270 CW":
            return 270.0
        else:
            return 0
    except:
        return 0

def cropImage(image, rect):
    return image.crop(rect)


def resizeImage(image, width, height):

    imageWidgth, imageHeight = image.size

    if (imageWidgth / width) < imageHeight / height:
        wpercent = (width / float(image.size[0]))
        hsize = round((float(image.size[1]) * float(wpercent)))
        return image.resize((width, hsize), Image.ANTIALIAS)
    else:
        wpercent = (height / float(image.size[1]))
        wsize = round((float(image.size[0]) * float(wpercent)))
        return image.resize((wsize, height), Image.ANTIALIAS)


def findOptimalRect(fileName):
    url = 'https://croppola.com/croppola/image.json?aspectRatio=1024:600&minimumHeight=600%&algorithm=croppola'
    try:
        data = open(fileName, 'rb')
        res = requests.post(url, data=data, headers={'User-Agent': 'py'})
        data.close()
        if res.status_code == 200:
            jsonFile = json.loads(res.content.decode('utf-8'))
            return (jsonFile['cropX'], jsonFile['cropY'], jsonFile['cropX'] + jsonFile['cropWidth'], jsonFile['cropY'] + jsonFile['cropHeight'])
        else:
            print('Error return code')
            print(res.status_code)
            return None
    except IOError:
        print('Error fetching rect from image')
        return None


def processOnCreated(src_path, internalDirectory, fileList):
    if os.path.exists(src_path):
        image = Image.open(src_path)
        
        rect = None
        if 'nocrop' not in src_path:
            rect = findOptimalRect(src_path)
        if rect:
            image = cropImage(image, rect)

        image = resizeImage(image, 1024, 600)
        
        angle = getRotationData(src_path)
        image = image.rotate(-angle)

        image.save(os.path.join(internalDirectory, os.path.basename(src_path)))
        fileList.insert(random.randrange(len(fileList) + 1), os.path.basename(src_path))
        
def processOnDeleted(src_path, internalDirectory, fileList):
    if os.path.exists(os.path.join(internalDirectory, os.path.basename(src_path))):
        os.remove(os.path.join(internalDirectory, os.path.basename(src_path)))
    if os.path.basename(src_path) in fileList:
        fileList.remove(os.path.basename(src_path))

def processOnMoved(src_path, dest_path, internalDirectory, fileList):
    if os.path.exists(os.path.join(internalDirectory, os.path.basename(src_path))):
        os.remove(os.path.join(internalDirectory, os.path.basename(src_path)))
    if os.path.basename(src_path) in fileList:
        fileList.remove(os.path.basename(src_path))
    processOnCreated(dest_path, internalDirectory, fileList)

class FileManager:
    def __init__(self, path):
        self.externalDirectory = path

        self.internalDirectory = os.path.join(os.path.dirname(path), 'internalDirectory')

        if not os.path.exists(self.internalDirectory):
            os.mkdir(self.internalDirectory)

        self.fileList = os.listdir(self.internalDirectory)
        random.shuffle(self.fileList)

        self.fileEventQueue = queue.Queue()

        self.runFlag = 1
        self.backgroundThread = threading.Thread(target=self.process)
        self.backgroundThread.start()

        self.fileEventHandler = FileEventHandler(self.fileEventQueue)

        self.observer = Observer()
        self.observer.schedule(self.fileEventHandler, self.externalDirectory)
        self.observer.start()

        self.currentFileIndex = 0

    def process(self):
        register_heif_opener()
        while self.runFlag:
            try:
                fileEvent = self.fileEventQueue.get(timeout=1)

                time.sleep(1)

                if fileEvent.event_type == 'created':
                    processOnCreated(fileEvent.src_path, self.internalDirectory, self.fileList)
                    # print(fileEvent.src_path + ' added')
                elif fileEvent.event_type == 'moved':
                    # print(fileEvent.src_path + ' renamed to ' + fileEvent.dest_path)
                    processOnMoved(fileEvent.src_path, fileEvent.dest_path, self.internalDirectory, self.fileList)
                elif fileEvent.event_type == 'deleted':
                    processOnDeleted(fileEvent.src_path, self.internalDirectory, self.fileList)
                    # print(fileEvent.src_path + ' removed')
            except Exception as e:
                print("exception", repr(e))

    def stop(self):
        self.runFlag = 0
        self.backgroundThread.join()
        self.observer.stop()
        self.observer.join()

    def incrementCurrentFileIndex(self):
        self.currentFileIndex = self.currentFileIndex + 1

        if self.currentFileIndex >= len(self.fileList):
            self.currentFileIndex = 0

    def decrementCurrentFileIndex(self):
        self.currentFileIndex = self.currentFileIndex - 1

        if self.currentFileIndex < 0:
            self.currentFileIndex = len(self.fileList) - 1

    def getFirstFile(self):
        if len(self.fileList):
            return os.path.join(self.internalDirectory, self.fileList[0])
        else:
            return None

    def getNextFile(self):
        if len(self.fileList):
            self.incrementCurrentFileIndex()
            return os.path.join(self.internalDirectory, self.fileList[self.currentFileIndex])
        else:
            return None

    def getPreviousFile(self):
        if len(self.fileList):
            self.decrementCurrentFileIndex()
            return os.path.join(self.internalDirectory, self.fileList[self.currentFileIndex])
        else:
            return None

