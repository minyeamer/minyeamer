oddnumber = [1, 3, 5, 7, 9]
cafes = ['star', 'bene', 'yoger', 'friends']
A = [1, 5, 'A', 'CC', 'B']
listInList = [[1, 3, 5, 6, 7], cafes, oddnumber, 1, 3, 'Abc']

print(oddnumber)
print(cafes)
print(A)
print(listInList)

#

oddnumber = [1, 3, 5, 7, 9]
cafes = ['star', 'bene', 'yoger', 'friends']
A = [1, 5, 'A', 'CC', 'B']
listInList = [[1, 3, 5, 6, 7], cafes, oddnumber, 1, 3, 'Abc']

a = oddnumber[3]
b = cafes[1]
c = A[2]
d = listInList[0][1]  # 리스트 내 리스트 접근

print(a)
print(b)
print(c)
print(d)
print(a + d, oddnumber[4] * listInList[4])  # 숫자 + 숫자 연산 가능
print(b + c)  # 문자열 + 문자열: 문자열 합하기

#

oddnumber = [1, 3, 5, 7, 9]
cafes = ['star', 'bene', 'yoger', 'friends']
A = [1, 5, 'A', 'CC', 'B']
listInList = [[1, 3, 5, 6, 7], cafes, oddnumber, 1, 3, 'Abc']

a = oddnumber[1:5]
b = cafes[1:]
c = A[:2]
d = listInList[0][1:4]  # 리스트 내 리스트 접근

print(a)
print(b)
print(c)
print(d)

#

evennumbers = [2, 4, 6, 8, 10]
oddnumbers = [1, 3, 5, 7, 9]

numbers = evennumbers + oddnumbers
print(numbers)
print(numbers * 4)

#

numbers = [2, 4, 6, 8, 10, 1, 3, 5, 7, 9]

numbers[4] = 100
print(numbers)

numbers[2] = "hello"
print(numbers)

numbers[0] = numbers[9]  # 인덱스 9를 인덱스 0에 대입
print(numbers)

numbers[8] = ['a', 'b', 'c']  # 리스트 전체를 형태 유지하며 대입
print(numbers)

#

numbers = [2, 4, 6, 8, 10, 1, 3, 5, 7, 9]

numbers[4:5] = [80]
print(numbers)

numbers[2:6] = "hello"
print(numbers)

numbers[2:3] = ['a', 'b', 'c']
print(numbers)

numbers[8] = ['a', 'b', 'c']  # 리스트 전체를 형태 유지하며 대입
print(numbers)

numbers[:] = [1]
print(numbers)

#

numbers = [2, 4, 6, 8, 10, 1, 3, 5, 7, 9]

# 값만 삭제
numbers[3] = ""
print(numbers)

#

numbers = [2, 4, 6, 8, 10, 1, 3, 5, 7, 9]

a = "goorm"

# 공간까지 삭제
del numbers[4]
print(numbers)

del numbers[:5]
print(numbers)

# 객체 자체를 삭제
del a

#

numbers = [2, 4, 6, 8, 10, 1, 3, 5, 7, 9]
print(numbers)

numbers.insert(3, [11, 12, 13])
print(numbers)

# append와 extend의 차이
numbers.extend(['a', 'b', 'c'])
print(numbers)
numbers.append(['a', 'b', 'c'])
print(numbers)

#

numbers = [2, 4, 6, 8, 1, 3, 5, 7]
print(numbers)

numbers.insert(3, [11, 12, 13])
print(numbers)

numbers.remove(3)
print(numbers)
print(numbers.pop())
print(numbers)

#

evennumbers = [2, 4, 6, 8]
oddnumbers = [1, 3, 5, 7]
print(evennumbers, oddnumbers)

numbers = evennumbers + oddnumbers
print(numbers)

numbers.sort()
print(numbers)

numbers.reverse()
print(numbers)

#

numbers = [1, 6, 7, 3, 5, 6, 8, 3, 3]

numbers.index(6)
print(numbers)
print(numbers.count(3))

#

list1 = [2, 5, 2, 0, 1]
list2 = [4, 1, 2]

list1.append(list2)
print(list1, len(list1))

#

# 빈 리스트 생성 후 값 초기화 불가능
# drawer = []
# drawer[0] = "양말"

drawer = []

drawer.append("양말")
print(drawer, drawer[0])

drawer.extend(["속옷", "모자", "반팔", "바지"])
print(drawer)
