# _*_ coding= utf-8 _*_
import cv2
import numpy as np
import glob
from random import randint


def inside_area(r1, r2):
    """r1の四角形はr2の四角形に入るかどうかを判別する

    r1の四角形はr2の四角形に入るかどうかを判別する

    パラメータ:
        r1: 判別対象四角形
        r2: 判別される対象四角形

    戻り値:
        True/False

    例外:
        なし
    """
    # 座標情報を取得する
    r1_x1, r1_y1, r1_w1, r1_h1 = r1
    r2_x2, r2_y2, r2_w2, r2_h2 = r2
    # 判別結果を返す
    if (r1_x1 >= r2_x2) and (r1_y1 >= r2_y2) and (r1_x1 + r1_w1 <= r2_x2 + r2_w2) and (r1_y1 + r1_h1 <= r2_y2 + r2_h2):
        return True
    else:
        return False


def inside_x_axis(r1, r2):
    """X軸を重なっているかどうかを判別する

    X軸を重なっているかどうかを判別する

    パラメータ:
        r1: 判別対象四角形
        r2: 判別される対象四角形

    戻り値:
        True/False

    例外:
        なし
    """
    # 座標情報を取得する
    r1_x1, r1_y1, r1_w1, r1_h1 = r1
    r2_x2, r2_y2, r2_w2, r2_h2 = r2
    # 判別結果を返す
    # if ((r1_x1 < r2_x2) and (r1_x1+r1_w1 > r2_x2))
    #        or ((r1_x1 < r2_x2+r2_w2) and (r1_x1+r1_w1 > r2_x2+r2_w2))
    #        or ((r1_x1 > r2_x2) and (r1_x1+r1_w1 < r2_x2 + r2_w2)):
    if ((r1_x1 <= r2_x2) and (r1_x1+r1_w1 >= r2_x2)) \
            or ((r1_x1 <= r2_x2+r2_w2) and (r1_x1+r1_w1 >= r2_x2+r2_w2)) \
            or ((r1_x1 > r2_x2) and (r1_x1+r1_w1 < r2_x2+r2_w2)):
        return True
    else:
        return False


def wrap_character(rect):
    """対象文字が含まれた正方形を算出する

    対象文字が含まれた正方形を算出する

    パラメータ:
        rect: 判別対象四角形

    戻り値:
        正方形の座標情報

    例外:
        なし
    """
    # 座標情報を取得する
    rect_x, rect_y, rect_w, rect_h = rect
    # パディング値を設定する
    padding = 1
    # 重心点を算出する
    hcenter = rect_x + rect_w/2
    vcenter = rect_y + rect_h/2
    # 正方形を算出する
    if rect_h > rect_w:
        rect_w = rect_h
        rect_x = hcenter - (rect_w/2)
    else:
        rect_h = rect_w
        rect_y = vcenter - (rect_h/2)
    # パディングに加えた正方形を返す
    return rect_x-padding, rect_y-padding, rect_w+padding, rect_h+padding


# 画像を読み込む
img = cv2.imread('./testdata/sample/sample8.jpg', 1)


"""
画像の前処理
"""
# グレースケールに変換する
bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ガウシアンフィルタを用いて画像の平滑化を行う
bw = cv2.GaussianBlur(bw, (3, 3), 0)
# 二値化を行う
ret, thbw = cv2.threshold(bw, 215, 255, cv2.THRESH_BINARY_INV)
# 収縮処理を行う
thbw = cv2.erode(thbw, np.ones((2, 2), np.uint8), iterations=2)


"""
文字の輪郭を取得
"""
# 輪郭を検出する
cntrs, hier = cv2.findContours(thbw.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# 面積でソートする
cntrs = sorted(cntrs, key=cv2.contourArea, reverse=True)


"""
不備な輪郭を除外する
"""
counter = 1
rectangles = []
for c in cntrs:
    #
    r = c_x, c_y, c_w, c_h = cv2.boundingRect(c)
    a = cv2.contourArea(c)
    b = (img.shape[0]-3) * (img.shape[1]-3)
    #
    contour_area_Threshold = 70
    is_inside = False
    #
    for q in rectangles:
        if inside_area(r, q):
            is_inside = True
            break
    #
    if not is_inside:
        # print a
        #cv2.rectangle(img, (c_x, c_y), (c_x + c_w, c_y + c_h), (255, 0, 0), 1)
        #
        if (not a == b) and (a > contour_area_Threshold):
            #
            target_r = r
            for i, q in enumerate(rectangles):
                if inside_x_axis(target_r, q):
                    #
                    target_x = 0
                    target_y = 0
                    target_w = 0
                    target_h = 0
                    #
                    x1, y1, w1, h1 = target_r
                    x2, y2, w2, h2 = q
                    #
                    if x1 <= x2:
                        target_x = x1
                    else:
                        target_x = x2
                    if y1 <= y2:
                        target_y = y1
                    else:
                        target_y = y2
                    #
                    if x1 + w1 >= x2 + w2:
                        target_w = x1 + w1 - target_x
                    else:
                        target_w = x2 + w2 - target_x
                    if y1 + h1 >= y2 + h2:
                        target_h = y1 + h1 - target_y
                    else:
                        target_h = y2 + h2 - target_y
                    #

                    area1 = w1 * h1
                    area2 = w2 * h2
                    if (area1 / area2 > 0.5) or (area2 / area1 > 0.5):
                        rectangles.pop(i)
                        target_r = target_x, target_y, target_w, target_h

                    #cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 1)
                    #cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 1)

                    break

            rectangles.append(target_r)


"""
各文字の画像を取得する
"""
for r in rectangles:
    #
    x, y, w, h = r
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
    #print x, y, w, h

    """
    wd_x, wd_y, wd_w, wd_h = wrap_character(r)
    if wd_x < 0:
        wd_x = 0
    if wd_y < 0:
        wd_y = 0
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
