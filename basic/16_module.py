import random

a = random.random()
b = random.randrange(1, 10)
c = ['a', 'b', 'c', 'd']
d = random.choice(c)

#

import calcultor

add_result = calculator.add(10,2)
sub_result = calculator.sub(10,2)
mul_result = calculator.mul(10,2)
div_result = calculator.div(10,2)
mod_result = calculator.mod(10,2)

print(add_result)  #=> 12
print(sub_result)  #=> 8
print(mul_result)  #=> 20
print(div_result)  #=> 5
print(mod_result)  #=> 0

#

# import my_module

# print(my_module.three_times(10)) #=> 30
# print(my_module.ten_times(10)) #=> 100

#

from my_module import three_times
from my_module import ten_times
# 또는 from 모듈 이름 import *

print(three_times(10)) #=> 30
print(ten_times(10)) #=> 100
