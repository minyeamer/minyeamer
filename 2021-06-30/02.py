# Set은 입력한 순서대로 저장하지 않음, 중복 허용 안함

animals = {'dog', 'cat', 'hamster', 'dog'}
print(type(animals))
print(animals)
print()

animals = {'dog', 'cat'}
animals.add('hamster')
animals.add('lion')
print(animals)
print()

animals.update({1, 2, 3})
print(animals)
print()

animals.remove('hamster')
print(animals)
print()

nums = {1, 2, 3, 4}
print(nums)
nums.clear()
print(nums)
print()

strName = 'HongKilDong'
print(type(strName))
print(strName)
strName = set(strName)
print(type(strName))
print(strName)
