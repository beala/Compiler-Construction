def fib(n, cur, nex):
	if n != 0:
		return fib(n + -1, nex, cur + nex)
	else:
		return cur

def whi(n):
	if n == 0:
		return 0
	else:
		print fib(20, 0, 1)
		return whi(n+-1)

whi(100)
