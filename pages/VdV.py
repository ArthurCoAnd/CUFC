import dash
from dash import callback, dash_table, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from PIL import Image
import json
from math import sqrt, pi, ceil
import pandas as pd
import os

from modules.SD_VdV import SD_VdV
from modules.GG_VeI import GG_VeI

from tools.R2SI import R2SI

dash.register_page(__name__, name="🛫 Voar de Volta 🛬", title="CUFC - Voar de Volta")

CUFC_dir = os.path.dirname(__file__).replace("pages","")

IMG_CIRC_VdV = html.Img(src=Image.open("./images/circuitos/VdV.png"), width="100%")
IMG_CIRC_VdV_E1 = html.Img(src=Image.open("./images/circuitos/VdV_e1.png"), width="50%")
IMG_CIRC_VdV_E2 = html.Img(src=Image.open("./images/circuitos/VdV_e2.png"), width="50%")
IMG_CIRC_VdV_E3 = html.Img(src=Image.open("./images/circuitos/VdV_e3.png"), width="50%")

AeAw_DF = pd.read_csv(f"{CUFC_dir}/data/AeAw.csv", sep=";", decimal=",")
AWG_DF = pd.read_csv(f"{CUFC_dir}/data/AWG.csv", sep=";", decimal=",")
CAP_DF = pd.read_csv(f"{CUFC_dir}/data/Capacitores.csv", sep=";", decimal=".")

ENT = ["Vi","Vo","Po","rend","dVo_V","dVo_p","fs","Ts","D","Bmax","Jmax"]

# ██       █████  ██    ██  ██████  ██    ██ ████████ 
# ██      ██   ██  ██  ██  ██    ██ ██    ██    ██    
# ██      ███████   ████   ██    ██ ██    ██    ██    
# ██      ██   ██    ██    ██    ██ ██    ██    ██    
# ███████ ██   ██    ██     ██████   ██████     ██    

