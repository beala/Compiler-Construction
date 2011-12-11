def sum(n, t):
	if n == 0:
		return t
	else:
		return sum(n + -1, n + t)

def whil(n, func):
	if n == 0:
		return 0
	else:
		func(1000, 0)
		return whil(n + -1, func)

whil(1000, sum)
