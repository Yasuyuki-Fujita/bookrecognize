# 書籍の画像認識をやってみた
    本リポジトリでは、書籍の画像認識を実施した内容を記す。

## 目的（やりたいこと）
  - スマホで撮影した書籍の画像からＩＳＢＮ番号を取得する。
 （取得したＩＳＢＮをシステムの連携キーとして取得可能とする）

## 使用したAWSサービス
|サービス名            |説明                    |
|:--                  |:--                     |
|Amazon SageMaker | サービス内Jupyter notebookを使用し、モデル作成～学習済モデルを利用したに使用 |
|Amazon S3 |SageMakerと連携し、学習済モデルを格納   |
|Amazon API Gateway+Lambda | APIとして画像から学習した特定のISBNに対する結果（確率）を返却 |
[![概要](image.png)](./image.png)


## 概要   

 - 1.画像とＩＳＢＮの紐づけ（モデル作成～学習）
     - モデル作成～学習：AWS SageMaker内のJupyter notebook上にある画像分類のサンプル「Image-classification-lst-format」に手を加えを実施
       - ソース：[Image-classification-lst-format.ipynb](URL "https://github.com/Yasuyuki-Fujita/bookrecognize/blob/master/notebook/Image-classification-lst-format.ipynb")
     - 学習に使用するデータ：ISBNを画像分類項目とし、各ISBNに対し約100の画像ファイルを用意
       - データ：[256_ObjectCategories.tar](URL "./notebook/256_ObjectCategories.tar")[notebook]256_ObjectCategories.tar<br>
       フォルダ名の「.」以降の文字列で画像分類分け
            ```
            256_ObjectCategories
                ├─001.ISBN479804573X
                │      001_0001.jpg
                │      001_0002.jpg
                │       ～
                │      001_0100.jpg
                │      
                ├─002.ISBN4537256109
                │      002_0001.jpg
                │       ～
                │      002_0100.jpg
                │      
                └─003.ISBN4839964564
                        003_0001.jpg
                        ～
                        003_0100.jpg
            ```

     - SageMakerで学習済みモデルを利用した各分類毎の確率を返却するエンドポイントを作成

 - 2.画像分析判定
     - 画像分類した学習結果をSageMaker上でAPIとして公開し
