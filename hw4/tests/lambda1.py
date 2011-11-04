def f():
	y = 10
	return lambda x: x + y
d = f()
print d((lambda : 10)())
