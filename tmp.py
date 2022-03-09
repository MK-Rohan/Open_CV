import pytesseract, cv2

img_ori_2 = cv2.imread("./fig/book2.jpg")
img_gray_2 = cv2.cvtColor(img_ori_2, cv2.COLOR_BGR2GRAY)
img_gray_2 = cv2.threshold(
    img_gray_2, 130, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
)[1]
# img_gray_2 = cv2.medianBlur(img_gray_2, 10)

img_ori_3 = cv2.imread("./fig/book3.jpg")
img_gray_3 = cv2.cvtColor(img_ori_3, cv2.COLOR_BGR2GRAY)
img_gray_3 = cv2.threshold(
    img_gray_3, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
)[1]
# img_gray_3 = cv2.medianBlur(img_gray_3, 10)

cv2.imshow("img2", img_gray_2)
cv2.imshow("img3", img_gray_3)
cv2.waitKey()
cv2.destroyAllWindows()

pytesseract.pytesseract.tesseract_cmd = (
    r"C:/Program Files/Tesseract-OCR/tesseract"
)

print(pytesseract.image_to_string(img_gray_2, lang="kor"))
print()
print(pytesseract.image_to_string(img_gray_3, lang="kor"))
