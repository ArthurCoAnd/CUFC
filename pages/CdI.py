import dash
from dash import dcc, html
from PIL import Image

dash.register_page(__name__, name="🍺 Choppeira 🍻", title="CUFC - Choppeira")

IMG_Choppeira = Image.open(f"./images/ChoppeiraKaiser.png")

layout = html.Div([
    html.Div("Choppeira", style={"font-size":40, "textAlign":"center"}),
    html.Hr(),
    html.Center(html.Img(src=IMG_Choppeira, height="500px"),),
])
