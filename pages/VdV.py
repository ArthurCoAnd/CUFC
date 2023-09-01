import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from PIL import Image
import json
from math import sqrt

from modules.SD_VdV import SD_VdV
from modules.GG_VeI import GG_VeI

from tools.R2SI import R2SI

dash.register_page(__name__, name="🛫 Voar de Volta 🛬", title="CUFC - Voar de Volta")

IMG_CIRC_VdV = html.Img(src=Image.open("./images/circuitos/VdV.png"), width="100%")
IMG_CIRC_VdV_E1 = html.Img(src=Image.open("./images/circuitos/VdV_e1.png"), width="50%")
IMG_CIRC_VdV_E2 = html.Img(src=Image.open("./images/circuitos/VdV_e2.png"), width="50%")
IMG_CIRC_VdV_E3 = html.Img(src=Image.open("./images/circuitos/VdV_e3.png"), width="50%")

ENT = ["Vi","Pi","N1","N2","fs","Ts","D","Vo","Ro","Po","Co","dVo","dVo_p"]

# ██       █████  ██    ██  ██████  ██    ██ ████████ 
# ██      ██   ██  ██  ██  ██    ██ ██    ██    ██    
# ██      ███████   ████   ██    ██ ██    ██    ██    
# ██      ██   ██    ██    ██    ██ ██    ██    ██    
# ███████ ██   ██    ██     ██████   ██████     ██    

layout = html.Div([
	html.Div("Voar de Volta", style={"font-size":40, "textAlign":"center"}),
	html.Hr(),
	dbc.Container([
		dbc.Row([
			dbc.Col(children=[], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2, id="VdV-ent"),
			dbc.Col([
				html.Center(children=IMG_CIRC_VdV, id="VdV-circ"),
			], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10),
		]),
	]),
	html.Hr(),
	html.Div("Cálculos", style={"font-size":30, "textAlign":"center"}),
	html.Hr(),
	dbc.Container([
		dbc.Row([html.Center(dcc.Markdown(children="", id="C-ViIiPi", mathjax=True, style={"font-size":30})),]),
		dbc.Row([html.Center(dcc.Markdown(children="", id="C-L1", mathjax=True, style={"font-size":30})),]),
		dbc.Row([html.Center(dcc.Markdown(children="", id="C-DT", mathjax=True, style={"font-size":30})),]),
		dbc.Row([html.Center(dcc.Markdown(children="", id="C-L2", mathjax=True, style={"font-size":30})),]),
		dbc.Row([html.Center(dcc.Markdown(children="", id="C-Comin", mathjax=True, style={"font-size":30})),]),
		dbc.Row([html.Center(dcc.Markdown(children="", id="C-iL1max", mathjax=True, style={"font-size":30})),]),
		dbc.Row([html.Center(dcc.Markdown(children="", id="C-iL2max", mathjax=True, style={"font-size":30})),]),
		dbc.Row([html.Center(dcc.Markdown(children="", id="C-tx", mathjax=True, style={"font-size":30})),]),
	]),
	html.Hr(),
	html.Div("Tensões e Correntes", style={"font-size":30, "textAlign":"center"}),
	html.Hr(),
	dbc.Container([
		dbc.Row([dcc.Dropdown(["Enrolamento Primário", "Enrolamento Secundário", "Chave", "Diodo"], value="Enrolamento Primário", style={"font-size":20, "textAlign":"center"}, id="DD-V&I"),]),
		dbc.Row([dcc.Graph(id="G-V&I"),]),
	]),
	html.Hr(),
	html.Div("Etapas de Operação", style={"font-size":30, "textAlign":"center"}),
	html.Hr(),
	dbc.Container([
		dbc.Row([html.Div("Primeira Etapa", style={"font-size":20, "textAlign":"center"}),]),
		dbc.Row([html.Center(children=IMG_CIRC_VdV_E1, id="VdV-circ-e1"),]),
		
		dbc.Row([html.Div("Segunda Etapa", style={"font-size":20, "textAlign":"center"}),]),
		dbc.Row([html.Center(children=IMG_CIRC_VdV_E2, id="VdV-circ-e2"),]),

		dbc.Row([html.Div("Terceira Etapa", style={"font-size":20, "textAlign":"center"}),]),
		dbc.Row([html.Center(children=IMG_CIRC_VdV_E3, id="VdV-circ-e3"),]),
	]),
	html.Hr(),
])

