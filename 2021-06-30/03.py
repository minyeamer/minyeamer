# dictionary 내에 중복된 키가 존재하면 안됨

books = {'design': 10000, 'programming': 20000, 'os': 30000}
print(books)
print(type(books))
print()

print(books['os'])
print(books['design'])
print()

# keys() 등 함수는 list로 묶어서 객체(dict_keys 등)으로 반환
# items() 함수는 key와 value의 한 쌍을 튜플로 묶어서 list로 반환

print(books.keys())
print(books.values())
print(books.items())
print()

print(list(books.keys()))
print(list(books.keys())[0])
print()

print(list(books.items())[0])
print(type(list(books.items())[0]))
print()

dict_sample = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
print(dict_sample)
dict_sample['e'] = 5
print(dict_sample)
print()
