import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas_datareader.data as web
import datetime

start = datetime.datetime(2017,1,1)
end = datetime.datetime(2019,4,25)

stock= 'TSLA'

df = web.DataReader(stock, 'yahoo', start, end)

app = dash.Dash()

app.layout = html.Div(children=[
        html.H1(children="Hello dash"),
        
        
        
        
        html.Div(children='''
                 symbol to graph:
        '''),
                 
        dcc.Input(id='input', value='', type='text'),
        html.Div(id='output-graph')
])

@app.callback(
        Output(component_id='output-graph', component_property='children'),
        [Input(component_id='input', component_property='value')]
        )

def update_graph(input_data):
    df = web.DataReader(input_data, 'yahoo', start, end)
    
    return dcc.Graph(
            id='example-graph',
            figure={
                    'data': [
                            {'x': df.index, 'y': df.Close, 'type': 'line', 'name': input_data},
                    ],
                    'layout': {
                            'title': input_data        
                    }
            }
    )

if __name__ == '__main__':
    app.run_server(debug=True)

