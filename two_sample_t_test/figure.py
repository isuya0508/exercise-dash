from typing import List

import plotly.graph_objects as go


def draw_swarm_plot(data_a: List[float], data_b: List[float]) -> go.Figure:
    """２つのデータ群のSwarm Plotを出力する

    Parameters
    ----------
    data_a : list_like[float]
    data_b : list_like[float]

    Returns
    -------
    go.Figure
    """

    fig = go.Figure()
    fig.add_trace(
        swarm_plot_box(data_a, 'データ群A')
    ),
    fig.add_trace(
        swarm_plot_box(data_b, 'データ群B')
    ),
    fig.update_layout(
        title_text='生成データ Swarm Plot',
        title_x=0.5,
        showlegend=False,
        template='plotly_white'
    )
    return fig


def swarm_plot_box(data: List[float], name: str) -> go.Box:
    """データ群のSwarm Plotを出力する

    Parameters
    ----------
    data : list_like[float]
    name : str
        データ群の名前

    Returns
    -------
    go.Box
    """

    # 箱ひげ図を消すために、fillcolor、line、pointsposの引数を追加する
    # 参考: https://github.com/plotly/plotly.js/issues/4021
    box = go.Box(
        y=data,
        name=name,
        boxpoints='all',
        fillcolor='rgba(0, 0, 0, 0)',
        line={'width': 0},
        pointpos=0,
        hoveron='points'
    )
    return box
