def r(lis, cur):
	nex = cur+-1
	lis = [nex] + lis
	return lis if nex == 0 else r(lis, nex)

print r([],input())