layout = html.Div([
	html.Div(html.Center(html.H1("Voar de Volta"))),
	
	# ███████ ███    ██ ████████ ██████   █████  ██████   █████  ███████ 
	# ██      ████   ██    ██    ██   ██ ██   ██ ██   ██ ██   ██ ██      
	# █████   ██ ██  ██    ██    ██████  ███████ ██   ██ ███████ ███████ 
	# ██      ██  ██ ██    ██    ██   ██ ██   ██ ██   ██ ██   ██      ██ 
	# ███████ ██   ████    ██    ██   ██ ██   ██ ██████  ██   ██ ███████ 

	html.Hr(),
	dbc.Container([
		dbc.Row([
			dbc.Col(children=[], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2, id="VdV-ent"),
			dbc.Col([
				html.Center(children=IMG_CIRC_VdV, id="VdV-circ"),
			], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10),
		]),
	]),
	
	#  ██████  █████  ██       ██████ ██    ██ ██       ██████  ███████ 
	# ██      ██   ██ ██      ██      ██    ██ ██      ██    ██ ██      
	# ██      ███████ ██      ██      ██    ██ ██      ██    ██ ███████ 
	# ██      ██   ██ ██      ██      ██    ██ ██      ██    ██      ██ 
	#  ██████ ██   ██ ███████  ██████  ██████  ███████  ██████  ███████ 

	html.Hr(),
	html.Div(html.Center(html.H1("Cálculos"))),
	html.Hr(),
	dbc.Container([
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-n-calc", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-DT", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-tx", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-Pi", mathjax=True, style={"font-size":30}))]),
		
		html.Hr(),
		dbc.Row([html.Center(html.H3("Indutores"))]),
		dbc.Row([html.Center(html.H5("Primário"))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-L1", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-iL1max", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-iL1rms", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(html.H5("Secundário"))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-L2", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-iL2max", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-iL2rms", mathjax=True, style={"font-size":30}))]),
		
		html.Hr(),
		dbc.Row([html.Center(html.H3("Capacitor de Saída"))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-Comin", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Div(dcc.Dropdown(id="VdV-DD-Co", options=CAP_DF["txt"], value=CAP_DF["txt"][CAP_DF.index[0]]))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-Co", mathjax=True, style={"font-size":30}))]),
		
		html.Hr(),
		dbc.Row([html.Center(html.H3("Núcleo"))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-AeAw", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(id="VdV-TAB-AeAw")]),
		dbc.Row([html.Div(dcc.Dropdown(id="VdV-DD-NUC", options=AeAw_DF["Núcleo"], value=AeAw_DF["Núcleo"][AeAw_DF.index[0]]))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-Ae", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-Aw", mathjax=True, style={"font-size":30}))]),
		
		html.Hr(),
		dbc.Row([html.Center(html.H3("Espiras"))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-N1", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-N2", mathjax=True, style={"font-size":30}))]),

		html.Hr(),
		dbc.Row([html.Center(html.H3("Condutores"))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-delta", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-Askin", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(id="VdV-TAB-AWG")]),
		dbc.Row([html.Center(html.H5("Fio Primário"))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-Af1", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Div(dcc.Dropdown(id="VdV-DD-AWG-f1", options=AWG_DF["AWG"], value=AWG_DF["AWG"][AeAw_DF.index[0]]))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-NCP-f1", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(html.H5("Fio Secundário"))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-Af2", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Div(dcc.Dropdown(id="VdV-DD-AWG-f2", options=AWG_DF["AWG"], value=AWG_DF["AWG"][AeAw_DF.index[0]]))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-NCP-f2", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(html.H5("Entreferro"))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-lg", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(html.H5("Fator de Execução"))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-Aw-min", mathjax=True, style={"font-size":30}))]),
		dbc.Row([html.Center(dcc.Markdown(id="VdV-C-FE", mathjax=True, style={"font-size":30}))]),
	]),
	
	#  ██████  ██████   █████  ███████ ██  ██████  ██████  
	# ██       ██   ██ ██   ██ ██      ██ ██      ██    ██ 
	# ██   ███ ██████  ███████ █████   ██ ██      ██    ██ 
	# ██    ██ ██   ██ ██   ██ ██      ██ ██      ██    ██ 
	#  ██████  ██   ██ ██   ██ ██      ██  ██████  ██████  
	
	html.Hr(),
	html.Div(html.Center(html.H1("Tensões e Correntes"))),
	html.Hr(),
	dbc.Container([
		dbc.Row([html.Center(html.H3("Enrolamento Primário"))]),
		dbc.Row([dcc.Graph(id="VdV-G-L1")]),
		dbc.Row([html.Center(html.H3("Enrolamento Secundário"))]),
		dbc.Row([dcc.Graph(id="VdV-G-L2")]),
		dbc.Row([html.Center(html.H3("Chave"))]),
		dbc.Row([dcc.Graph(id="VdV-G-S")]),
		dbc.Row([html.Center(html.H3("Diodo"))]),
		dbc.Row([dcc.Graph(id="VdV-G-D")]),
	]),
])

#  ██████  ██████  ███    ██ ███████ ██  ██████  ██    ██ ██████   █████  ██████  
# ██      ██    ██ ████   ██ ██      ██ ██       ██    ██ ██   ██ ██   ██ ██   ██ 
# ██      ██    ██ ██ ██  ██ █████   ██ ██   ███ ██    ██ ██████  ███████ ██████  
# ██      ██    ██ ██  ██ ██ ██      ██ ██    ██ ██    ██ ██   ██ ██   ██ ██   ██ 
#  ██████  ██████  ██   ████ ██      ██  ██████   ██████  ██   ██ ██   ██ ██   ██ 

