hobbies = ['reading', 'musig', 'movie']
print(type(hobbies))

hobbies = [100, 3.141592, 'reading']
print(hobbies)
print()

animals = ['lion', 'tiger', 'rabbit']
print(animals[0])
print(animals[1])
print(animals[2])
print()

print(animals[1:])
print(animals[0:len(animals)])
print(animals[-1])    # 맨 마지막
print(animals[-3])
print(animals[0:-1])    # 맨 마지막 전까지
print()

animals[1] = 'cat'
print(animals)
animals.append('dog')
print(animals)
del animals[1]
print(animals)
animals.insert(2, 'pig')
print(animals)
print()

animals.append(3)
animals.append('3.14')
print(animals)
print(type(animals[4]))
print(type(animals[5]))
print()

del animals[3:]
print(animals)
print()

print(animals.pop(2))
print(animals)
animals.append('pig')
print()

animals.append('lion')
print(animals)
animals.remove('lion')    # 1번째 요소만 삭제
print(animals)
print()

animals.clear()
print(animals)
