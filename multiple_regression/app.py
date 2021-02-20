from typing import List

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from statsmodels.regression import linear_model
import statsmodels.tools as sm_tools

from dataset import BostonHousePrices
from utils import retrieve_summary_texts


dataset_boston = BostonHousePrices()
df = dataset_boston.as_df()

attribute_description = [f'{line}\n' for line in dataset_boston.attribute_description_lines()]

NUM_DEFAULT_FEATURES = 1
SIGNIFICANCE_LEVELS = [0.05, 0.01]


app = dash.Dash(
    name=__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title='重回帰分析'
)
app.layout = dbc.Container(
    children=[
        dbc.Row(
            className='bg-dark text-white p-1 mb-2',
            children=[
                dbc.Col(
                    className='col-12',
                    children=[
                        html.H3('重回帰分析')
                    ]
                )
            ]
        ),
        dbc.Row(
            className='mb-1',
            children=[
                dbc.Col(
                    className='col-4',
                    children=[
                        html.Div(
                            className='border p-2 mb-1',
                            children=[
                                html.H6('特徴量を選択'),
                                dcc.Dropdown(
                                    id='selected-features',
                                    className='mb-1',
                                    options=[{'label': f, 'value': f} for f in dataset_boston.features],
                                    multi=True,
                                    value=dataset_boston.features[: NUM_DEFAULT_FEATURES],
                                    clearable=False
                                ),
                                dcc.Checklist(
                                    id='constant-checklist',
                                    options=[{'label': '定数項を追加', 'value': 'add_constant'}],
                                    value=['add_constant']
                                ),
                                dcc.Dropdown(
                                    id='significance-level',
                                    options=[
                                        {'label': f'有意水準{int(alpha*100)}%', 'value': alpha}
                                        for alpha in SIGNIFICANCE_LEVELS
                                    ],
                                    value=SIGNIFICANCE_LEVELS[0],
                                    clearable=False
                                ),
                            ]
                        ),
                        dbc.Button(
                            id='attribute-description-button',
                            size='sm',
                            color='info',
                            className='border mb-1',
                            outline=True,
                            n_clicks=0,
                            children='属性の説明を表示',
                        ),
                        dbc.Collapse(
                            id='attribute-description-collapse',
                            is_open=False,
                            children=[
                                html.Pre(
                                    id='attribute-description',
                                    style={'font-size': '12.5px'},
                                    children=attribute_description
                                )
                            ]
                        )

                    ]
                ),
                dbc.Col(
                    className='col-4',
                    children=[
                        dcc.Graph(id='scatter-plot'),
                        html.Div(
                            style={'position': 'relative'},
                            children=[
                                html.Div(
                                    style={'display': 'inline-block'},
                                    children='対象の特徴量'
                                ),
                                dcc.Dropdown(
                                    id='scatter-plot-feature',
                                    className='ml-3',
                                    style={
                                        'position': 'absolute',
                                        'top': '-25%',
                                        'display': 'inline-block',
                                        'width': 150
                                    },
                                    options=[{'label': f, 'value': f} for f in dataset_boston.features],
                                    value=dataset_boston.features[0],
                                    clearable=False
                                )
                            ]
                        )
                    ]
                ),
                dbc.Col(
                    className='col-4',
                    children=[
                        dcc.Graph(id='correlation-heatmap'),
                        dcc.Checklist(
                            id='correlation-heatmap-checklist',
                            options=[{'label': '選択した特徴量とMEDVに限定', 'value': 'only_selected'}],
                            value=[]
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    className='col-12',
                    children=[
                        html.H4('重回帰分析 結果')
                    ]
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    className='col-6',
                    children=[
                        html.Pre(
                            id='summary-table',
                            style={'font-size': '12.5px'}
                        ),
                        html.Pre(
                            id='residuals-table',
                            style={'font-size': '12.5px'}
                        )
                    ]
                ),
                dbc.Col(
                    className='col-6',
                    children=[
                        html.Pre(
                            id='features-table',
                            style={'font-size': '12.5px'}
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    className='col-12',
                    children=[
                        html.Pre(id='additional-explanations')
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    output=Output('correlation-heatmap', 'figure'),
    inputs=[
        Input('selected-features', 'value'),
        Input('correlation-heatmap-checklist', 'value')
    ]
)
def draw_corr_heatmap(features: List[str], checklist_only_selected: List[str]):
    """相関係数ヒートマップを描写する

    Parameters
    ----------
    checklist_only_selected : List[str]
        特徴量の限定のチェックリスト。チェックされている場合は['add_only_selected']、
        されていない場合は空のリストになる。
        チェックされている場合、選択された特徴量とMEDVのみに対して、ヒートマップを作成する。
        されていない場合は、全属性に対してヒートマップを作成する。

    Returns
    -------
    fig : plotly.graph_objects.Figure
        相関係数のヒートマップ
    """
    if checklist_only_selected:
        features_corr = features + [dataset_boston.target]
        df_corr = df[features_corr].corr()
    else:
        df_corr = df.corr()

    # df_corrをgo.Heatmapで表示させると行が反転したヒートマップになる。
    # そのため、df_corrのcolumnsを反転させたdf_corr_reverseを使う。
    attributes_reversed = list(reversed(df_corr.columns))
    df_corr_reversed = df_corr[attributes_reversed]

    fig = go.Figure(
        data=go.Heatmap(
            z=df_corr_reversed,
            x=df_corr.columns,
            y=attributes_reversed,
            zmin=-1,
            zmax=1,
            colorscale=[[0, 'red'], [0.5, 'white'], [1.0, 'blue']]
        )
    )
    fig.update_layout(
        title_text='相関係数ヒートマップ',
        title_x=0.5,
        width=400,
        height=400
    )
    return fig


@app.callback(
    output=Output('scatter-plot', 'figure'),
    inputs=Input('scatter-plot-feature', 'value'),
)
def draw_scatter_plot(feature: str):
    """対象の特徴量とtargetであるMEDVの散布図を描写する

    Parameters
    ----------
    feature : str
        対象の特徴量

    Returns
    -------
    fig : plotly.graph_objects
        散布図
    """
    x = df[feature]
    y = df[dataset_boston.target]

    fig = go.Figure(
        data=go.Scatter(
            x=x,
            y=y,
            mode='markers',
            text=['x', 'y']
        )
    )
    fig.update_layout(
        title_text=f'散布図 ({feature} - {dataset_boston.target})',
        title_x=0.5,
        xaxis_title=feature,
        yaxis_title=dataset_boston.target,
        template='plotly_white',
        width=400,
        height=400
    )
    return fig


@app.callback(
    output=Output('attribute-description-collapse', 'is_open'),
    inputs=[Input('attribute-description-button', 'n_clicks')],
    state=[State('attribute-description-collapse', 'is_open')]
)
def display_attribute_description(n_clicks: int, is_open: bool):
    """「属性の説明を表示」ボタンが押されたときに、表示の状態を切り替える

    Parameters
    ----------
    n_clicks : int
        ボタンが押された回数。
    is_open : bool
        属性の説明の表示状態。

    Returns
    -------
    bool
        切り替え後の属性の説明の表示状態
    """

    if not n_clicks:
        return False
    else:
        return not is_open


@app.callback(
    output=[
        Output('summary-table', 'children'),
        Output('features-table', 'children'),
        Output('residuals-table', 'children'),
        Output('additional-explanations', 'children')
    ],
    inputs=[
        Input('selected-features', 'value'),
        Input('constant-checklist', 'value'),
        Input('significance-level', 'value'),
    ]
)
def perform_regression(
    features: List[str],
    checklist_constant: List[str],
    alpha: float
):
    """重回帰を実行する

    Parameters
    ----------
    features : List[str]
        選択された特徴量
    checklist_constant : List[str]
        定数項追加のチェックリスト。チェックされている場合は['add_constant']、
        されていない場合は空のリストになる
    alpha : float
        有意水準。0と1の間の数値。

    Returns
    -------
    summary_table : str
        サマリテーブルのテキスト
    features_table : str
        特徴量テーブルのテキスト
    residuals_table : str
        残差テーブルのテキスト
    additional_explanations : str
        回帰に関する補足説明のテキスト
    """

    X = df[features]
    y = df[dataset_boston.target]
    if checklist_constant:
        X = sm_tools.add_constant(X)

    results_regression = linear_model.OLS(y, X).fit()

    tables, additional_explanations = retrieve_summary_texts(results_regression, alpha)
    summary_table, features_table, residuals_table = tables

    return summary_table, features_table, residuals_table, additional_explanations


if __name__ == '__main__':
    app.run_server(debug=True)