@callback([
		Output("VdV-ent", "children"),
		Output("VdV-C-n-calc", "children"), Output("VdV-C-DT", "children"), Output("VdV-C-tx", "children"), Output("VdV-C-Pi", "children"),
		Output("VdV-C-L1", "children"), Output("VdV-C-iL1max", "children"), Output("VdV-C-iL1rms", "children"),
		Output("VdV-C-L2", "children"), Output("VdV-C-iL2max", "children"), Output("VdV-C-iL2rms", "children"),
		Output("VdV-C-Comin", "children"), Output("VdV-DD-Co", "options"), Output("VdV-DD-Co", "value"),
		Output("VdV-C-AeAw", "children"), Output("VdV-TAB-AeAw", "children"), Output("VdV-DD-NUC", "options"), Output("VdV-DD-NUC", "value"),
		Output("VdV-C-delta", "children"), Output("VdV-C-Askin", "children"), Output("VdV-TAB-AWG", "children"),
		Output("VdV-C-Af1", "children"), Output("VdV-DD-AWG-f1", "options"), Output("VdV-DD-AWG-f1", "value"),
		Output("VdV-C-Af2", "children"), Output("VdV-DD-AWG-f2", "options"), Output("VdV-DD-AWG-f2", "value"),
		Output("VdV-G-L1", "figure"), Output("VdV-G-L2", "figure"), Output("VdV-G-S", "figure"), Output("VdV-G-D", "figure")
		], Input("VdV-data", "data"))
