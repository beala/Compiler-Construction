def fib(f):
	return 1 if f == 1 else 0 if f == 0 else fib(f+ -1) + fib(f +-2)

print fib(input())
