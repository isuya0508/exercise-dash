from typing import Union

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
from sqlalchemy import create_engine

from database import db_path
import sql_templates


app = dash.Dash(
    name=__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title='Toy SQL Application'
)
app.layout = dbc.Container(
    children=[
        dbc.Row(
            className='bg-dark text-white p-1 mb-4',
            children=dbc.Col(
                className='col-12',
                children=html.H2(children='Toy SQL Application')
            )
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    className='col-6 mb-3',
                    children=[
                        html.H5(children='SQL文'),
                        html.Div(
                            className='border border-info p-2 ml-4 mt-3 mb-3',
                            children=[
                                dcc.Dropdown(
                                    className='sm mb-1',
                                    id='sql-template',
                                    options=[
                                        {'label': 'ドイツ語の国を人口が多い順に取得する', 'value': 'german_lines'},
                                        {'label': '宗教ごとに国を数える', 'value': 'count_by_religion_lines'},
                                        {'label': '国名に「j」を含む国を取得する', 'value': 'contain_j_lines'}
                                    ]
                                ),
                                dbc.Button(
                                    id='sql-template-button',
                                    color='info',
                                    size='sm',
                                    children='テンプレートを挿入'
                                )
                            ]
                        ),
                        dcc.Textarea(
                            id='sql-text',
                            style={'width': '100%', 'height': 240},
                        ),
                        dbc.Button(
                            id='sql-execution-button',
                            className='mr-1',
                            color='primary',
                            outline=True,
                            n_clicks=0,
                            children='実行'
                        ),
                    ]
                ),
                dbc.Col(
                    className='col-6',
                    children=[
                        html.H5(children='ER図'),
                        html.Embed(
                            width='100%',
                            height=400,
                            src=app.get_asset_url('erd.pdf')
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    className='col-12',
                    children=html.Div(id='sql-result')
                )
            ]
        )
    ]
)


@app.callback(
    output=Output('sql-text', 'value'),
    inputs=Input('sql-template-button', 'n_clicks'),
    state=State('sql-template', 'value')
)
def write_sql_template(n_clicks: int, template_name: Union[str, None]) -> str:
    if template_name is None:
        return ''
    else:
        lines = getattr(sql_templates, template_name)
        sql_text = '\n'.join(lines)
        return sql_text


@app.callback(
    output=Output('sql-result', 'children'),
    inputs=Input('sql-execution-button', 'n_clicks'),
    state=State('sql-text', 'value')
)
def execute_sql(n_clicks: int, sql_text: str):
    if n_clicks:
        engine = create_engine(f'sqlite:///{db_path}')
        df = pd.read_sql_query(sql_text, engine)

        table = dbc.Table.from_dataframe(
            df,
            bordered=True,
            hover=True
        )
        return table

    else:
        component = html.Div(
            className='alert alert-info',
            children='SQLクエリの結果が表示されます'
        )
        return component


if __name__ == '__main__':
    app.run_server(debug=True)
