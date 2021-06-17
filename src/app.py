import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from DataProcess import *

app = dash.Dash()
df_school_type = pd.read_csv(
    '../lab3_datasets/college-salaries/salaries-by-college-type.csv')
df_school_region = pd.read_csv(
    '../lab3_datasets/college-salaries/salaries-by-region.csv')
df_school_type = data_handle(df_school_type)

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='school_type_or_region',
                options=[{'label': i, 'value': i} for i in ['School Type', 'Region']],
                value='School Type'
            )
        ],
            style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='salary_type',
                options=[{'label': i, 'value': i} for i in get_salary_type()],
                value='Mid-Career Median Salary'
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            # 左边的柱状图
            id='start_mid_salary_compare',

        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        # 右边的箱型图
        dcc.Graph(id='salary_box')
    ], style={'display': 'inline-block', 'width': '49%'}),
    html.Div([
        # 下边的Sunburst图
        dcc.Graph(id='sunburst_salary_box'),

    ], style={'display': 'inline-block', 'width': '49%'}),
    html.Div([
        # 具体学校的图片
        dcc.Graph(id='certain_school'),
    ], style={'display': 'inline-block', 'width': '49%'}),

])


@app.callback(
    dash.dependencies.Output('start_mid_salary_compare', 'figure'),
    [dash.dependencies.Input('school_type_or_region', 'value')])
def update_start_mid_salary_compare_graph(school_type_or_region):
    graph_date = get_start_mid_salary_compare_data(school_type_or_region)
    trace_1 = go.Bar(
        x=graph_date['x'],
        y=graph_date['Starting Median Salary'],
        name='Starting Median Salary'
    )
    trace_2 = go.Bar(
        x=graph_date['x'],
        y=graph_date['Mid-Career Median Salary'],
        name='Mid-Career Median Salary'
    )

    trace = [trace_1, trace_2]
    layout = go.Layout(
        title=school_type_or_region + ' --- Salary Graph',
        # 横坐标设置
        xaxis={
            'title': school_type_or_region,
        },
        # 纵坐标设置
        yaxis={
            'title': 'Salary',
        },
        margin={'l': 50, 'b': 30, 't': 50, 'r': 0},
        height=450,
        hovermode='closest'
    )
    return {
        'data': trace,
        'layout': layout
    }


@app.callback(
    dash.dependencies.Output('salary_box', 'figure'),
    [dash.dependencies.Input('school_type_or_region', 'value'),
     dash.dependencies.Input('salary_type', 'value')])
def update_salary_box_graph(school_type_or_region, salary_type):
    graph_date = get_salary_box_data(school_type_or_region, salary_type)
    trace = []
    for i in range(len(graph_date['x'])):
        trace.append(go.Box(y=np.array(graph_date['y'][i])[0], name=graph_date['x'][i]))

    layout = go.Layout(
        title=school_type_or_region + ' --- Salary Distribution',
        # 横坐标设置
        xaxis={
            'title': school_type_or_region,
        },
        # 纵坐标设置
        yaxis={
            'title': 'Salary Distribution',
        },
        margin={'l': 50, 'b': 30, 't': 50, 'r': 0},
        height=450,
        hovermode='closest'
    )
    return {
        'data': trace,
        'layout': layout
    }


@app.callback(
    dash.dependencies.Output('sunburst_salary_box', 'figure'),
    [dash.dependencies.Input('school_type_or_region', 'value')])
def update_sunburst_salary_box_graph(school_type_or_region):
    graph_date = get_data(school_type_or_region)
    fig = px.sunburst(
        graph_date,
        path=[school_type_or_region, 'School Name'],
        values='Mid-Career Median Salary',
        branchvalues='total',
        color='Mid-Career Median Salary',
        color_continuous_scale='RdBu',
        title='sunburst graph',
        hover_data=['School Name']

    )

    fig.layout.height = 600
    fig.layout.margin = {'l': 50, 'b': 30, 't': 50, 'r': 0}
    fig.layout.title = 'sunburst graph'
    fig.layout.hovermode = 'closest'

    return {
        'data': fig.data,
        'layout': fig.layout
    }


@app.callback(
    dash.dependencies.Output('certain_school', 'figure'),
    [dash.dependencies.Input('sunburst_salary_box', 'hoverData'),
     dash.dependencies.Input('school_type_or_region', 'value')])
def update_certain_school_graph(hoverData, school_type_or_region):
    school_name = hoverData['points'][0]['label'].strip()
    graph = get_data(school_type_or_region)
    yArray = []
    if school_name not in get_school_regions() and school_name not in get_school_types():
        dff = graph[graph['School Name'] == school_name]
        yArray = np.array(dff)[0][3:]
    elif school_name in get_school_types():
        yArray = get_media_salary_by_certain_school_type(graph, school_name)
    elif school_name in get_school_regions():
        yArray = get_media_salary_by_certain_school_region(graph, school_name)
    adjust_array_data(yArray)

    return {
        'data': [go.Scatter(
            x=['10', '25', '50', '75', '90'],
            y=yArray,
            mode='lines+markers',
            line=dict(
                color='rgba(255, 182, 193)',
                width=1
            ),
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            title='Salary Of Certain School, School Type Or Region',
            # 横坐标设置
            xaxis={
                'title': 'Mid-Career (x)th Percentile Salary',
                'tickmode': 'auto', 'nticks': 10, 'tickwidth': 0.1,
            },
            # 纵坐标设置
            yaxis={
                'title': school_name,
            },
            margin={'l': 60, 'b': 80, 't': 50, 'r': 0},
            height=550,
            width=700,
            hovermode='closest'
        )
    }


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    dataInit()
    app.run_server(port=8090)
