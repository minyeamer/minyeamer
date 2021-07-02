# int        ex) 1, 2, 0
# float      ex) 3.15, -2.1
# complex    ex) j, 2j, 3 + 2j
#  복소수형에서 실수부는 "변수.real", 허수부는 "변수.imag",
#  켤레복소수는 "변수.conjugate()"로 반환
# 16진수      ex) 0xDA
# 2진수       ex) 0b110101

a = 10
b = -2.5
c = 1 + 2j
d = 0xDA # 218

print(a, type(a))
print(b, type(b))
print(c, c.real , c.imag, c.conjugate(), type(c))
print(d, type(d))

print(a + b, type(a + b))
print(c + d, type(c + d))

#

a = "Hello goorm!"
if (a) : #만약 (a)의 값이 존재한다면 
    print("참")
else : #아니면
    print("거짓")

b = ""
if (b == True) : #만약 (b)의 값이 존재한다면
    print("참")
else : #아니면
    print("거짓")   
