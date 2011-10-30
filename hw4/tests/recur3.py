def r(lis, cur):
	nex = cur+-1
	lis = lis + [nex]
	return lis if nex == 0 else r(lis, nex)

print r([],10)
