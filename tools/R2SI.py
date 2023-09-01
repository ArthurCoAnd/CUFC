# Bibliotecas
from si_prefix import split
from si_prefix import si_format as SI
from random import random, randint
from math import modf
from numpy import isnan

def R2SI(x):
	if x == None or isnan(x):
		return "? "
	else:
		if modf(x)[0] == 0.0:
			xi = int(x)
			if abs(xi) < 1000:
				return xi
		else: xi = x/10**split(x)[1]
		
		if xi <= 10:
			return SI(x,2)
		elif xi <= 100:
			return SI(x,1)
		elif xi <= 1000:
			return SI(x,0)
		else:
			return SI(x,1)
	
if __name__ == "__main__":
	for x in range(5):
		print(f"> {x}")
		r = random()*10**-x
		print(f"{r} - {R2SI(r)}")
		r = random()*10**x
		print(f"{r} - {R2SI(r)}")
	for x in range(5):
		print(f"> {x}")
		r = randint(100,1000)*10**-x
		print(f"{r} - {R2SI(r)}")
		r = randint(100,1000)*10**x
		print(f"{r} - {R2SI(r)}")