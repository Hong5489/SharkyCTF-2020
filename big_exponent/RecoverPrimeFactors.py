from math import gcd #for gcd function (or easily implementable to avoid import)
import random #for random elements drawing in RecoverPrimeFactors

def failFunction():
	print("Prime factors not found")

def outputPrimes(a, n):
	p = gcd(a, n)
	q = n // p
	if p > q:
		p, q = q, p
	print("Found factors p and q")
	print("p = {0}".format(str(p)))
	print("q = {0}".format(str(q)))
	return p,q


def RecoverPrimeFactors(n, e, d):
	"""The following algorithm recovers the prime factor
		s of a modulus, given the public and private
		exponents.
		Function call: RecoverPrimeFactors(n, e, d)
		Input: 	n: modulus
				e: public exponent
				d: private exponent
		Output: (p, q): prime factors of modulus"""

	k = d * e - 1
	if k % 2 == 1:
		failFunction()
		return 0, 0
	else:
		t = 0
		r = k
		while(r % 2 == 0):
			r = int(r // 2)
			t += 1
		for i in range(1, 101):
			g = random.randint(0, n) # random g in [0, n-1]
			y = pow(g, r, n)
			if y == 1 or y == n - 1:
				continue
			else:
				for j in range(1, t): # j \in [1, t-1]
					x = pow(y, 2, n)
					if x == 1:
						p, q = outputPrimes(y - 1, n)
						return p, q
					elif x == n - 1:
						continue
					y = x
					x = pow(y, 2, n)
					if  x == 1:
						p, q = outputPrimes(y - 1, n)
						return p, q

n = 0xde508237659bf9ddfea3171e51b7bab7be61ca6fc8842d607030f2b836fb2fe9ad33c4e88d96362a69cebaa0c5e3646447a051ce15e6f81222f37e02655bed041f21ace12c690d50caad1c1a2d429d1b15d85016d51bcd5816c157a20ce517142858f1c8a83d84c5464eb1b4d5dee0fc618924b95769717e10e60ead9341454698360b88c23bee8b5c19e2cb3f81cc8020c236024339ac2d74042b94764ddfd0dce6c1da291d2b28b1875d9e0c35a1883962bc178b697a3713a133729a4510510a48f0cbd8780c7818f25571073b2d3924ae1c67c5be217b6829f4ff6cf3dcbe63195d7ae9bc8618ae2ab4749be54b0db559152d025fb14d136575c0d84afd9d
e = 0x92cbd92005563daed06c4b010fbc53dd98c63711dad7b4712bad8ba6bec38ace7f3ef48e491c88e46f38b4b3c443d6809976838fddaa023724045cf042b21325be66939840068b569a7366cec013ceecfe9d3b63b6817bcfe6d14d72a86992189880aa139237366dd76b197ad130aec9806056e755b6c7ea97c412dc82268cf6cb95b68749778b79e676d8dfea67f79bebf950b118d61aca718e57644462659071c2eef9a75fbf2d6fea2d54b4c658651568a958ee9c2ac1542f0b02a00787af1ecfbcf8b5cac1f2f34215feaf674c55eab4f9d289fcfa098947af3c17e1e1aea3f028ca077ca35b821995301ffde713364d9aac9a3c9ee481a8fcb5d598b6c1
d = 12943142410604045324963573717399150995389999892438958933300438824584828677265304042959568659708458383668696495604670543369903677147732370774826294074933249

RecoverPrimeFactors(n,e,d)