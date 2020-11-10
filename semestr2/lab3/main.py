import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import numpy

title = '|Состояние         |           Среднее время              |           Cреднее относительное время\n\
|                           |   пребывания системы            |                пребывания системы\n\
|                           |       в этом состоянии               |                 в этом состоянии\n'

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Button('+', id='adding-button', n_clicks=0),
        html.Button('-', id='removing-button', n_clicks=0)
    ], style={'height': 50}),

    dash_table.DataTable(
        id='table',
        columns=(
            [{'id': '0', 'name': ''}] +
            [{'id': '{}'.format(i), 'name': '{}'.format(i)}
                for i in range(1, 4)]
        ),
        data=[
            {'0': (j + 1) for i in range(1, 3)}
            for j in range(3)
        ],
        editable=True,
        style_table={
            'width': '30%'
        },
    ),

    html.Button('Time', id='time-button', n_clicks=0),

    html.Div([
        dcc.Textarea(
            id='textarea-example',
            value=title,
            style={'width': '35%', 'height': 80})
    ])
])


@app.callback(
    Output('table', 'columns'),
    [Input('adding-button', 'n_clicks')],
    State('table', 'columns'))
def update_columns(n_clicks, existing_columns):
    if n_clicks > 0:
        existing_columns.append({
            'id': str(len(existing_columns)),
            'name': str(len(existing_columns))
        })
    return existing_columns


@app.callback(
    Output('table', 'data'),
    [Input('adding-button', 'n_clicks')],
    [State('table', 'data'),
     State('table', 'columns')])
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
        rows[len(columns) - 1]['0'] = str(len(columns))
    return rows


@app.callback(
    Output('textarea-example', 'value'),
    [Input('time-button', 'n_clicks')],
    State('table', 'data'))
def print_data(n_clicks, data):
    if n_clicks > 0:
        m = len(data)
        dictlist = [0] * m
        for i in range(m):
            dictlist[i] = [0] * m

        i = 0
        for d in data:
            for j in range(1, len(data) + 1):
                try:
                    dictlist[i][j - 1] = int(d[str(j)])
                except Exception:
                    dictlist[i][j - 1] = 0
            i += 1
        out, time = solve(dictlist)
        string = title
        for i in range(len(out)):
            string += "|{:^26d}|{:^48.3f}|{:^75.3f}\n".format(i + 1, time[i], out[i])
        return string


def solve(array):
    n = len(array)
    coef = numpy.zeros((n, n))
    sum = numpy.zeros(n)
    for i in range(n):
        for j in range(n):
            sum[i] += array[i][j]
            coef[i][j] = array[j][i]
        coef[i][i] = -sum[i]

    m = numpy.zeros(n)
    m[-1] = 1

    for i in range(n):
        coef[-1][i] = 1
    out = numpy.linalg.solve(coef, m)

    time = numpy.zeros(n)
    for i in range(n):
        time[i] = (1 - out[i]) / out[i] / sum[i]
    return out, time


if __name__ == '__main__':
    app.run_server(debug=True)
