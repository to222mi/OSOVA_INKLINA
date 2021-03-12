import base64
import io
import os
import dash
import dash_auth
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from pathlib import Path
import pandas as pd
import json
import numpy as np
import requests
import plotly
import plotly.graph_objs as go
import chart_studio
chart_studio.tools.set_credentials_file(username='to222mi', api_key='w2LIHZZq34BgaBYRCxbp')
import plotly.graph_objs as go
from plotly import tools as tls

import matplotlib.pyplot as plt
import codecs, json

## set the referral links to the css stylesheets used for this program
external_css = [
	"https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
	"https://cdn.rawgit.com/plotly/dash-app-stylesheets/737dc4ab11f7a1a8d6b5645d26f69133d97062ae/dash-wind-streaming.css",
	"https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
	"https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
	"https://fonts.googleapis.com/css?family=Roboto:300,400,500",
	"https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700",
    "https://codepen.io/chriddyp/pen/bWLwgP.css"
    ]

external_stylesheets=external_css

VALID_USERNAME_PASSWORD_PAIRS = [['inklina', 'ttOsOvA2020']]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

server = app.server

app.layout = html.Div([
	html.Div([
        html.H2("TT OSOVÁ - GEOTECHNICKÝ MONITORING"),
        html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png"),
		html.Img(src="https://www.vimvic.cz/upload/images/companies-company-logo/12214.png", 
			style={'width':'115','height':'75','verticalAlign':'center'}),
		], className='banner'),
    html.Br(),
    html.H4("INKLINOMETRIE"),
	html.Br(),
    html.H6("VYBER VRT"),
	dcc.Dropdown(
        id='dropdown_vrty',
        options=[
            {'label': 'INKLINOVRT 2A', 'value': '2A'},
            {'label': 'INKLINOVRT 2B', 'value': '2B'},
            {'label': 'INKLINOVRT 4A', 'value': '4A'},
            {'label': 'INKLINOVRT 4B', 'value': '4B'},
            {'label': 'INKLINOVRT 5A', 'value': '5A'},
            {'label': 'INKLINOVRT 5B', 'value': '5B'},
            {'label': 'INKLINOVRT 7A', 'value': '7A'},
            {'label': 'INKLINOVRT 7B', 'value': '7B'},
            {'label': 'INKLINOVRT 9A', 'value': '9A'},
            {'label': 'INKLINOVRT 9B', 'value': '9B'},
            {'label': 'INKLINOVRT 11A', 'value': '11A'},
            {'label': 'INKLINOVRT 11B', 'value': '11B'},
            {'label': 'INKLINOVRT 13A', 'value': '13A'},
            {'label': 'INKLINOVRT 22', 'value': '22'},
            {'label': 'INKLINOVRT 23', 'value': '23'},
        ],
        value='2A'),
    html.Div([
        html.Div([html.H4("POZICE INKLINOVRTU"),
            dcc.Graph(id='map')], style={'display': 'inline-block', 'width': '33%'}),
        html.Div([html.H4("3D - KUMULATIVNÍ ZOBRAZENÍ"),
            dcc.Graph(id='graph4')],style={'display': 'inline-block', 'width': '66%'})]),
	html.Div(id='intermediate_value', style={'display': 'none'}),
    html.Div(id='intermediate_value1', style={'display': 'none'})
	])
    
@app.callback(
	Output('intermediate_value', 'children'),
	[Input('dropdown_vrty', 'value')])	
def save_popisy(vrt):
    popisy = pd.read_csv("DATA_ALL\DATA_OK\POPISY\POPISY1.csv", dtype=np.str, delimiter=',')
    popisy = popisy.values.tolist()
    return json.dumps(popisy)
    
@app.callback(
	Output('map', 'figure'),
    [Input('intermediate_value', 'children'),
    Input('dropdown_vrty','value')])	
