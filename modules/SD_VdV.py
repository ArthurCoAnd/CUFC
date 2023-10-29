import os, sys
parent = os.path.abspath(".")
sys.path.insert(1, parent)

import matplotlib
matplotlib.use('Agg')

import schemdraw
import schemdraw.elements as elm

import pandas as pd

from tools.R2SI import R2SI

def SD_VdV(VdV,N1,N2,Co):
	
	with schemdraw.Drawing(show=False) as d:
		# Configurações
		d.config(fontsize=13)

		# Declaração dos Elementos
		Vi_str = f"$V_i$\n{R2SI(VdV['Vi'])}V"
		Vi = elm.SourceV().up().label(Vi_str)
		L1_str = f"$L_1$\n{R2SI(VdV['L1'])}H"
		L2_str = f"$L_2$\n{R2SI(VdV['L2'])}H"
		N1_str = f"$N_1$\n{N1}"
		N2_str = f"$N_2$\n{N2}"
		TR1_str = f"{L1_str}\n{N1_str}"
		TR2_str = f"{L2_str}\n{N2_str}"
		TRN_str = f"N1 : N2\n{N1} : {N2}"
		Tr = elm.Transformer(t1=5, t2=5).label(L1_str,"lft").label(L2_str,"rgt").label(TRN_str)
		S = elm.Switch().label("$S$")
		D = elm.Diode().label("$D$")
		Co_str = f"$C_o$\n{R2SI(Co)}F"
		Co = elm.Capacitor().label(Co_str)
		Po_str = f"$P_o$\n{R2SI(VdV['Po'])}W"
		Po = elm.Resistor().label(Po_str)
		Vo_str = f"$V_o$\n{R2SI(VdV['Vo'])}V"
		Vo = elm.Gap().label(("+",Vo_str,"–"))

		# Circuito
		d += Vi
		d += elm.Line().up().length(d.unit/3) # Lin1
		d += elm.Line().right() # Lin2
		d += elm.Dot()
		d += Tr.right().anchor("p1")

		d += S.down().at(Tr.p2)
		d += elm.Line().left() # Lin3
		d += elm.Line().up().length(d.unit/3) # Lin4

		d += D.right().at(Tr.s1)
		d += elm.Dot()
		d.push(); d += Co.down(); d.pop()
		d += elm.Line().right() # Lin5
		d += elm.Dot()
		d.push(); d += Po.down(); d.pop()
		d += elm.Line().right().length(d.unit/2) # Lin6
		d += elm.Dot()
		d += Vo.down()
		d += elm.Dot()
		d += elm.Line().left().length(d.unit/2) # Lin7
		d += elm.Dot()
		d += elm.Line().left() # Lin8
		d += elm.Dot()
		d += elm.Line().left() # Lin9
		d += elm.Line().up().length(d.unit/3) # Lin10
		d += elm.Dot()

		d.save(fname=f"./images/circuitos/VdV.png", dpi=300)