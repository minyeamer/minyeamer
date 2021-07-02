num1 = 17.5
num2 = 10
cpx1 = 3 + 3j
cpx2 = 1 - 2j
str1 = "Hello"
str2 = "goorm"

print(num1 + num2)
print(str1 + str2)
print(num1 - num2)
print(num1 * num2)
print(num2 ** num1)    # 제곱
print(num1 / num2)
print(num1 // num2)    # 몫
print(num1 % num2)     # 나머지
print(cpx1 / cpx2)

#

a = 2
print("result = a : ", a)
a += 4
print("result += 4 : ", a)
a -= 2
print("result -= 2 : ", a)
a *= 5
print("result *= 5 : ", a)
a /= 2
print("result /= 2 : ", a)
a %= 3
print("result %= 3 : ", a)

#

a = True
b = False

print("true and false :", a and b)
print("true and true :", a and a)
print("true or false :", a or b)
print("false or false :", b or b)
print("not true :", not a)

#

print("100 == 100 :", 100 == 100)
print("100 == 200 :", 100 == 200)
print("100 != 100 :", 100 != 100)
print("100 != 200 :", 100 != 200)
print("0 < 9 :", 0 < 9)
print("0 > 9 :", 0 > 9)
print("0 >= 9 :", 0 >= 9)
print("0 <= 0 :", 0 <= 0)

#

a = 22    # 0b10110
b = 19    # 0b10011

print(a&b)    # AND
print(a|b)    # OR
print(a^b)    # XOR

#

a = 3
a &= 2
print("a &= 2 : ", a)
a |= 5
print("a |= 5 : ", a)
a ^= 4
print("a ^= 4 : ", a)