def update_map(intermediate_value, vrt):
    popisy = pd.read_json(intermediate_value)
    new_header = popisy.iloc[0]
    popisy = popisy[1:]
    popisy.columns = new_header
    ink = popisy[vrt]
    ink = ink.tolist()
    name = np.str(ink[0])
    long = np.float(ink[1])
    lat = np.float(ink[2])
    
    tunel = np.loadtxt("DATA_OK\POPISY\TUNEL.csv", dtype=np.float, delimiter=',')
    tunlong = tunel[:,0]
    tunlat = tunel[:,1]
    tunel1 = np.loadtxt("DATA_OK\POPISY\TUNEL1.txt", dtype=np.float, delimiter=',')
    tunlong1 = tunel1[:,0]
    tunlat1 = tunel1[:,1]
    coord = np.loadtxt("DATA_OK\POPISY\COORD.txt", dtype=np.float, delimiter=',')
    coordlong = coord[:,0]
    coordlat = coord[:,1]
    
    mapbox_access_token = 'pk.eyJ1IjoibWFyaGFuc2t5IiwiYSI6ImNqdWNvdDhsczBsdWY0NGx0ODVndjk3d2wifQ.x7EC5ZvG8pk8J5vPbh03Xw'    
    
    coordata = go.Scattermapbox(
			lat=coordlat,
			lon=coordlong,
			mode='markers',
			marker=go.scattermapbox.Marker(
				size=5,
				color='red',
                opacity=0.7))
            
    data = go.Scattermapbox(
			name = name,
			lat=[lat],
			lon=[long],
			mode='markers + text',
			marker=go.scattermapbox.Marker(
				size=18,
				color='red'),
			text=name,
            textfont_size=14,
            textfont_color = 'black',
            textposition="top center")
        
    data_t = go.Scattermapbox(
        name = "tunel",
        lat=tunlat,
        lon=tunlong,
        mode='lines',
        hoverinfo='skip',
        line = dict(width = 2, color = 'blue'))
        
    data_tt = go.Scattermapbox(
        name = "tunel",
        lat=tunlat1,
        lon=tunlong1,
        mode='lines',
        hoverinfo='skip',
        line = dict(width = 2, color = 'blue'))
    
    layout = go.Layout(
		showlegend=False,
		autosize=False,
		height=1000,
		hovermode='closest',
		mapbox=go.layout.Mapbox(
			style = "satellite-streets",
			accesstoken=mapbox_access_token,
            center=go.layout.mapbox.Center(
				lat=lat,
				lon=long),
			bearing=0,
			pitch=0,
			zoom=16))
    
    fig = go.Figure(data=[coordata, data, data_t, data_tt], layout=layout)
    return fig
    
@app.callback(Output('graph4', 'figure'),
              Input('dropdown_vrty', 'value'),
              Input('intermediate_value', 'children'))
