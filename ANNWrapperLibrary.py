# _*_ coding= utf-8 _*_
import cv2
import numpy as np


def create_ann(layer_sizes):
    """ANNを生成する

        ANNモデルのインスタンスを作成する

        パラメータ:
            layer_sizes: ANNモデルのレイヤーサイズ

        戻り値:
            ANNインスタンス

        例外:
            なし
    """
    # ANNインスタンスを生成する
    ann = cv2.ANN_MLP()
    # ANNのレイヤーを設定する
    ann.create(layer_sizes)
    # ANNインスタンスを返す
    return ann


def train(ann, train_data, train_resp):
    """学習を実施する

            ANN方式で学習データを使って学習を実施する

            パラメータ:
                ann: ANNモデルのインスタンス
                train_data: 学習データ
                train_resp: 学習データに対応する結果

            戻り値:
                ANNインスタンス

            例外:
                なし
    """
    # Set criteria
    criteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001)
    # Set parameters
    params = dict(term_crit=criteria,
                  train_method=cv2.ANN_MLP_TRAIN_PARAMS_BACKPROP,
                  bp_dw_scale=0.001,
                  bp_moment_scale=0.1)
    # Start training
    ann.train(train_data, train_resp, None, params=params)
    # ANNインスタンスを返す
    return ann


def evaluate(ann, test_data):
    """評価を実施する

            評価データを使って評価を実施する。評価用画像を表示し、予測結果を出力する

            パラメータ:
                ann: ANNモデルのインスタンス
                test_data: 評価用データ

            戻り値:
                なし

            例外:
                なし
    """
    # サンプルデータを取得する
    sample_data = np.array(test_data[0][0].ravel(), dtype=np.float32)
    # 画像に変換する
    sample_image = sample_data.reshape(28, 28)
    # 画像を表示する
    cv2.imshow("sample", sample_image)
    cv2.waitKey(0)
    # 予測結果を出力する
    print ann.predict(sample_data)


def predict(ann, sample_image):
    """予測を実施する

            サンプルデータを使って予測を実施する。予測結果を出力する

            パラメータ:
                ann: ANNモデルのインスタンス
                test_data: 評価用データ

            戻り値:
                なし

            例外:
                なし
    """
    # 対象画像を取得する
    target_image = sample_image.copy()
    # 画像サイズを標準化する
    rows, cols = target_image.shaple
    if (rows != 28 or cols != 28) and rows * cols > 0:
        target_image = cv2.resize(target_image, (28, 28), interpolation=cv2.INTER_CUBIC)
    # 予測結果を返す
    return ann.predict(np.array([target_image.ravel()], dtype=np.float32))
