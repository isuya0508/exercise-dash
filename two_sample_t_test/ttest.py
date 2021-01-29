from typing import List

from scipy import stats


def perform_ttest(data_a: List[float], data_b: List[float], alternative: str, significance_level: float) -> str:
    """2標本t検定を実行し、結果のサマリを出力する

    Parameters
    ----------
    data_a : list_like[float]
    data_b : list_like[float]
    alternative : str
        対立仮説。two-sided, less, greaterのいずれか。
        参考: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html
    significance_level : float
        有意水準

    Returns
    -------
    str
    """

    t, p_value = stats.ttest_ind(data_a, data_b, equal_var=True, alternative=alternative)

    ttest_summary = write_ttest_summary(t, p_value, alternative, significance_level)
    return ttest_summary


def write_ttest_summary(t: float, p_value: float, alternative: str, significance_level: float) -> str:
    """t検定のサマリを出力する

    Parameters
    ----------
    t : float
        t検定値
    p_value : float
        p値
    alternative : str
        対立仮説。two-sided, less, greaterのいずれか。
        参考: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html
    significance_level : float
        有意水準

    Returns
    -------
    str
    """

    if p_value < significance_level:
        ttest_result = '帰無仮説は棄却される'
    else:
        ttest_result = '帰無仮説は棄却されない'

    lines = [
        'データ群の関係 - 独立',
        '帰無仮説       - データ群Aの平均 ＝ データ群Bの平均',
        '対立仮説       - {}'.format(write_formal_alternative(alternative)),
        '等分散の仮定   - あり',
        '有意水準       - {}'.format(significance_level),
        '検定方法       - スチューデントのt検定',
        't検定値        - {}'.format(t),
        'p値            - {}'.format(p_value),
        '検定結果       - {}'.format(ttest_result)
    ]

    summary = '\n'.join(lines)
    return summary


def write_formal_alternative(alternative: str) -> str:
    """正式な対立仮説を記述する

    Parameters
    ----------
    alternative : str
        対立仮説。two-sided, less, greaterのいずれか。
        参考: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html

    Returns
    -------
    str
    """

    inequality_sign_dict = {
        'two-sided': '≠',
        'less': '＜',
        'greater': '＞'
    }

    return f'データ群Aの平均 {inequality_sign_dict[alternative]} データ群Bの平均'