def update_graph(vrt, intermediate_value):
    popisy = pd.read_json(intermediate_value)
    new_header = popisy.iloc[0]
    popisy = popisy[1:]
    popisy.columns = new_header
    ink = popisy[vrt]
    ink = ink.tolist()
    azimuth = np.int(ink[3])    
    posun = np.int(ink[4])
    posun1 = np.float(posun/2)
    
    list_of_files = os.listdir("DATA_OK\INK_{}".format(vrt))
    list_of_files = sorted(list_of_files,key=lambda x: int(os.path.splitext(x)[1].strip(".")))
    DATA = list()
    datess = list()

    for file in list_of_files:
        print(file)
        data = np.loadtxt("DATA_OK\INK_{}\{}".format(vrt, file), dtype=np.int, delimiter=' ', skiprows = 16)
        dates = np.loadtxt("DATA_OK\INK_{}\{}".format(vrt, file), dtype=np.str, delimiter=',')
        DATA.append(data)
        datess.append(dates[2])
    
    
    traces_A1 = list()
    traces_A2 = list()
    traces_total = list()

    traces_A1_kum = list()
    traces_A2_kum = list()
    traces_total_kum = list()

    traces_3D = list()
    traces_3D_mesh = list()

    A1A3B2B4_kum_ref_total = []
    A2A4B1B3_kum_ref_total = []
    D_total = []

    D = DATA[0][posun:,0]/2 - posun1
    
    if 0<azimuth and azimuth<45:
        alfa = azimuth
        beta = 90 - alfa
        a = np.sin(np.radians(alfa))*5
        b = np.sin(np.radians(beta))*5
        A = b
        B = a*-1
    elif azimuth == 45:
        alfa = 45
        a = np.sin(np.radians(alfa))*5
        A = a
        B = a*-1
    elif 45<azimuth and azimuth<90:
        alfa = 90 - azimuth
        beta = azimuth
        a = np.sin(np.radians(alfa))*5
        b = np.sin(np.radians(beta))*5
        A = a
        B = b*-1
    elif azimuth == 90:
        A = 0
        B = -5
    elif 90<azimuth and azimuth<135:
        alfa = azimuth - 90
        beta = 90 - alfa
        a = np.sin(np.radians(alfa))*5
        b = np.sin(np.radians(beta))*5
        A = a*-1
        B = b*-1
    elif azimuth == 135:
        alfa = 45
        a = np.sin(np.radians(alfa))*5
        A = a*-1
        B = a*-1
    elif 135<azimuth and azimuth<180:
        alfa = 180 - azimuth
        beta = 90 - alfa
        a = np.sin(np.radians(alfa))*5
        b = np.sin(np.radians(beta))*5
        A = b*-1
        B = a*-1
    elif azimuth == 180:
        A = -5
        B = 0
    elif 180<azimuth and azimuth<225:
        alfa = azimuth -180
        beta = 90 - alfa
        a = np.sin(np.radians(alfa))*5
        b = np.sin(np.radians(beta))*5
        A = b*-1
        B = a
    elif azimuth == 225:
        alfa = 45
        a = np.sin(np.radians(alfa))*5
        A = a*-1
        B = a
    elif 225<azimuth and azimuth<270:
        alfa = 270 - azimuth
        beta = 90 - alfa
        a = np.sin(np.radians(alfa))*5
        b = np.sin(np.radians(beta))*5
        A = a*-1
        B = b
    elif azimuth == 270:
        A = 0
        B = 5
    elif 270<azimuth and azimuth<315:
        alfa = azimuth -270
        beta = 90 - alfa
        a = np.sin(np.radians(alfa))*5
        b = np.sin(np.radians(beta))*5
        A = a
        B = b
    elif azimuth == 315:
        alfa = 45
        a = np.sin(np.radians(alfa))*5
        A = a
        B = a
    elif 315<azimuth and azimuth<360:
        alfa = 360 - azimuth
        beta = 90 - alfa
        a = np.sin(np.radians(alfa))*5
        b = np.sin(np.radians(beta))*5
        A = b
        B = a
    elif azimuth == 0 or azimuth == 360:
        A = 5
        B = 0
    
    trace_north_3D = trace_north_3D = go.Cone(
        x=[0],
        y=[0],
        z=[0],
        u=[A],
        v=[B],
        w=[0],
        showscale=False,
        name =  "North", 
        text = "North",
        opacity = 0.5)
    
    trace_north_3D_t = go.Scatter3d(
        x=[A/2],
        y=[B/2],
        z=[0],
        name =  "North", 
        text = "SEVER",
        mode='text',
        showlegend = False)
        
    import matplotlib.pyplot as plt
    cmap = plt.cm.get_cmap('viridis_r')        


    for i in range(len(DATA)):
        
        rgba = cmap(i/len(DATA))
        rgba = tuple(int((255*x)) for x in rgba[0:3])
        rgba = 'rgb'+str(rgba)
        
        if vrt == "7B" and i>15:
            posun = 10
        elif vrt == "9B" and i>16:
            posun = 13
        
        if DATA[i][0,5] == -32768:
            A1 = DATA[i][posun:,1]
            A3 = DATA[i][posun:,2]
            B1 = DATA[i][posun:,3]
            B3 = DATA[i][posun:,4]
            
            A1_0 = DATA[0][posun:,1]
            A3_0 = DATA[0][posun:,2]
            B1_0 = DATA[0][posun:,3]
            B3_0 = DATA[0][posun:,4]
            
            A1A3B2B4 = ((A1-A3)/2)/20000*500
            A2A4B1B3 = ((B1-B3)/2)/20000*500             
            total = (A1A3B2B4**2+A2A4B1B3**2)**0.5
                            
            A1A3B2B4_kum = [sum(A1A3B2B4[i:-1]) for i in range(0,len(A1))]
            A2A4B1B3_kum = [sum(A2A4B1B3[i:-1]) for i in range(0,len(A1))]
            total_kum = [sum(total[i:-1]) for i in range(0,len(A1))]
                   
            A1A3B2B4_ref = ((A1_0-A3_0)/2)/20000*500
            A2A4B1B3_ref = ((B1_0-B3_0)/2)/20000*500             
            total_ref = ((A1A3B2B4-A1A3B2B4_ref)**2+(A2A4B1B3-A2A4B1B3_ref)**2)**0.5     
            
            A1A3B2B4_kum_ref = np.array([sum(A1A3B2B4[i:-1]) for i in range(0,len(A1))]) - np.array([sum(A1A3B2B4_ref[i:-1]) for i in range(0,len(A1))])
            A2A4B1B3_kum_ref = np.array([sum(A2A4B1B3[i:-1]) for i in range(0,len(A1))]) - np.array([sum(A2A4B1B3_ref[i:-1]) for i in range(0,len(A1))])
            total_kum_ref = (A1A3B2B4_kum_ref**2 + A2A4B1B3_kum_ref**2)**0.5
        else:
            
            
            A1 = DATA[i][posun:,1]
            A3 = DATA[i][posun:,2]
            A2 = DATA[i][posun:,3]
            A4 = DATA[i][posun:,4]
            B1 = DATA[i][posun:,5]
            B3 = DATA[i][posun:,6]
            B2 = DATA[i][posun:,7]
            B4 = DATA[i][posun:,8]
            
            A1_0 = DATA[0][posun:,1]
            A3_0 = DATA[0][posun:,2]
            A2_0 = DATA[0][posun:,3]
            A4_0 = DATA[0][posun:,4]
            B1_0 = DATA[0][posun:,5]
            B3_0 = DATA[0][posun:,6]
            B2_0 = DATA[0][posun:,7]
            B4_0 = DATA[0][posun:,8]

            A1A3B2B4 = ((A1-A3-B2+B4)/4)/20000*500
            A2A4B1B3 = ((A2-A4-B3+B1)/4)/20000*500
            total = (A1A3B2B4**2+A2A4B1B3**2)**0.5
                      
            A1A3B2B4_kum = [sum(A1A3B2B4[i:-1]) for i in range(0,len(A1))]
            A2A4B1B3_kum = [sum(A2A4B1B3[i:-1]) for i in range(0,len(A1))]
            total_kum = [sum(total[i:-1]) for i in range(0,len(A1))]
            
            A1A3B2B4_ref = ((A1_0-A3_0-B2_0+B4_0)/4)/20000*500
            A2A4B1B3_ref = ((A2_0-A4_0-B3_0+B1_0)/4)/20000*500
            total_ref = ((A1A3B2B4-A1A3B2B4_ref)**2+(A2A4B1B3-A2A4B1B3_ref)**2)**0.5
            
            A1A3B2B4_kum_ref = np.array([sum(A1A3B2B4[i:-1]) for i in range(0,len(A1))]) - np.array([sum(A1A3B2B4_ref[i:-1]) for i in range(0,len(A1))])
            A2A4B1B3_kum_ref = np.array([sum(A2A4B1B3[i:-1]) for i in range(0,len(A1))]) - np.array([sum(A2A4B1B3_ref[i:-1]) for i in range(0,len(A1))])
            total_kum_ref = (A1A3B2B4_kum_ref**2 + A2A4B1B3_kum_ref**2)**0.5
            

        D = DATA[i][posun:,0]/2 -posun1


        
        trace_3D = go.Scatter3d(
            x=list(A1A3B2B4_kum_ref),
            y=list(A2A4B1B3_kum_ref),
            z=list(-D),
            name =  datess[i], 
            #hovertext= list(cas),
            mode='lines + markers',
            marker=dict(
                color=rgba,
                size=3,),
        )
        traces_3D.append(trace_3D)
           
     
        
        layout1 = go.Layout(
            scene = dict(aspectmode = 'data'),
            #title='kumulatívny graf',
            #width = 1000,
            height=1000,
            xaxis=dict(
                title='Baxis'),
            yaxis=dict(
                title='Aaxis',
                autorange = 'reversed'),
            )
        
        
    traces_3D.append(trace_north_3D)
    traces_3D.append(trace_north_3D_t)
    
    fig = go.Figure(data=traces_3D, layout=layout1)
    fig.update_scenes(yaxis_autorange="reversed")
    fig.update_layout(scene = dict(
                        xaxis_title='A AXIS',
                        yaxis_title='B AXIS',
                        zaxis_title='DEPTH'),
                        )
                    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True,threaded=True)