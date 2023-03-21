import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Gapminder Data'),

    html.Div(children='''
        A dashboard to visualize Gapminder data.
    '''),

    dcc.Graph(id='scatter-plot'),

    dcc.Dropdown(
        id='xaxis-dropdown',
        options=[{'label': i, 'value': i} for i in df.columns[3:]],
        value='gdpPercap'
    ),

    dcc.Dropdown(
        id='yaxis-dropdown',
        options=[{'label': i, 'value': i} for i in df.columns[3:]],
        value='lifeExp'
    ),

    dcc.Graph(id='bar-chart'),

    dcc.Graph(id='line-chart')
])

# Define the callbacks for the app
@app.callback(
    Output(component_id='scatter-plot', component_property='figure'),
    [Input(component_id='xaxis-dropdown', component_property='value'),
     Input(component_id='yaxis-dropdown', component_property='value')]
)
def update_scatter_plot(xaxis_column_name, yaxis_column_name):
    fig = px.scatter(df,
                     x=xaxis_column_name,
                     y=yaxis_column_name,
                     color='continent',
                     size='pop',
                     hover_name='country',
                     log_x=True,
                     size_max=60)
    return fig

@app.callback(
    Output(component_id='bar-chart', component_property='figure'),
    [Input(component_id='yaxis-dropdown', component_property='value')]
)
def update_bar_chart(yaxis_column_name):
    data = df.groupby(['year', 'continent'])[yaxis_column_name].mean().reset_index()
    fig = px.bar(data,
                 x='year',
                 y=yaxis_column_name,
                 color='continent',
                 barmode='group')
    return fig

@app.callback(
    Output(component_id='line-chart', component_property='figure'),
    [Input(component_id='yaxis-dropdown', component_property='value')]
)
def update_line_chart(yaxis_column_name):
    data = df.groupby(['year', 'continent'])[yaxis_column_name].mean().reset_index()
    fig = go.Figure()
    for continent in data['continent'].unique():
        fig.add_trace(go.Scatter(x=data[data['continent'] == continent]['year'],
                                 y=data[data['continent'] == continent][yaxis_column_name],
                                 mode='lines',
                                 name=continent))
    fig.update_layout(xaxis_title='Year',
                      yaxis_title=yaxis_column_name)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)