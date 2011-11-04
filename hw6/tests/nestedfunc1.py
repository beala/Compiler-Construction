x = 1
def f():
	x = 2
	def g():
		x = 3
		print x
	g()
f() 
