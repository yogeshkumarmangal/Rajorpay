import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import dropbox
from plotly.subplots import make_subplots
# Step 1. Launch the application
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {'background': '#000000'}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
# Step 2. Import the dataset
dbx = dropbox.Dropbox("5uSdWA0gd2UAAAAAAAAAAauPVaO_t_nlwRgP3YzwZ8-2HlxYFWRLUrmTAgk4F4b7")
for entry in dbx.files_list_folder('').entries:
   aa=entry.name
   dd=entry.name
   if aa=='Rajaor Dashboard.csv':
       bb=entry.id
       resultresult =dbx.files_get_temporary_link(bb)
       cc=resultresult.link
   if dd=="RajaorPay Dasboard Table.csv":
      ee=entry.id
      resultresult =dbx.files_get_temporary_link(ee)
      ff=resultresult.link
      
st = pd.read_csv(cc)
df = pd.read_csv(ff)
# dropdown options
features = ['Amount','Number Of Person']
opts = [{'label' : i, 'value' : i} for i in features]

# range slider options
st['Date'] = pd.to_datetime(st.Date,format='%d-%m-%Y')
# Step 3. Create a plotly figure
fig = make_subplots(
    rows=2, cols=2,
    column_widths=[0.5, 0.5],
    row_heights=[0.5,0.5])
fig.add_trace(
    go.Bar(name='Payment Per Day',x=st.Date,y=st['Amount'], marker=dict(color="blue"), showlegend=True),
    row=1, col=1
)
fig.add_trace(
    go.Bar(name='Person Per Day',x=st.Date,y=st['Number Of Person'], marker=dict(color="crimson"), showlegend=True),
    row=1, col=2
)
fig.add_trace(
    go.Bar(name='Total Amount Per Month',x=df['Month'],y=df['Total Amount'], marker=dict(color="Green"), showlegend=True),
    row=2, col=1
)
fig.add_trace(
    go.Bar(name='Total Person Per Month',x=df['Month'],y=df['Toatl Person'], marker=dict(color="orange"), showlegend=True),
    row=2, col=2
)
fig.update_geos(
    projection_type="orthographic",
    landcolor="white",
    oceancolor="MidnightBlue",
    showocean=True,
    lakecolor="LightBlue"
)
fig.update_xaxes(tickangle=45)
fig.update_layout(
    template="plotly_dark",
    margin=dict(r=10, t=25, b=40, l=60),
    annotations=[
        dict(
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0)
    ]
)
fig.update_layout(height=500, width=700,title_text="Lyfas Rajorpay Dashboard")
# Step 4. Create a Dash layout
app.layout = html.Div([
                # adding a header and a paragraph
                html.Div([
                    html.H1("Acculi Labs Pvt. Ltd."),
                    html.P(" Rajaor Pay Dashboard Data Analytics"),
                    html.Hr()
                         ], 
                    style = {'padding' : '50px' , 
                             'backgroundColor' : 'lightblue',
                             'textAlign': 'center'}),
# adding a plot        
                dcc.Graph(id = 'plot', figure = fig),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=st.Date.min().date(),
                            max_date_allowed=st.Date.max().date(),
                            start_date=st.Date.min().date(),
                            end_date=st.Date.max().date(),
                        ),
                        dash_table.DataTable(
                           id='table',
                           columns=[{"name":i,"id":i} for i in df.columns],
                           data=df.to_dict('records'),
                           style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                           style_cell={
                               'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white',
                                 'textAlign': 'left'},
                           )
                     
                    ]
                ),
                      ])
                            
                

# Step 5. Add callback functions
@app.callback(Output('plot', 'figure'),
             [ Input("date-range", "start_date"),
        Input("date-range", "end_date"),])
def update_charts(start_date, end_date):
    mask = (
        (st.Date >= start_date)
        & (st.Date <= end_date)
    )
    filtered_data = st.loc[mask, :]
    fig = make_subplots(
    rows=2, cols=2,
    column_widths=[0.5, 0.5],
    row_heights=[0.5,0.5])
    fig.add_trace(
    go.Bar(name='Payment Per Day',x=filtered_data['Date'],y=filtered_data['Amount'], marker=dict(color="blue"), showlegend=True,text=filtered_data['Amount'],textposition='auto'),
    row=1, col=1
    )
    fig.add_trace(
    go.Bar(name='Person Per Day',x=filtered_data['Date'],y=filtered_data['Number Of Person'], marker=dict(color="crimson"), showlegend=True,text=filtered_data['Number Of Person'],textposition='auto'),
    row=1, col=2
    )
    fig.add_trace(
    go.Bar(name='Total Amount Per Month',x=df['Month'],y=df['Total Amount'], marker=dict(color="Green"), showlegend=True,text=df['Total Amount'],textposition='auto'),
    row=2, col=1)
    fig.add_trace(
    go.Bar(name='Total Person Per Month',x=df['Month'],y=df['Toatl Person'], marker=dict(color="orange"), showlegend=True,text=df['Toatl Person'],textposition='auto'),
    row=2, col=2)
    fig.update_geos(
    projection_type="orthographic",
    landcolor="white",
    oceancolor="MidnightBlue",
    showocean=True,
    lakecolor="LightBlue"
    )
    fig.update_xaxes(tickangle=45)
    fig.update_layout(
    template="plotly_dark",
    margin=dict(r=10, t=25, b=40, l=60),
    annotations=[
        dict(
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0)
    ]
    )
    fig.update_layout(title_text="Lyfas Rajorpay Dashboard")
    return fig
    # updating the plot
  
# Step 6. Add the server clause
if __name__ == "__main__":
        app.run_server(debug=False)
