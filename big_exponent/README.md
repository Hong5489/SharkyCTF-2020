# Beware my big exponent 299 points
>I made my own certificate on my local network.
>Have a look, communication between my client and my server is sooo secure!
>Creator: Fratso

[Pcap file](beware_my_big_exponent.pcapng)

Try using `wireshark` to open it:
![image1](image1.png)

Notice there is alot of `TLS` data, means it is encrypted using RSA certificate.

Since the challenge title is `Beware my big exponent`, so we need to find the certificate modulus and exponent (N and e).

Then I filter the packets with `tls` only, found a `Server hello, certificate` packet inside got a certificate with public key info:
![image2](image2.png)

Then **right click > Copy > Value** to copy the value
```py
n = 0xde508237659bf9ddfea3171e51b7bab7be61ca6fc8842d607030f2b836fb2fe9ad33c4e88d96362a69cebaa0c5e3646447a051ce15e6f81222f37e02655bed041f21ace12c690d50caad1c1a2d429d1b15d85016d51bcd5816c157a20ce517142858f1c8a83d84c5464eb1b4d5dee0fc618924b95769717e10e60ead9341454698360b88c23bee8b5c19e2cb3f81cc8020c236024339ac2d74042b94764ddfd0dce6c1da291d2b28b1875d9e0c35a1883962bc178b697a3713a133729a4510510a48f0cbd8780c7818f25571073b2d3924ae1c67c5be217b6829f4ff6cf3dcbe63195d7ae9bc8618ae2ab4749be54b0db559152d025fb14d136575c0d84afd9d
e = 0x92cbd92005563daed06c4b010fbc53dd98c63711dad7b4712bad8ba6bec38ace7f3ef48e491c88e46f38b4b3c443d6809976838fddaa023724045cf042b21325be66939840068b569a7366cec013ceecfe9d3b63b6817bcfe6d14d72a86992189880aa139237366dd76b197ad130aec9806056e755b6c7ea97c412dc82268cf6cb95b68749778b79e676d8dfea67f79bebf950b118d61aca718e57644462659071c2eef9a75fbf2d6fea2d54b4c658651568a958ee9c2ac1542f0b02a00787af1ecfbcf8b5cac1f2f34215feaf674c55eab4f9d289fcfa098947af3c17e1e1aea3f028ca077ca35b821995301ffde713364d9aac9a3c9ee481a8fcb5d598b6c1
```
Thats very large...

