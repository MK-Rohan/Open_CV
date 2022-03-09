##### Modules #####
import pytesseract, cv2, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

##### Image Load #####
image_original = cv2.imread("./fig/book2.jpg")
image_gray = cv2.cvtColor(image_original, cv2.COLOR_BGR2GRAY)

##### Image Color Value Distribution #####
# plt.hist(image_gray.ravel(), 256, [0, 256])
# plt.show()

_, thresh = cv2.threshold(image_gray, 0, 250, cv2.THRESH_BINARY)

##### Kernel Size #####
kernel = np.ones((5, 5), np.uint8)

##### Dilation #####
dilation = cv2.dilate(thresh, kernel, iterations=2)

##### Morph Close #####
closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)

contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, 3)
img_contour = cv2.drawContours(image_original, contours, -1, (0, 255, 0), 3)

contour_pos = list()

##### 잡음 제거 #####
for pos in range(len(contours)):
    area = cv2.contourArea(contours[pos])
    if area > 100:
        contour_pos.append(pos)

###
for p in contour_pos:
    img_temp = image_original.copy()
    img_orig = image_original.copy()
    x, y, w, h = cv2.boundingRect(contours[p])

    cnt = contours[p]
    area = cv2.contourArea(cnt)

    area_box = w * h

    img_contour = cv2.drawContours(img_orig, contours, p, (0, 255, 0), 1)

    cnt = contours[p]
    M = cv2.moments(cnt)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    for i in range(y, y + h):
        px_lst = img_contour[i]

        for j in range(x, x + w):
            if (px_lst[j] == [0, 255, 0]).all():
                cv2.line(img_contour, (j, i), (cx, cy), (1, 2, 3), 2)

    img_crop = img_contour[y : y + h, x : x + w]

    for i in range(y, y + h):
        px_lst = img_contour[i]

        for j in range(x, x + w):
            if (px_lst[j] != [1, 2, 3]).all():
                cv2.line(img_temp, (j, i), (j, i), (0, 0, 0), 2)

    img_save = img_temp[y : y + h, x : x + w]
    # cv2.imshow("image", img_save)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

pytesseract.pytesseract.tesseract_cmd = (
    r"C:/Program Files/Tesseract-OCR/tesseract"
)

####

CLIENT_ID = "hMsbLHYw68EctNQC_Bml"
CLIENT_SECRET = "zbMb6cu4PE"


def search_book(query):
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode, quote
    import json

    request = Request(
        "https://openapi.naver.com/v1/search/book?query=" + quote(query)
    )
    request.add_header("X-Naver-Client-id", CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)

    response = urlopen(request).read().decode("utf-8")
    search_result = json.loads(response)
    return search_result

    # if __name__ == "__main__":
    # books = search_book("종의 기원")["items"]
    # for book in books:
    #     print("title: {}".format(book["title"]))
    #     print("author: {}".format(book["author"]))
    #     print("pubdate: {}".format(book["pubdate"]))
    #     print("image: {}".format(book["image"]))
    #     print("description: {}".format(book["description"]))
    #     print("-------")


#####
idx = 0
#### 해당 영역 오려내기 #####
for pos in contour_pos:
    x, y, w, h = cv2.boundingRect(contours[pos])
    img_crop = img_temp[y : y + h, x : x + w]
    # cv2.imshow("image2", img_crop)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    line = pytesseract.image_to_string(img_crop, lang="kor")
    if 2 <= len(line):
        for ln in line.rstrip().split("\n"):
            try:
                books = search_book(ln)["items"]
            except:
                continue
            for book in books:
                print("----Start----")
                # print("Type of book:", type(book))
                # print("Type of books:", type(books))
                print("title: {}".format(book["title"]))
                print("author: {}".format(book["author"]))
                print("pubdate: {}".format(book["pubdate"]))
                print("image: {}".format(book["image"]))
                # print("description: {}".format(book["description"]))
                print("----End----")
                idx += 1
                if idx == 3:
                    idx = 0
                    break

