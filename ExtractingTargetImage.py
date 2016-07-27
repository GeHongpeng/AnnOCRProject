# _*_ coding= utf-8 _*_

import numpy as np
import cv2
import ContoursProcessingLibrary as cpl


# カラー画像を読み込む
img = cv2.imread('./testdata/sample/sample6.jpg', cv2.IMREAD_COLOR)

# 輪郭を算出する
contours = cpl.find_contours(img)

# 文字の長方形を算出する
rectangles = cpl.exclude_inadequacy_contours(img, contours)

"""
各文字の画像を取得する
"""
for r in rectangles:
    # 座標を取得する
    x, y, w, h = r
    # 取得した長方形を描画する
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)

    """
    # パディングに加えた正方形の座標情報を取得する
    wd_x, wd_y, wd_w, wd_h = wrap_character(r)
    if wd_x < 0:
        wd_x = 0
    if wd_y < 0:
        wd_y = 0
    # # 取得した正方形を描画する
    cv2.rectangle(img, (wd_x, wd_y), (wd_x+wd_w, wd_y+wd_h), (0, 255, 0), 1)
    """

    #roi = thbw[wd_y:wd_y+wd_h, wd_x:wd_x+wd_w]
    #title = 'test' + str(counter)
    #cv2.imshow(title, roi)
    #counter += 1


cv2.imshow('test', img)
cv2.imwrite('./testdata/sample/result.jpg', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
