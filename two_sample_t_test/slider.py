import dash_core_components as dcc


class ParameterSlider(object):
    """パラメータのスライダーを生成するクラス

    Parameters
    ----------
    id_ : str
        dcc.Sliderに設定するid値
    min_ : int
        スライダーの最小値
    max_ : int
        スライダーの最大値
    step : float
        値変更の間隔
    default : float
        デフォルト値
    markers_step : int
        スライダー上にマークを描写する感覚
    disabled : bool, optional
        Trueの場合、値変更を無効にする。デフォルト値はFalse
    """

    def __init__(
        self,
        id_: str, min_: int, max_: int, step: float, default: float,
        markers_step: int, disabled: bool = False
    ):
        self.id_ = id_
        self.min_ = min_
        self.max_ = max_
        self.step = step
        self.default = default
        self.markers_step = markers_step
        self.disabled = disabled

    def to_slider(self) -> dcc.Slider:
        """dcc.Sliderインスタンスを生成する

        Returns
        -------
        dcc.Slider
        """

        slider = dcc.Slider(
            id=self.id_,
            min=self.min_,
            max=self.max_,
            step=self.step,
            value=self.default,
            marks={
                v: str(v)
                for v in range(self.min_, self.max_ + self.markers_step, self.markers_step)
            },
            disabled=self.disabled
        )
        return slider


class NumDataParameterSlider(ParameterSlider):
    """データ数パラメータのスライダーを生成するクラス

    Parameters
    ----------
    id_ : str
        dcc.Sliderに設定するid値
    """

    def __init__(self, id_: str):
        min_ = 10
        max_ = 50
        step = 5
        default = 20
        markers_step = 10
        ParameterSlider.__init__(self, id_, min_, max_, step, default, markers_step)


class LocParameterSlider(ParameterSlider):
    """位置パラメータのスライダーを生成するクラス

    Parameters
    ----------
    id_ : str
        dcc.Sliderに設定するid値
    default : float
        デフォルト値
    """

    def __init__(self, id_: str, default: float):
        min_ = -5
        max_ = 5
        step = 0.1
        markers_step = 1
        ParameterSlider.__init__(self, id_, min_, max_, step, default, markers_step)


class VarianceParameterSlider(ParameterSlider):
    """位置パラメータのスライダーを生成するクラス

    Parameters
    ----------
    id_ : str
        dcc.Sliderに設定するid値
    disabled : bool, optional
        Trueの場合、値変更を無効にする。デフォルト値はFalse
    """

    def __init__(self, id_: str, disabled: bool = False):
        min_ = 1
        max_ = 5
        step = 0.1
        default = 1
        markers_step = 1
        ParameterSlider.__init__(self, id_, min_, max_, step, default, markers_step, disabled=disabled)
