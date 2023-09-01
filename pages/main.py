import dash
from dash import dcc, html
from PIL import Image

dash.register_page(__name__, name="🏡 Home 🏰", title="CUFC", path="/")

IMG_CUFC = Image.open(f"./images/CUFC.png")

layout = html.Div([
    html.Div("CUFC", style={"font-size":40, "textAlign":"center"}),
    html.Hr(),
    html.Center(html.Img(src=IMG_CUFC, width="313px"),),
])
