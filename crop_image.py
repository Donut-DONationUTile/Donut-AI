import cv2
import numpy as np

# 답지 이미지 
giftcon= cv2.imread('./asset/train/image7.jpeg')

#탬플릿
barcode = cv2.imread('./templete/only_barcode.png')
print("Original Barcode size: ", barcode.shape[1], barcode.shape[0])
# 크기 변경
# giftcon과 barcode의 가로 길이를 가져옵니다.
giftcon_width = giftcon.shape[1]
barcode_width = barcode.shape[1]
barcode_height = barcode.shape[0]

# giftcon의 가로 길이의 3/5를 바코드의 새로운 가로 길이로 설정합니다.
new_width = int(giftcon_width * 2/ 3)

# 바코드의 가로, 세로 비율을 계산하고 이를 바탕으로 새로운 세로 길이를 계산합니다.
ratio = barcode_height / barcode_width
new_height = int(new_width * ratio)

# 바코드의 크기를 조정합니다.
barcode = cv2.resize(barcode, (new_width, new_height))

# 크기 변경 확인
print("Giftcon size: ", giftcon_width)
print("Resized Barcode size: ", barcode.shape[1], barcode.shape[0])


res = cv2.matchTemplate(giftcon, barcode, cv2.TM_SQDIFF_NORMED)
threshold = .999
loc = np.where(res >= threshold)

h, w = barcode.shape[:-1]
for pt in zip(*loc[::-1]):  # Switch collumns and rows
    cv2.rectangle(giftcon, pt, (pt[0] + w + 40, pt[1] + h +60), (0, 0, 255), 2)
    #빨간색 굵기2의 박스를 그림 

cv2.imshow('Giftcon Image', giftcon)
cv2.waitKey(0)
cv2.destroyAllWindows()