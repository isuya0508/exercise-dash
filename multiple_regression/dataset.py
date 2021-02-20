from typing import List

import pandas as pd
from sklearn.datasets import load_boston


class BostonHousePrices():
    """Boston House Pricesのデータセットクラス

    scikit-learnから取得したデータセットを保持し、データセットを扱うための
    プロパティやメソッドを提供する。
    """
    def __init__(self):
        self.data = load_boston()

    @property
    def features(self) -> List[str]:
        """回帰における特徴量の属性名のリストを返す

        Returns
        -------
        features : List[str]
        """
        return self.data.feature_names

    @property
    def target(self) -> str:
        """回帰の対象となる属性名「MEDV」を返す

        Returns
        -------
        target : str
        """
        target = 'MEDV'
        return target

    def as_df(self) -> pd.DataFrame:
        """データセットをpandas.DataFrameで取得する

        Returns
        -------
        df : pandas.DataFrame
        """
        df = pd.DataFrame(self.data.data, columns=self.features)
        df[self.target] = self.data.target
        return df

    def attribute_description_lines(self) -> List[str]:
        """各属性の説明のリストを取得する

        self.data.DESCRから属性の説明が書かれている行を抜き出す。

        Returns
        -------
        List[str]
        """

        # self.data.DESCRから、属性の説明が書かれている行を抜き出し、先頭から「- 」まで削除する。
        # 対応する各行は、「        - <属性名>     <説明>」という形式であり、13行目から26行目に書かれている。
        descr_lines = self.data.DESCR.splitlines()
        attribute_descr_lines = [
            line.lstrip().lstrip('- ')
            for line in descr_lines[12: 26]
        ]

        return attribute_descr_lines
