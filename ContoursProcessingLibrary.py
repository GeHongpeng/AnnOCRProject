# _*_ coding= utf-8 _*_

import cv2
import numpy as np


def inside_area(r1, r2):
    """r1の長方形はr2の長方形に入るかどうかを判別する

    r1の長方形はr2の長方形に入るかどうかを判別する

    パラメータ:
        r1: 判別対象長方形
        r2: 判別される対象長方形

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
        r1: 判別対象長方形
        r2: 判別される対象長方形

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

        len = 0
        if (r1_y1 + r1_h1 < r2_y2 + r2_h2) and (r1_y1 + r1_h1 < r2_y2):
            len = r2_y2 - (r1_y1 + r1_h1)
            print len
            if len > 2:
                return False
        elif (r1_y1 + r1_h1 > r2_y2 + r2_h2) and (r1_y1 > r2_y2 + r2_h2):
            len = r1_y1 - (r2_y2 + r2_h2)
            print len
            if len > 2:
                return False

        return True
    else:
        return False


def wrap_character(rect):
    """対象文字が含まれた正方形を算出する

    対象文字が含まれた正方形を算出する

    パラメータ:
        rect: 判別対象長方形

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


def find_contours(img):
    """文字の輪郭を取得する

    文字の輪郭を取得する

    パラメータ:
        img: 対象カラー画像

    戻り値:
        輪郭情報配列

    例外:
        なし
    """
    # グレースケールに変換する
    bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ガウシアンフィルタを用いて画像の平滑化を行う
    bw = cv2.GaussianBlur(bw, (3, 3), 0)
    # 二値化を行う
    ret, thbw = cv2.threshold(bw, 230, 255, cv2.THRESH_BINARY_INV) # 印鑑: 195(二値化) 3×3(ガウシアン)  手書き: 230(二値化) 11×11(ガウシアン)
    # 収縮処理を行う
    thbw = cv2.erode(thbw, np.ones((2, 2), np.uint8), iterations=2)

    #cv2.imshow('thbw', thbw)
    #cv2.imwrite('./testdata/sample/result2.jpg', thbw)

    # 輪郭を検出する
    contours, hierarchy = cv2.findContours(thbw.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 面積でソートする
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # 輪郭を返す
    return contours


def exclude_inadequacy_contours(img, contours):
    """不備な輪郭を除外する

    不備な輪郭を除外する

    パラメータ:
        img: 対象カラー画像
        contours: 輪郭

    戻り値:
        輪郭情報配列

    例外:
        なし
    """
    counter = 1
    rectangles = []
    for c in contours:
        # 長方形の座標情報を取得
        r = c_x, c_y, c_w, c_h = cv2.boundingRect(c)
        # 輪郭エリアを算出する
        a = cv2.contourArea(c)
        b = (img.shape[0]-3) * (img.shape[1]-3)
        # 輪郭エリアの閾値を設定する
        contour_area_Threshold = 70
        # 既存の長方形に含まれるかどうかのフラグ
        is_inside = False
        # 既存の長方形に含まれるかどうかの判別処理を実施する
        for q in rectangles:
            if inside_area(r, q):
                is_inside = True
                break
        # 既存の長方形に含まれていない場合
        if not is_inside:
            #
            #if not a == b:
            if (not a == b) and (a > contour_area_Threshold):
                #
                target_r = r
                for i, q in enumerate(rectangles):
                    if inside_x_axis(target_r, q):
                        # 長方形の座標情報を初期化する
                        target_x = 0
                        target_y = 0
                        target_w = 0
                        target_h = 0
                        # 判別対象になる長方形の座標情報を取得する
                        x1, y1, w1, h1 = target_r
                        x2, y2, w2, h2 = q
                        # 上下の長方形をマージするための左上座標を算出する
                        if x1 <= x2:
                            target_x = x1
                        else:
                            target_x = x2
                        if y1 <= y2:
                            target_y = y1
                        else:
                            target_y = y2
                        # 上下の長方形をマージするための幅と高さを算出する
                        if x1 + w1 >= x2 + w2:
                            target_w = x1 + w1 - target_x
                        else:
                            target_w = x2 + w2 - target_x
                        if y1 + h1 >= y2 + h2:
                            target_h = y1 + h1 - target_y
                        else:
                            target_h = y2 + h2 - target_y
                        # 長方形面積を算出する
                        area1 = w1 * h1
                        area2 = w2 * h2
                        if (area1 / area2 > 0.5) or (area2 / area1 > 0.5):
                            rectangles.pop(i)
                            target_r = target_x, target_y, target_w, target_h

                        #cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 1)
                        #cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 1)
                        # ループから抜ける
                        break
                # 長方形配列に追加する
                rectangles.append(target_r)
    # 長方形配列を返す
    return rectangles

