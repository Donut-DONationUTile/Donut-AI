import cv2
import numpy as np

# 답지 이미지 
giftcon= cv2.imread('/asset/train/image3.jpeg')

#탬플릿
barcode = cv2.imread('/templete/barcode.png')

# 탬플릿 매칭 해내기 
res = cv2.matchTemplate(giftcon, barcode, cv2.TM_CCOEFF_NORMED)

# 임계치 정하기 
threshold = .65

#임계치 이상만 배열에 저장
loc = np.where(res >= threshold)

#템플릿의 가로(w),세로(h)길이 저장
h, w = barcode.shape[:-1]


for pt in zip(*loc[::-1]):  # Switch collumns and rows
    cv2.rectangle(giftcon, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    #빨간색 굵기2의 박스를 그림 

cv2.imshow(giftcon)