@callback([
		Output("VdV-ent", "children"), Output("VdV-circ", "children"),
		Output("C-ViIiPi", "children"), Output("C-L1", "children"), Output("C-L2", "children"), Output("C-Comin", "children"),
		Output("C-DT", "children"), Output("C-iL1max", "children"), Output("C-iL2max", "children"), Output("C-tx", "children"),
		], Input("VdV-data", "data"))
def configurar_elementos(VdV):
	ENTRADAS = html.Div([
		#
		# Variáveis de Entrada
		#
		dbc.Row([
			html.Center(dbc.RadioItems(["Vi","Ii","Pi"], "Ii", inline=True, id="RI-ViIiPi"))
		]),
		dbc.Row([
			dbc.Col([html.Div(f"Vi")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-Vi", value=VdV["Vi"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div(f"V")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div(f"Ii")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-Ii", value=VdV["Ii"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div(f"A")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div(f"Pi")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-Pi", value=VdV["Pi"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div(f"W")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		html.Hr(),
		#
		# Variáveis de Saída
		#
		dbc.Row([
			html.Center(dbc.RadioItems(["Vo","Ro","Po"], VdV["RI_VoRoPo"], inline=True, id="RI-VoRoPo"))
		]),
		dbc.Row([
			dbc.Col([html.Div(f"Vo")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-Vo", value=VdV["Vo"], type="number", debounce=True, disabled=VdV["RI_Vo"])], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div(f"V")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div(f"Ro")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-Ro", value=VdV["Ro"], type="number", debounce=True, disabled=VdV["RI_Ro"])], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div(f"Ω")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div(f"Po")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-Po", value=VdV["Po"], type="number", debounce=True, disabled=VdV["RI_Po"])], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div(f"W")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div(f"Co")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-Co", value=VdV["Co"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div(f"F")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			html.Center(dbc.RadioItems(["V","%"], VdV["RI_dVo_Vp"], inline=True, id="RI-dVo-Vp"))
		]),
		dbc.Row([
			dbc.Col([html.Div(f"ΔVo")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-dVo", value=VdV["dVo"], type="number", debounce=True, disabled=VdV["RI_dVo"])], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div(f"V")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div(f"ΔVo")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-dVo_p", value=VdV["dVo_p"], type="number", debounce=True, disabled=VdV["RI_dVo_p"])], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div(f"%")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		html.Hr(),
		#
		# Variáveis de Relação de Transformação
		#
		dbc.Row([
			dbc.Col([html.Div(f"N1")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-N1", value=VdV["N1"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
		]),
		dbc.Row([
			dbc.Col([html.Div(f"N2")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-N2", value=VdV["N2"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
		]),
		html.Hr(),
		#
		# Variáveis de Enrolamento
		#
		dbc.Row([
			dbc.Col([html.Div(f"L1")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-L1", value=VdV["L1"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div(f"H")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div(f"L2")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-L2", value=VdV["L2"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div(f"H")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		html.Hr(),
		#
		# Variáveis de Tempo
		#
		dbc.Row([
			html.Center(dbc.RadioItems(["fs","Ts"], VdV["RI_fsTs"], inline=True, id="RI-fsTs"))
		]),
		dbc.Row([
			dbc.Col([html.Div(f"fs")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-fs", value=VdV["fs"], type="number", debounce=True, disabled=VdV["RI_fs"])], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div(f"Hz")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div(f"Ts")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-Ts", value=VdV["Ts"], type="number", debounce=True, disabled=VdV["RI_Ts"])], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
			dbc.Col([html.Div(f"s")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
		]),
		dbc.Row([
			dbc.Col([html.Div(f"D")], xs=1, sm=1, md=2, lg=2, xl=2, xxl=2),
			dbc.Col([dbc.Input(id=f"I-D", value=VdV["D"], type="number", debounce=True)], xs=2, sm=2, md=8, lg=8, xl=8, xxl=8),
		]),
	])

	SD_VdV(VdV)
	IMG_CIRC_VdV = html.Img(src=Image.open("./images/circuitos/VdV.png"), width="100%")

	C_ViIiPi = f"$$I_i = \\frac{{P_i}}{{V_i}} = {R2SI(VdV['Ii'])}A$$"
	C_L1 = f"$$L_1 = \\frac{{V_i^2 \\cdot D^2}}{{2 \\cdot P_i \\cdot f_s}} = {R2SI(VdV['L1'])}H$$"
	C_L2 = f"$$L_2 = {R2SI(VdV['L2'])}H$$"
	C_Comin = f"$$C_{{o_{{min}}}} = {R2SI(VdV['Comin'])}F$$"
	C_DT = f"$$DT = {R2SI(VdV['DT'])}s$$"
	C_iL1max = f"$$i_{{L_{{1_{{max}}}}}} = i_{{S_{{max}}}} = \\frac{{V_i \\cdot D \\cdot T_s}}{{L_1}} = {R2SI(VdV['iL1max'])}A$$"
	C_iL2max = f"$$i_{{L_{{2_{{max}}}}}} = i_{{D_{{max}}}} = \\frac{{V_i \\cdot D \\cdot T_s \\cdot N_1}}{{L_1 \\cdot N_2}} = {R2SI(VdV['iL2max'])}A$$"
	C_tx = f"$$t_x = D \\cdot T_s \\cdot \\left( \\frac{{V_i \\cdot N_2}}{{V_o \\cdot N_1}} + 1 \\right) = {R2SI(VdV['tx'])}s$$"

	return ENTRADAS, IMG_CIRC_VdV, C_ViIiPi, C_L1, C_L2, C_Comin, C_DT, C_iL1max, C_iL2max, C_tx

def salvar_VdV_data(VdV):
	with open("./data/VdV.json", "w") as arq:
		json.dump(VdV, arq, indent=2)

@callback([Output("I-fs", "disabled"), Output("I-Ts", "disabled")], Input("RI-fsTs", "value"))
def aleração_RI_FreqPer(RI):
	if RI != "fs": return False, True
	else: return True, False

@callback([Output("I-Vo", "disabled"), Output("I-Ro", "disabled"), Output("I-Po", "disabled")], Input("RI-VoRoPo", "value"))
def aleração_RI_VoRoPo(RI):
	if RI == "Vo": return True, False, False
	elif RI == "Ro": return False, True, False
	else: return False, False, True

@callback([Output("I-dVo", "disabled"), Output("I-dVo_p", "disabled")], Input("RI-dVo-Vp", "value"))
def aleração_RI_FreqPer(RI):
	if RI != "V": return False, True
	else: return True, False

@callback(Output("G-V&I", "figure"), Input("DD-V&I", "value"), State("VdV-data", "data"))
def alteraração_DD_VeI(DD,VdV):
	return GG_VeI(DD,VdV)

@callback([
		Output("VdV-data", "data"),
		Output("I-fs", "value"), Output("I-Ts", "value"),
		Output("I-Vo", "value"), Output("I-Ro", "value"), Output("I-Po", "value"),
		Output("I-dVo", "value"), Output("I-dVo_p", "value"),
	], [[Input(f"I-{i}", "value") for i in ENT]], [State("VdV-data", "data"), State("RI-fsTs", "value"), State("RI-VoRoPo", "value"), State("RI-dVo-Vp", "value")])
def alteração_das_entradas(*args):
	VdV = {}
	for i, e in enumerate(ENT):
		VdV[e] = args[0][i]
	VdV_antigo = args[1]
	for e in ENT:
		if VdV[e] != VdV_antigo[e]:
			print(f"> {e} = {VdV[e]}")

	RI_fsTs = args[2]
	if RI_fsTs == "fs":
		VdV["RI_fsTs"] = "fs"
		VdV["RI_fs"] = True; VdV["RI_Ts"] = False
		VdV["fs"] = 1/VdV["Ts"]
	else:
		VdV["RI_fsTs"] = "Ts"
		VdV["RI_fs"] = False; VdV["RI_Ts"] = True
		VdV["Ts"] = 1/VdV["fs"]

	RI_VoRoPo = args[3]
	if RI_VoRoPo == "Vo":
		VdV["RI_VoRoPo"] = "Vo"
		VdV["RI_Vo"] = True; VdV["RI_Ro"] = False; VdV["RI_Po"] = False
		VdV["Vo"] = sqrt(VdV["Po"]*VdV["Ro"])
	elif RI_VoRoPo == "Ro":
		VdV["RI_VoRoPo"] = "Ro"
		VdV["RI_Vo"] = False; VdV["RI_Ro"] = True; VdV["RI_Po"] = False
		VdV["Ro"] = VdV["Vo"]*VdV["Vo"]/VdV["Po"]
	else:
		VdV["RI_VoRoPo"] = "Po"
		VdV["RI_Vo"] = False; VdV["RI_Ro"] = False; VdV["RI_Po"] = True
		VdV["Po"] = VdV["Vo"]*VdV["Vo"]/VdV["Ro"]

	RI_dVo_Vp = args[4]
	if RI_dVo_Vp == "V":
		VdV["RI_dVo_Vp"] = "V"
		VdV["dVo"] = VdV["Vo"]*VdV["dVo_p"]/100
		VdV["RI_dVo"] = True; VdV["RI_dVo_p"] = False
	else:
		VdV["RI_dVo_Vp"] = "%"
		VdV["dVo_p"] = 100*VdV["dVo"]/VdV["Vo"]
		VdV["RI_dVo"] = False; VdV["RI_dVo_p"] = True

	VdV["Ii"] = VdV["Pi"]/VdV["Vi"]

	VdV["Io"] = VdV["Po"]/VdV["Vo"]

	VdV["L1"] = VdV["Vi"]*VdV["Vi"]*VdV["D"]*VdV["D"]/(2*VdV["Pi"]*VdV["fs"])

	VdV["DT"] = VdV["D"]*VdV["Ts"]

	VdV["N1N2"] = VdV["N1"]/VdV["N2"]
	
	VdV["N2N1"] = VdV["N2"]/VdV["N1"]
	
	VdV["L2"] = VdV["L1"]*VdV["N2N1"]*VdV["N2N1"]

	VdV["Comin"] = VdV["Io"]*VdV["DT"]/VdV["dVo"]
	
	VdV["iL1max"] = VdV["Vi"]*VdV["DT"]/VdV["L1"]
	VdV["iSmax"] = VdV["iL1max"]
	VdV["iL2max"] = VdV["iL1max"]*VdV["N1N2"]
	VdV["iDmax"] = VdV["iL2max"]
	VdV["tx"] = VdV["DT"]*((VdV["N2N1"]*VdV["Vi"]/VdV["Vo"]) + 1)
	VdV["VL1min"] = -VdV["Vo"]*VdV["N1N2"]
	VdV["VL2max"] = VdV["Vi"]*VdV["N2N1"]
	VdV["VSmax"] = VdV["Vi"] + VdV["Vo"]*VdV["N1N2"]
	VdV["VDmax"] = VdV["Vo"] + VdV["Vi"]*VdV["N2N1"]

	salvar_VdV_data(VdV)

	return VdV, VdV["fs"], VdV["Ts"], VdV["Vo"], VdV["Ro"], VdV["Po"], VdV["dVo"], VdV["dVo_p"]

# A
# Vi = 100
# Vo = 300
# Po = 50
# dVo_p = 1%

# B
# Vi = 100
# Vo = 100
# dVo = 5
# Po = 100

# C
# L1 = 2.13e-3
# L2 = 48e-6
# Vi = 400
# Vo = 50
# Po = ?

# D
# Po = 200
# Vi = 500
# Vo = 80
# iP1max <= 1.8
# vSmax <= 850