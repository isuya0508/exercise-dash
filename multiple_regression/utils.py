from statsmodels.regression import linear_model


def retrieve_summary_texts(results: linear_model.OLSResults, alpha: float):
    """回帰結果のsummaryをテキストで取得する

    Parameters
    ----------
    results : statsmodels.regression.linear_model.OLSResults
        回帰結果
    alpha : float
        有意水準。0と1の間の数値。

    Returns
    -------
    tables : List[str]
        サマリテーブル、特徴量テーブル、残差テーブルのテキストのリスト
    additional_explanations : str
        回帰に関する補足説明のテキスト
    """

    assert 0 < alpha < 1

    summary = results.summary(alpha=alpha)
    # summary.tables[0].titleには、'OLS Regression Results'のような表のタイトルが設定されている。
    # これを削除し、タイトルが表示されないようにする。
    summary.tables[0].title = None

    tables = [table.as_text() for table in summary.tables]
    additional_explanations = summary.extra_txt

    return tables, additional_explanations
