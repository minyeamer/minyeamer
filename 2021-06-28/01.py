'''
num = 3
num = 3.14
num = "Hello World"
print(num)
print("싸지방에서 하는 첫 파이썬")
'''

import math

str = 'Korea'
num1 = 3.14
num2 = '3'

print(type(str))
print(type(num1))
print(type(num2))
print()

print(num1 * int(num2))

var1 = var2 = var3 = "Hello World"
print(var1)
print(var2)
print(var3)
print()

print(len(var1))
print(var1[0: 5])
print(var1[0: len(var1)-1])
print()

var1, var2, var3 = 'a', 'b', 'c'
print(var1)
print(var2)
print(var3)
print()

a, b = 100, 200
print(a, b)
a, b = b, a
print(a, b)
print()

print(math.pi)
print()
