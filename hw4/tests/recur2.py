def r(x):
	y = x+-1
	print y
	return 0 if y == 0 else l(y)

def l(x):
	y = x+-1
	print y
	return 0 if y == 0 else r(y)

r(10)
