def r(x):
	print x+-1
	return 0 if x+-1 == 0 else r(x+-1)

r(10)
