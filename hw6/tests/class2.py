class C:
	class D:
		0

C.D.x = 99

print (C.D if True else C).x