def configurar_elementos(VdV):
	ENTRADAS = html.Div([
		dbc.Row([
			dbc.Col([html.Div("Vi")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id="VdV-I-Vi", value=VdV["Vi"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div("V")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div("Vo")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id="VdV-I-Vo", value=VdV["Vo"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div("V")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div("Po")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id="VdV-I-Po", value=VdV["Po"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div("W")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Center(dcc.Markdown("$$\\eta$$", mathjax=True))], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id="VdV-I-rend", value=VdV["rend"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div("%")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),

		html.Hr(),
		dbc.Row([
			html.Center(dbc.RadioItems(["V","%"], VdV["RI_dVo"], inline=True, id="VdV-RI-dVo"))
		]),
		dbc.Row([
			dbc.Col([html.Div("ΔVo")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id="VdV-I-dVo_V", value=VdV["dVo_V"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div("V")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div("ΔVo")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id="VdV-I-dVo_p", value=VdV["dVo_p"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div("%")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),

		html.Hr(),
		dbc.Row([
			html.Center(dbc.RadioItems(["fs","Ts"], VdV["RI_fsTs"], inline=True, id="VdV-RI-fsTs"))
		]),
		dbc.Row([
			dbc.Col([html.Div("fs")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id="VdV-I-fs", value=VdV["fs"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div("Hz")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div("Ts")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id="VdV-I-Ts", value=VdV["Ts"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div("s")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div("D")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id="VdV-I-D", value=VdV["D"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
		]),

		html.Hr(),
		dbc.Row([
			dbc.Col([html.Div("Bmax")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id="VdV-I-Bmax", value=VdV["Bmax"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div("T")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div("Jmax")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id="VdV-I-Jmax", value=VdV["Jmax"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div("A/cm²")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
	])

	C_n = f"$$n = \\frac{{N_2}}{{N_1}} \\leq \\frac{{V_o \\cdot \\left( 1 - D \\right)}}{{V_i \\cdot D}}$$ = {VdV['N2N1_calc']:.5f} $$\\Rightarrow n$$ = {VdV['N2N1']}"
	C_DT = f"$$DT = D \\cdot T_s$$ = {R2SI(VdV['DT'])}s"
	C_tx = f"$$t_x = DT \\cdot \\left( \\frac{{V_i \\cdot n}}{{V_o}} + 1 \\right)$$ = {R2SI(VdV['tx'])}s"
	C_Pi = f"$$P_i = \\frac{{P_o}}{{\\eta}}$$ = {R2SI(VdV['Pi'])}W"

	C_L1 = f"$$L_1 = \\frac{{V_i^2 \\cdot D^2}}{{2 \\cdot P_i \\cdot f_s}}$$ = {R2SI(VdV['L1'])}H"
	C_iL1max = f"$$i_{{L_{{1_{{max}}}}}} = i_{{S_{{max}}}} = \\frac{{V_i \\cdot DT}}{{L_1}}$$ = {R2SI(VdV['iL1max'])}A"
	C_iL1rms = f"$$i_{{L_{{1_{{rms}}}}}} = i_{{L_{{1_{{max}}}}}} \\cdot \\sqrt{{ \\frac{{D}}{{3}} }}$$ = {R2SI(VdV['iL1rms'])}A"
	
	C_L2 = f"$$L_2 = n^2 \\cdot L_1$$ = {R2SI(VdV['L2'])}H"
	C_iL2max = f"$$i_{{L_{{2_{{max}}}}}} = i_{{D_{{max}}}} = \\frac{{V_i \\cdot DT}}{{L_1 \\cdot n}}$$ = {R2SI(VdV['iL2max'])}A"
	C_iL2rms = f"$$i_{{L_{{2_{{rms}}}}}} = i_{{L_{{2_{{max}}}}}} \\cdot \\sqrt{{ \\frac{{tx-DT}}{{3 \\cdot T_s}} }}$$ = {R2SI(VdV['iL2rms'])}A"

	C_Comin = f"$$C_{{o_{{min}}}} = \\frac{{I_o \\cdot DT}}{{\\Delta V_o}}$$ = {R2SI(VdV['Comin'])}F"
	Co_DF = CAP_DF.loc[CAP_DF["F"] >= VdV["Comin"]]
	Co_opt = Co_DF["txt"]
	Co_val = Co_DF["txt"][Co_DF.index[0]]
	
	# AeAw
	C_AeAw = f"$$A_e A_w = \\frac{{L_1 \\cdot i_{{L_{{1_{{max}}}}}} \\cdot i_{{L_{{1_{{rms}}}}}}}}{{B_{{max}} \\cdot J_{{max}} \\cdot K}}$$ = {R2SI(VdV['AeAw']*10e8)}$$cm^4$$"
	TAB_AeAw = dash_table.DataTable(
		data = AeAw_DF.to_dict("records"),
		columns = [{"name": i, "id": i} for i in AeAw_DF.columns],
		style_cell = {"textAlign": "center"},
		cell_selectable = False,
		style_data_conditional=[
			{"if": {
				"filter_query": f"{{AeAw}} > {VdV['AeAw']*1e9}",
				"column_id": "AeAw"
			},
			"backgroundColor": "green",
			"color": "white"},
			{"if": {
				"filter_query": f"{{AeAw}} <= {VdV['AeAw']*1e9}",
				"column_id": "AeAw"
			},
			"backgroundColor": "red",
			"color": "white"},
		]
	)
	NUC_DF = AeAw_DF.loc[AeAw_DF["AeAw"] >= VdV["AeAw"]*1e9]
	if len(NUC_DF) > 0:
		NUC_opt = NUC_DF["Núcleo"]
		NUC_val = NUC_DF["Núcleo"][NUC_DF.index[0]]
	else:
		NUC_opt = ["E-55"]
		NUC_val = "E-55"

	# Efeito Skin
	C_delta = f"$$\\delta = \\frac{{7,5}}{{\\sqrt{{f_s}}}}$$ = {R2SI(VdV['delta'])}cm"
	C_Askin = f"$$A_{{skin}} = \\pi \\cdot \\delta^2$$ = {R2SI(VdV['Askin'])}cm²"
	TAB_AWG = dash_table.DataTable(
		data = AWG_DF.to_dict("records"),
		columns = [{"name":i, "id":i} for i in AWG_DF.columns],
		style_cell = {"textAlign": "center"},
		cell_selectable = False,
		style_data_conditional=[
			{"if": {
				"filter_query": f"{{ACu}} < {VdV['Askin']}",
				"column_id": "ACu"
			},
			"backgroundColor": "green",
			"color": "white"},
			{"if": {
				"filter_query": f"{{ACu}} >= {VdV['Askin']}",
				"column_id": "ACu"
			},
			"backgroundColor": "red",
			"color": "white"},
		]
	)
	TAB_Askin = AWG_DF.loc[AWG_DF["ACu"] < VdV["Askin"]]
	AWG_min = TAB_Askin["AWG"][TAB_Askin.index[0]]

	C_Af1 = f"$$A_{{fio_1}} = \\frac{{i_{{L_{{1_{{rms}}}}}}}}{{J_{{max}}}}$$ = {R2SI(VdV['Af1'])}cm²"
	TAB_f1 = AWG_DF.loc[AWG_DF["ACu"] < VdV["Af1"]]
	TAB_f1 = TAB_f1.loc[TAB_f1["AWG"] >= AWG_min]
	AWG_f1_val = TAB_f1["AWG"].tolist()
	AWG_f1_opt = AWG_f1_val[0]

	C_Af2 = f"$$A_{{fio_2}} = \\frac{{i_{{L_{{2_{{rms}}}}}}}}{{J_{{max}}}}$$ = {R2SI(VdV['Af2'])}cm²"
	TAB_f2 = AWG_DF.loc[AWG_DF["ACu"] < VdV["Af2"]]
	TAB_f2 = TAB_f2.loc[TAB_f2["AWG"] >= AWG_min]
	AWG_f2_val = TAB_f2["AWG"].tolist()
	AWG_f2_opt = AWG_f2_val[0]
	
	fig = GG_VeI(VdV)

	return ENTRADAS, C_n, C_DT, C_tx, C_Pi, C_L1, C_iL1max, C_iL1rms, C_L2, C_iL2max, C_iL2rms, C_Comin, Co_opt, Co_val, C_AeAw, TAB_AeAw, NUC_opt, NUC_val, C_delta, C_Askin, TAB_AWG, C_Af1, AWG_f1_val, AWG_f1_opt, C_Af2, AWG_f2_val, AWG_f2_opt, fig[0], fig[1], fig[2], fig[3]

#  █████  ██      ████████ ███████ ██████   █████  ██████  
# ██   ██ ██         ██    ██      ██   ██ ██   ██ ██   ██ 
# ███████ ██         ██    █████   ██████  ███████ ██████  
# ██   ██ ██         ██    ██      ██   ██ ██   ██ ██   ██ 
# ██   ██ ███████    ██    ███████ ██   ██ ██   ██ ██   ██ 

@callback([Output("VdV-I-fs", "disabled"), Output("VdV-I-Ts", "disabled")], Input("VdV-RI-fsTs", "value"))
def aleração_RI_FreqPer(RI):
	if RI == "fs": return False, True
	else: return True, False

@callback([Output("VdV-I-dVo_V", "disabled"), Output("VdV-I-dVo_p", "disabled")], Input("VdV-RI-dVo", "value"))
def aleração_RI_dVo(RI):
	if RI == "V": return False, True
	else: return True, False

#  ██████  █████  ██       ██████ ██    ██ ██       █████  ██████  
# ██      ██   ██ ██      ██      ██    ██ ██      ██   ██ ██   ██ 
# ██      ███████ ██      ██      ██    ██ ██      ███████ ██████  
# ██      ██   ██ ██      ██      ██    ██ ██      ██   ██ ██   ██ 
#  ██████ ██   ██ ███████  ██████  ██████  ███████ ██   ██ ██   ██ 

@callback([
		Output("VdV-data", "data"),
		Output("VdV-I-fs", "value"), Output("VdV-I-Ts", "value"),
		Output("VdV-I-dVo_V", "value"), Output("VdV-I-dVo_p", "value"),
	], [[Input(f"VdV-I-{i}", "value") for i in ENT]], [State("VdV-data", "data"), State("VdV-RI-fsTs", "value"), State("VdV-RI-dVo", "value")])
def alteração_das_entradas(*args):
	VdV = {}

	for i, e in enumerate(ENT):
		VdV[e] = args[0][i]
	VdV_antigo = args[1]
	for e in ENT:
		if VdV[e] != VdV_antigo[e]:
			print(f"> {e}: {VdV_antigo[e]} -> {VdV[e]}")

	RI_fsTs = args[2]
	if RI_fsTs == "fs":
		VdV["RI_fsTs"] = "fs"
		VdV["RI_fs"] = False; VdV["RI_Ts"] = True
		VdV["Ts"] = 1/VdV["fs"]
	else:
		VdV["RI_fsTs"] = "Ts"
		VdV["RI_fs"] = True; VdV["RI_Ts"] = False
		VdV["fs"] = 1/VdV["Ts"]

	RI_dVo = args[3]
	if RI_dVo == "V":
		VdV["RI_dVo"] = "V"
		VdV["RI_dVo_V"] = False; VdV["RI_dVo_p"] = True
		VdV["dVo_p"] = 100*VdV["dVo_V"]/VdV["Vo"]
	else:
		VdV["RI_dVo"] = "%"
		VdV["RI_dVo_V"] = True; VdV["RI_dVo_p"] = False
		VdV["dVo_V"] = VdV["dVo_p"]*VdV["Vo"]/100
	
	VdV["DT"] = VdV["D"]*VdV["Ts"]

	VdV["N2N1_calc"] = VdV["Vo"]*(1-VdV["D"])/(VdV["Vi"]*VdV["D"])
	VdV["N2N1"] = int(VdV["N2N1_calc"]*10)/10

	VdV["N1N2"] = 1/VdV["N2N1"]

	VdV["tx"] = VdV["DT"]*((VdV["N2N1"]*VdV["Vi"]/VdV["Vo"]) + 1)

	VdV["Pi"] = 100*VdV["Po"]/VdV["rend"]

	VdV["Ii"] = VdV["Pi"]/VdV["Vi"]

	VdV["Io"] = VdV["Po"]/VdV["Vo"]

	VdV["L1"] = VdV["Vi"]*VdV["Vi"]*VdV["D"]*VdV["D"]/(2*VdV["Pi"]*VdV["fs"])

	VdV["L2"] = VdV["L1"]*VdV["N2N1"]*VdV["N2N1"]

	VdV["Comin"] = VdV["Io"]*VdV["DT"]/VdV["dVo_V"]
	
	VdV["VL1min"] = -VdV["Vo"]*VdV["N1N2"]
	VdV["iL1max"] = VdV["Vi"]*VdV["DT"]/VdV["L1"]
	VdV["iL1rms"] = VdV["iL1max"]*sqrt(VdV["D"]/3)

	VdV["VL2max"] = VdV["Vi"]*VdV["N2N1"]
	VdV["iL2max"] = VdV["iL1max"]*VdV["N1N2"]
	VdV["iL2rms"] = VdV["iL2max"]*sqrt((VdV["tx"]-VdV["DT"])/(3*VdV["Ts"]))
	
	VdV["VSmax"] = VdV["Vi"] + VdV["Vo"]*VdV["N1N2"]
	VdV["iSmax"] = VdV["iL1max"]
	
	VdV["VDmax"] = VdV["Vo"] + VdV["Vi"]*VdV["N2N1"]
	VdV["iDmax"] = VdV["iL2max"]

	VdV["K"] = 0.25
	VdV["AeAw"] = VdV["L1"]*VdV["iL1max"]*VdV["iL1rms"]/(VdV["Bmax"]*VdV["Jmax"]*1e5*VdV["K"])

	VdV["delta"] = 7.5/sqrt(VdV["fs"])
	VdV["Askin"] = pi*VdV["delta"]*VdV["delta"]

	VdV["Af1"] = VdV["iL1rms"]/VdV["Jmax"]
	VdV["Af2"] = VdV["iL2rms"]/VdV["Jmax"]

	VdV = dict(sorted(VdV.items(), key=lambda i: i[0].lower()))
	# print(json.dumps(VdV, indent=2))
	with open("./data/VdV.json", "w") as arq:
		json.dump(VdV, arq, indent=2)

	return VdV, VdV["fs"], VdV["Ts"], VdV["dVo_V"], VdV["dVo_p"]

# ██████  ██████   ██████  ██████  ██████   ██████  ██     ██ ███    ██ 
# ██   ██ ██   ██ ██    ██ ██   ██ ██   ██ ██    ██ ██     ██ ████   ██ 
# ██   ██ ██████  ██    ██ ██████  ██   ██ ██    ██ ██  █  ██ ██ ██  ██ 
# ██   ██ ██   ██ ██    ██ ██      ██   ██ ██    ██ ██ ███ ██ ██  ██ ██ 
# ██████  ██   ██  ██████  ██      ██████   ██████   ███ ███  ██   ████ 

@callback([
	Output("VdV-C-Co", "children"), Output("VdV-C-Ae", "children"), Output("VdV-C-Aw", "children"),
	Output("VdV-C-N1", "children"), Output("VdV-C-N2", "children"),
	Output("VdV-C-NCP-f1", "children"), Output("VdV-C-NCP-f2", "children"),
	Output("VdV-C-lg", "children"),
	Output("VdV-C-Aw-min", "children"), Output("VdV-C-FE", "children"),
	Output("VdV-circ", "children"),
	], [
		Input("VdV-DD-Co", "value"), Input("VdV-DD-NUC", "value"),
		Input("VdV-DD-AWG-f1", "value"), Input("VdV-DD-AWG-f2", "value"),
	], State("VdV-data", "data"))
def alteração_das_DD(Co, NUC, AWG_f1, AWG_f2, VdV):
	Co_DF = CAP_DF.loc[CAP_DF["txt"] == Co]
	Co = Co_DF["F"][Co_DF.index[0]]
	C_Co = f"$$C_o$$ = {R2SI(Co)}F"

	NUC_DF = AeAw_DF.loc[AeAw_DF["Núcleo"] == NUC]
	Ae = NUC_DF["Ae"][NUC_DF.index[0]]
	C_Ae = f"$$A_e$$ = {Ae}$$cm^4$$"
	Aw = NUC_DF["Aw"][NUC_DF.index[0]]
	C_Aw = f"$$A_w$$ = {Aw}$$cm^4$$"

	N1_calc = VdV["L1"]*VdV["iL1max"]/(1e-4*Ae*VdV["Bmax"])
	N2 = int(N1_calc*VdV["N2N1_calc"])
	N1 = int(N2/VdV["N2N1"])
	C_N2 = f"$$N_2 = N_1 \\cdot n$$ = {N2}"
	C_N1 = f"$$N_1 = \\frac{{L_1 \\cdot i_{{L_{{1_{{max}}}}}}}}{{A_e \\cdot B_{{max}}}}$$ = {N1_calc:.2f} $$\\Rightarrow N_1$$ = {N1}"

	TAB_Askin = AWG_DF.loc[AWG_DF["ACu"] < VdV["Askin"]]
	TAB_f1 = TAB_Askin.loc[TAB_Askin["AWG"] == AWG_f1]
	ACu_f1 = TAB_f1["ACu"][TAB_f1.index[0]]
	AIso_f1 = TAB_f1["AIso"][TAB_f1.index[0]]
	TAB_f2 = TAB_Askin.loc[TAB_Askin["AWG"] == AWG_f2]
	ACu_f2 = TAB_f2["ACu"][TAB_f2.index[0]]
	AIso_f2 = TAB_f2["AIso"][TAB_f2.index[0]]

	NCP_f1 = ceil(VdV["Af1"]/ACu_f1)
	NCP_f2 = ceil(VdV["Af2"]/ACu_f2)
	C_NCP_f1 = f"$$NCP_{{fio_1}} = \\frac{{A_{{fio_1}}}}{{A_{{AWG_1}}}}$$ = {NCP_f1}"
	C_NCP_f2 = f"$$NCP_{{fio_2}} = \\frac{{A_{{fio_2}}}}{{A_{{AWG_2}}}}$$ = {NCP_f2}"

	lg = N1*N1*Ae*1e-4*4*pi*1e-7/VdV["L1"]
	C_lg = f"$$\\frac{{N_1^2 \\cdot A_e \\cdot \\mu_0}}{{L_1}}$$ = {R2SI(lg)}m"

	Aw_min = N1*NCP_f1*AIso_f1 + N2*NCP_f2*AIso_f2
	C_Aw_min = f"$$A_{{W_{{min}}}} = N_1 \\cdot NCP_1 \\cdot A_{{Iso_1}} + N_2 \\cdot NCP_2 \\cdot A_{{Iso_2}}$$ = {R2SI(Aw_min)}cm²"
	FE = Aw_min/Aw
	C_FE = f"$$FE = \\frac{{AW_{{min}}}}{{AW}}$$ = {FE:.3f}"

	SD_VdV(VdV,N1,N2,Co)
	IMG_CIRC_VdV = html.Img(src=Image.open("./images/circuitos/VdV.png"), width="100%")

	return C_Co, C_Ae, C_Aw, C_N1, C_N2, C_NCP_f1, C_NCP_f2, C_lg, C_Aw_min, C_FE, IMG_CIRC_VdV

# Vo = 75
# Po = 16,2
# n = 90