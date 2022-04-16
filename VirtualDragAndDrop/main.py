import cv2 
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)


class DragImg():
    def __init__(self, path, posOrigin, imgType):

        self.posOrigin = posOrigin
        self.imgType = imgType
        self.path = path

        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        self.size = self.img.shape[:2]

    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size
        # check if in region

        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2



# img1 = cv2.imread("ImagesJPG/1.jpg")
# img1 = cv2.imread("ImagesPNG/1.png", cv2.IMREAD_UNCHANGED)
# ox, oy = 200, 200


path = "ImagesPNG"
myList = os.listdir(path)
print(myList)

listImg = []
for x, pathImg in enumerate(myList):
    if 'png' in pathImg:
        imgType = 'png'
    else:
        imgType = 'jpg'
    listImg.append( DragImg(f'{path}/{pathImg}',[50+x*300, 50], imgType))
    

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        # check if clicked

        # cursor = lmList[8]
        length, info, img = detector.findDistance(lmList[8], lmList[12], img)
        # print(length)
        if length < 60:
            cursor = lmList[8]
            for imgObject in listImg:
                imgObject.update(cursor)

    try:

        for imgObject in listImg:

            # Drow for JPG Image
            h, w = img1.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                # Drow for PNG Image
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            else:
                img[oy:oy+h, ox:ox+w] = imgObject.img  


    except:
        pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)

