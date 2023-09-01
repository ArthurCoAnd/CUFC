from plotly.subplots import make_subplots
import plotly.graph_objects as go

def GG_VeI(DD, VdV):	
	DT = VdV["DT"]
	tx = VdV["tx"]
	Ts = VdV["Ts"]

	Vi = VdV["Vi"]
	Vo = VdV["Vo"]

	# Enrolamento Primário
	G_L1 = make_subplots(rows=1, cols=2)

	VL1min = VdV["VL1min"]
	x = [0, DT, DT, tx, tx, Ts]
	y = [Vi, Vi, VL1min, VL1min, 0, 0]
	G_L1.add_trace(go.Scatter(x=x, y=y, name="vL1"), row=1, col=1)

	iL1max = VdV["iL1max"]
	x = [0, DT, DT, tx, Ts]
	y = [0, iL1max, 0, 0, 0]
	G_L1.add_trace(go.Scatter(x=x, y=y, name="iL1"), row=1, col=2)

	# Chave
	G_S = make_subplots(rows=1, cols=2)

	VSmax = VdV["VSmax"]
	x = [0, DT, DT, tx, tx, Ts]
	y = [0, 0, VSmax, VSmax, Vi, Vi]
	G_S.add_trace(go.Scatter(x=x, y=y, name="vS"), row=1, col=1)
	
	iSmax = VdV["iSmax"]
	x = [0, DT, DT, tx, Ts]
	y = [0, 0, iSmax, 0, 0]
	G_S.add_trace(go.Scatter(x=x, y=y, name="iS"), row=1, col=2)

	# Enrolamento Secundário
	G_L2 = make_subplots(rows=1, cols=2)

	VL2max = VdV["VL2max"]
	x = [0, DT, DT, tx, tx, Ts]
	y = [VL2max, VL2max, -Vo, -Vo, 0, 0]
	G_L2.add_trace(go.Scatter(x=x, y=y, name="vL2"), row=1, col=1)

	iL2max = VdV["iL2max"]
	x = [0, DT, DT, tx, Ts]
	y = [0, 0, iL2max, 0, 0]
	G_L2.add_trace(go.Scatter(x=x, y=y, name="iL2"), row=1, col=2)

	# Diodo
	G_D = make_subplots(rows=1, cols=2)

	VDmax = VdV["VDmax"]
	x = [0, DT, DT, tx, tx, Ts]
	y = [VDmax, VDmax, 0, 0, Vo, Vo]
	G_D.add_trace(go.Scatter(x=x, y=y, name="vD"), row=1, col=1)
	
	iDmax = VdV["iDmax"]
	x = [0, DT, DT, tx, Ts]
	y = [0, iDmax, 0, 0, 0]
	G_D.add_trace(go.Scatter(x=x, y=y, name="iD"), row=1, col=2)

	if DD == "Enrolamento Primário": return G_L1
	elif DD == "Enrolamento Secundário": return G_L2
	elif DD == "Chave": return G_S
	else: return G_D