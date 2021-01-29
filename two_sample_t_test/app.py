from typing import List, NamedTuple

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash_table import DataTable
import numpy as np

import slider
from figure import draw_swarm_plot
from ttest import perform_ttest


app = dash.Dash(
    name=__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title='2標本t検定'
)
app.layout = dbc.Container(
    children=[
        dbc.Row(
            className='bg-dark text-white p-1 mb-3',
            children=dbc.Col(
                className='col-12',
                children=html.H2(children='2標本t検定')
            )
        ),
        dbc.Row(
            className='border-bottom pb-3 mb-3',
            children=[
                dbc.Col(
                    className='col-4',
                    children=html.Div(
                        className='border p-2',
                        children=[
                            html.H6(children='シード値'),
                            html.Div(
                                className='ml-3 mb-1',
                                children=[
                                    dcc.Checklist(
                                        id='checklist-give-seed',
                                        className='mr-2',
                                        style={'display': 'inline-block'},
                                        options=[{'label': '指定する', 'value': 'yes'}],
                                        value=['yes']
                                    ),
                                    dcc.Input(
                                        id='seed',
                                        type='number',
                                        style={'display': 'inline-block', 'width': 60},
                                        disabled=True,
                                        value=np.random.randint(1, 1000)
                                    )
                                ]
                            ),
                            html.H6(children='対立仮説'),
                            dcc.Dropdown(
                                id='alternative-hypothesis',
                                className='ml-3 mb-1',
                                style={'width': '240px', 'font-size': '12px'},
                                options=[
                                    {'label': 'データ群Aの平均 ≠ データ群Bの平均', 'value': 'two-sided'},
                                    {'label': 'データ群Aの平均 ＜ データ群Bの平均', 'value': 'less'},
                                    {'label': 'データ群Aの平均 ＞ データ群Bの平均', 'value': 'greater'}
                                ],
                                value='two-sided',
                                clearable=False
                            ),
                            html.H6(children='有意水準'),
                            dcc.RadioItems(
                                id='significance-level',
                                className='ml-3 mb-1',
                                labelClassName='ml-3',
                                labelStyle={'display': 'inline-block'},
                                options=[
                                    {'label': 0.05, 'value': 0.05},
                                    {'label': 0.01, 'value': 0.01}
                                ],
                                value=0.05,
                            )
                        ]
                    )
                ),
                dbc.Col(
                    className='col-4',
                    children=[
                        html.H5('データ群A'),
                        html.Div(
                            id='num-data-a',
                            className='ml-3'
                        ),
                        slider.NumDataParameterSlider(id_='slider-num-data-a').to_slider(),
                        html.Div(
                            id='loc-data-a',
                            className='ml-3'
                        ),
                        slider.LocParameterSlider(id_='slider-loc-data-a', default=-1).to_slider(),
                        html.Div(
                            id='variance-data-a',
                            className='ml-3'
                        ),
                        slider.VarianceParameterSlider(id_='slider-variance-data-a').to_slider()
                    ]
                ),
                dbc.Col(
                    className='col-4',
                    children=[
                        html.H5('データ群B'),
                        html.Div(
                            id='num-data-b',
                            className='ml-3'
                        ),
                        slider.NumDataParameterSlider(id_='slider-num-data-b').to_slider(),
                        html.Div(
                            id='loc-data-b',
                            className='ml-3'
                        ),
                        slider.LocParameterSlider(id_='slider-loc-data-b', default=1).to_slider(),
                        html.Div(
                            id='variance-data-b',
                            className='ml-3'
                        ),
                        slider.VarianceParameterSlider(id_='slider-variance-data-b', disabled=True).to_slider()
                    ]
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    className='col-6',
                    children=dcc.Graph(id='generated-data')
                ),
                dbc.Col(
                    className='col-6',
                    children=[
                        html.H5('生成データの統計情報'),
                        html.Div(
                            className='p-1 mb-2',
                            children=DataTable(
                                id='stats-table',
                                columns=[
                                    {'id': 'column-stats', 'name': ''},
                                    {'id': 'column-data-a', 'name': 'データ群A'},
                                    {'id': 'column-data-b', 'name': 'データ群B'}
                                ],
                                style_cell={'width': '33%'}
                            )
                        ),
                        html.H5('t検定の結果'),
                        html.Div(
                            id='t-test-result',
                            className='border border-success p-2 ml-2',
                            style={'white-space': 'pre', 'font-family': 'monospace', 'font-size': '14px'}
                        )
                    ]
                )
            ]
        )
    ]
)


