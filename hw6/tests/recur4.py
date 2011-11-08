def reversed(toReverse, l):
		return [] if l == 0 else [toReverse[l+-1]] + reversed(toReverse, l + -1)

print reversed([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], 20)