Research about `RSA big exponent` then I found this link:
[(Very) Large RSA Private Exponent
Vulnerabilities](https://pdfs.semanticscholar.org/20b9/177cd4d6d4ad68d85b3a31d297e0686ca970.pdf)

As the link says, it is vulnerable to:
1. Wiener attack
2. Boneh & Durfee attack
3. Bl¨omer & May attack

## Attempt Wiener attack
Found a awesome github link that implement wiener attack:
[Wiener attack python](https://github.com/pablocelayes/rsa-wiener-attack)

But I tried it failed =(
```py
n = 0xde508237659bf9ddfea3171e51b7bab7be61ca6fc8842d607030f2b836fb2fe9ad33c4e88d96362a69cebaa0c5e3646447a051ce15e6f81222f37e02655bed041f21ace12c690d50caad1c1a2d429d1b15d85016d51bcd5816c157a20ce517142858f1c8a83d84c5464eb1b4d5dee0fc618924b95769717e10e60ead9341454698360b88c23bee8b5c19e2cb3f81cc8020c236024339ac2d74042b94764ddfd0dce6c1da291d2b28b1875d9e0c35a1883962bc178b697a3713a133729a4510510a48f0cbd8780c7818f25571073b2d3924ae1c67c5be217b6829f4ff6cf3dcbe63195d7ae9bc8618ae2ab4749be54b0db559152d025fb14d136575c0d84afd9d
e = 0x92cbd92005563daed06c4b010fbc53dd98c63711dad7b4712bad8ba6bec38ace7f3ef48e491c88e46f38b4b3c443d6809976838fddaa023724045cf042b21325be66939840068b569a7366cec013ceecfe9d3b63b6817bcfe6d14d72a86992189880aa139237366dd76b197ad130aec9806056e755b6c7ea97c412dc82268cf6cb95b68749778b79e676d8dfea67f79bebf950b118d61aca718e57644462659071c2eef9a75fbf2d6fea2d54b4c658651568a958ee9c2ac1542f0b02a00787af1ecfbcf8b5cac1f2f34215feaf674c55eab4f9d289fcfa098947af3c17e1e1aea3f028ca077ca35b821995301ffde713364d9aac9a3c9ee481a8fcb5d598b6c1
print hack_RSA(e,n)
```
```
Result: None
```

## Attempt Boneh Durfee
Found a awesome github link that implement Boneh Durfee attack:
[Boneh Durfee Attack sage](https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage)

I run it in [Sage Cell Server Online](https://sagecell.sagemath.org/)

Because it uses Python 3 so need to modify the `print` function to `print()`

[Sage script](boneh_durfee.sage)

I modified and substitute the `n` and `e` then run it:
```
=== checking values ===
* delta: 0.180000000000000
* delta < 0.292 True
* size of e: 2047
* size of N: 2047
* m: 4 , t: 2
=== running algorithm ===
* removing unhelpful vector 0
6 / 18  vectors are not helpful
det(L) < e^(m*n) (good! If a solution exists < N^delta, it )will be found
00 X 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ~
01 X X 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 
02 0 0 X 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ~
03 0 0 X X 0 0 0 0 0 0 0 0 0 0 0 0 0 0 
04 0 0 X X X 0 0 0 0 0 0 0 0 0 0 0 0 0 
05 0 0 0 0 0 X 0 0 0 0 0 0 0 0 0 0 0 0 ~
06 0 0 0 0 0 X X 0 0 0 0 0 0 0 0 0 0 0 ~
07 0 0 0 0 0 X X X 0 0 0 0 0 0 0 0 0 0 
08 0 0 0 0 0 X X X X 0 0 0 0 0 0 0 0 0 
09 0 0 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 0 ~
10 0 0 0 0 0 0 0 0 0 X X 0 0 0 0 0 0 0 ~
11 0 0 0 0 0 0 0 0 0 X X X 0 0 0 0 0 0 
12 0 0 0 0 0 0 0 0 0 X X X X 0 0 0 0 0 
13 0 0 0 0 0 0 0 0 0 X X X X X 0 0 0 0 
14 X X 0 X X 0 0 0 0 0 0 0 0 0 X 0 0 0 
15 0 0 X X X 0 X X X 0 0 0 0 0 0 X 0 0 
16 0 0 0 0 0 X X X X 0 X X X X 0 0 X 0 
17 0 0 X X X 0 X X X 0 0 X X X 0 X X X 
optimizing basis of the lattice via LLL, this can take a long time
LLL is done!
looking for independent vectors in the lattice
found them, using vectors 0 and 1
=== solution found ===
private key found: 12943142410604045324963573717399150995389999892438958933300438824584828677265304042959568659708458383668696495604670543369903677147732370774826294074933249
=== 0.6928098201751709 seconds ===
```
Yes!! Looks like the private key was found!

But we still need to find `p` and `q` (Factors of n) in order to generate priavte key file

After some research on `recover prime factors from d` I found this link:
[RecoverPrimeFactors Python Script](https://gist.github.com/ddddavidee/b34c2b67757a54ce75cb)

Then I try put `n,e,d` and run it :
```py
Found factors p and q
p = 164441167076194050840321817212536500388636415391892106491247092164367645140884158927017205813336612847593526287801167563423504176790975721780418425966481749425234107905692891680874509476677160519369597538227403671389395206356958865156041256171902828271284573242174288595261126461987274686277681505513120989184
q = 170666533814295917828331869425665971317070188692399509223519094595113142671934591620768926038831184472718590967100763812201354170079400637193416916951832726356328597418015817377866563218909418909360207332115160652812930509379249560291922300146725394287083516536936847852702375514055379610743173434893282267733
```
Notice the `p` is not prime number...

Then i try fix the script by changing line 9 from `q = int(n / p)` to `q = n // p`

[Modified script](RecoverPrimeFactors.py)
```py
Found factors p and q
p = 164441167076194048289177549751957300156423005925381420194157446896979106243555923290589933246156646059419620292139416182066883241128056398157417093440471693509548094733904144948446333651229095822135394923077369387260929093126330048595259377887997453551290504742789553131676076615054763462443452200481155814953
q = 170666533814295917828331869425665971317070188692399509223519094595113142671934591620768926038831184472718590967100763812201354170079400637193416916951832726356328597418015817377866563218909418909360207332115160652812930509379249560291922300146725394287083516536936847852702375514055379610743173434893282267733
```

Looks like it works!

I'm using Python Crypto Module to generate the private key:
[PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html#Crypto.PublicKey.RSA.construct)

Lets generate the private key using my [python script](solve.py)!
```python
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
import gmpy2
n = 0xde50...
e = 0x92cb...
p = 16444...
q = 17066...
d = 12943...
assert(n==p*q)
priv = RSA.construct((n, e, inverse(e, (p - 1) * (q - 1))))
open("priv.pem",'w').write(priv.exportKey('PEM'))
```
Inside [priv.pem](priv.pem)
```
-----BEGIN RSA PRIVATE KEY-----
MIIEYgIBAAKCAQEA3lCCN2Wb+d3+oxceUbe6t75hym/IhC1gcDDyuDb7L+mtM8To
jZY2KmnOuqDF42RkR6BRzhXm+BIi834CZVvtBB8hrOEsaQ1Qyq0cGi1CnRsV2FAW
1RvNWBbBV6IM5RcUKFjxyKg9hMVGTrG01d7g/GGJJLlXaXF+EOYOrZNBRUaYNguI
wjvui1wZ4ss/gcyAIMI2AkM5rC10BCuUdk3f0NzmwdopHSsosYddngw1oYg5YrwX
i2l6NxOhM3KaRRBRCkjwy9h4DHgY8lVxBzstOSSuHGfFviF7aCn0/2zz3L5jGV16
6byGGK4qtHSb5UsNtVkVLQJfsU0TZXXA2Er9nQKCAQEAksvZIAVWPa7QbEsBD7xT
3ZjGNxHa17RxK62Lpr7Dis5/PvSOSRyI5G84tLPEQ9aAmXaDj92qAjckBFzwQrIT
Jb5mk5hABotWmnNmzsATzuz+nTtjtoF7z+bRTXKoaZIYmICqE5I3Nm3Xaxl60TCu
yYBgVudVtsfql8QS3IImjPbLlbaHSXeLeeZ22N/qZ/eb6/lQsRjWGspxjldkRGJl
kHHC7vmnX78tb+otVLTGWGUVaKlY7pwqwVQvCwKgB4evHs+8+LXKwfLzQhX+r2dM
Veq0+dKJ/PoJiUevPBfh4a6j8CjKB3yjW4IZlTAf/ecTNk2arJo8nuSBqPy11Zi2
wQJBAPcgwyMCxwgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAECgYEA6iwH3JSUBvo35o28qp4NBcnxUqVA63ls
wzStLPaGJU9lK6MsUzNy1SptVlJ4SMWAVLCMxOEdd+kNIFUC3ZUbUTrtvnAXm/JZ
DJ4BECIQbEfQhjXVkRT+NRMttEPgYQYI2cXo14386blESJbrItZkt3VFL2OLDqag
EValexBZlikCgYEA8wmGsMQpLWvtwzNj31gX3e5BWEGIdKYkeod8HFGeN/acAFKz
xLDauFhOoxCD3MeaMug9rBtz/KqKIpGuhVtC0tdW37ZseRCPa4Joi4hv5vyK1CoH
KSvaodSH0jkLfYceHbW+KoM6/H/JcfrdgBkXRTT7MrkH0mQ9or3nwtU7UlUCQQD3
IMMjAscIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAABAkEA9yDDIwLHCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQKBgQDgTuMGPFR7csWQ
/MD1Px/4Rm9bIyhZWJWICA4hVF6R4EJKK+bY//B+oqrwVvlwqcc3ITGcIu16ZesC
vtuO7eEy+9w+dFAa0MD1wEWbl6d/46sMupPxeFyEZsCbUMWhgk2ao63H9FDRsgQH
UyA5/+/0o2nrIFZyFtKT7IgbxrmmOw==
-----END RSA PRIVATE KEY-----
```

Then use Wireshark to decrypt the encrypted packets!

In wireshark > Edit > Preferences > Protocols > TLS > Edit
![image3](image3.png)

Then type in the details and import the `priv.pem`
![image4](image4.png)

After Click OK, notice the packets has been decrypted!
![image5](image5.png)

Got one 1099 length packets looks suspicious, then I click inside then got the flag!!!
![image6](image6.png)

## Flag
```
shkCTF{Publ1c_3xp_t0o_b1G_6a8eaf56ab89cb}
```