def make_stats_table_data(data_a: np.array, data_b: np.array):
    """データの統計情報テーブルのデータを出力する

    Parameters
    ----------
    data_a : np.array
        1次元の配列
    data_b : np.array
        1次元の配列

    Returns
    -------
    list[dict[str, float]]
        テーブルの各行を表すdictのlist。
        各dictのkeyはDataTableのcolumnsに設定されたid、valueはセルの値に対応する。
    """

    assert data_a.ndim == 1
    assert data_b.ndim == 1

    class Row(NamedTuple):
        stats: str
        data_a: float
        data_b: float

    rows = [
        Row('データ数', len(data_a), len(data_b)),
        Row('標本平均', data_a.mean(), data_b.mean()),
        Row('標本分散', data_a.var(ddof=0), data_b.var(ddof=0)),
        Row('不偏分散', data_a.var(ddof=1), data_b.var(ddof=1))
    ]

    stats_table_data = [
        {'column-stats': r.stats, 'column-data-a': r.data_a, 'column-data-b': r.data_b}
        for r in rows
    ]
    return stats_table_data


@app.callback(
    output=Output('seed', 'disabled'),
    inputs=Input('checklist-give-seed', 'value')
)
def enable_seed(checklist_give_seed: List[str]):
    enable = bool(checklist_give_seed)
    return not enable


@app.callback(
    output=[
        Output('num-data-a', 'children'),
        Output('num-data-b', 'children')
    ],
    inputs=[
        Input('slider-num-data-a', 'value'),
        Input('slider-num-data-b', 'value')
    ]
)
def select_num_data(num_data_a: str, num_data_b: str):
    text_a = f'データ数 : {num_data_a}'
    text_b = f'データ数 : {num_data_b}'
    return text_a, text_b


@app.callback(
    output=[
        Output('loc-data-a', 'children'),
        Output('loc-data-b', 'children')
    ],
    inputs=[
        Input('slider-loc-data-a', 'value'),
        Input('slider-loc-data-b', 'value')
    ]
)
def select_loc(loc_a: str, loc_b: str):
    text_a = f'平均 : {loc_a}'
    text_b = f'平均 : {loc_b}'
    return text_a, text_b


@app.callback(
    output=[
        Output('variance-data-a', 'children'),
        Output('variance-data-b', 'children'),
        Output('slider-variance-data-b', 'value')
    ],
    inputs=Input('slider-variance-data-a', 'value')
)
def select_variance(variance: str):
    text_a = f'分散 : {variance}'
    text_b = f'分散 : {variance}'
    return text_a, text_b, variance


@app.callback(
    output=[
        Output('generated-data', 'figure'),
        Output('stats-table', 'data'),
        Output('t-test-result', 'children')
    ],
    inputs=[
        Input('checklist-give-seed', 'value'),
        Input('seed', 'value'),
        Input('alternative-hypothesis', 'value'),
        Input('significance-level', 'value'),
        Input('slider-num-data-a', 'value'),
        Input('slider-num-data-b', 'value'),
        Input('slider-loc-data-a', 'value'),
        Input('slider-loc-data-b', 'value'),
        Input('slider-variance-data-a', 'value'),
        Input('slider-variance-data-b', 'value')
    ]
)
def generate_data(
    checklist_give_seed: List[str], seed: int, alternative: str,
    significance_level: float, num_data_a: int, num_data_b: int,
    loc_a: float, loc_b: float, variance_a: float, variance_b: float,
):
    assert variance_a > 0
    assert variance_b > 0

    if checklist_give_seed:
        np.random.seed(seed)

    data_a = np.random.normal(loc_a, np.sqrt(variance_a), num_data_a)
    data_b = np.random.normal(loc_b, np.sqrt(variance_b), num_data_b)

    fig = draw_swarm_plot(data_a, data_b)
    stats_table_data = make_stats_table_data(data_a, data_b)
    ttest_result = perform_ttest(data_a, data_b, alternative, significance_level)

    return fig, stats_table_data, ttest_result


if __name__ == '__main__':
    app.run_server(debug=True)
