# 튜플은 생성 후 수정이 불가능

x = 100, 200, 300
print(x)
print(type(x))
print()

animals = ('dog', 'cat', 'lion')
print(animals)
print(animals[0])
print(animals[1:])
print()

print(animals.index('cat'))
animals = ('dog', 'cat', 'dog', 'hamster', 'dog')
print(animals.count('dog'))

# 튜플의 요소는 삭제가 안되지만 튜플 자체 삭제는 가능
# del animals[1]
del animals
