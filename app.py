# Bibliotecas
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import os
import pandas as pd
from PIL import Image
import json

app_dir = os.path.dirname(__file__)
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.UNITED], suppress_callback_exceptions=True)
app.title = "CUFC"
app._favicon = (f"CUFC.ico")

IMG_CUFC = Image.open(f"images/CUFC.png")

with open("data/VdV.json", "r") as arq:
    VdV_data = json.load(arq)

menu = dbc.Nav([
	dbc.NavLink([
		html.Div(p["name"], style={"font-size":20, "textAlign":"center"})
	], href=p["path"], active="exact") for p in dash.page_registry.values()
], pills=True)

app.layout = dbc.Container([
	dcc.Store(id="VdV-data", data=VdV_data),
	dbc.Row([
		dbc.Col([
			html.Center(html.Img(src=IMG_CUFC, height="71px")),
		], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
		dbc.Col([
			html.Div("Calculadora Universal de Fontes Chaveadas", style={"font-size":50, "textAlign":"center"})
		], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10),
	], style={"padding-top":"10px"}),
	html.Hr(),
	dbc.Row([
		menu
	]),
    html.Hr(),
	dbc.Row([
		dash.page_container
	]),
], fluid=True)

if __name__ == "__main__":
	os.system("cls" if os.name == "nt" else "clear")
	print('--------------------------------------------')
	print(' .d8888b.  888     888 8888888888 .d8888b.  ')
	print('d88P  Y88b 888     888 888       d88P  Y88b ')
	print('888    888 888     888 888       888    888 ')
	print('888        888     888 8888888   888        ')
	print('888        888     888 888       888        ')
	print('888    888 888     888 888       888    888 ')
	print('Y88b  d88P Y88b. .d88P 888       Y88b  d88P ')
	print(' "Y8888P"   "Y88888P"  888        "Y8888P"  ')
	print('--------------------------------------------')
	print('  Calculadora Universal de Fontes Chaveadas ')
	print('--------------------------------------------')
	app.run(debug=True)