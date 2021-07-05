# engdic = {
#     "apple": "사과",
#     "book": ["책", "예약하다"],
#     "grape": "포도",
#     "while": "~하는동안에"
# }

# inputword = input("검색할 영어 단어를 입력하세요:")
# ...

#

# count = 0
# while count != 100:						# while범위시작
#     print("Hello goorm!", count)
#     count += 1							# while범위끝

#

# jump_count = 0  # 줄넘기 횟수 설정

# while jump_count != 20:
#     jump_count += 1
#     print("줄넘기를 %d회 했습니다." % (jump_count))

#

# jump_count = 0

# while True:  # 계속 Ture이기 때문에 멈추지 않음
#     jump_count += 1
#     print("줄넘기를 %d회 했습니다." % (jump_count))

num = 1
total = 0

while num <= 10:
    total += num
    num += 1

print(total)

#

evennumbers = []  # 빈 리스트 생성
num = 2

while num <= 30:
    evennumbers.append(num)
    num += 2

print(evennumbers)

#

# 콘솔 입력으로 문자열을 받은 뒤 정수로 변환
# inputnum = int(input("양의 정수를 입력하세요:"))
# num = 0

# while num < inputnum:
#     print("Python", num)
#     num += 1

#

# for i in range(0, 10, 1):
#     print(i)

#

# i = 0

# while i < 10:
#     print(i)
#     i += 1

#

# for num in range(10):
#     print(num)

# for a in range(4, 8):
#     print("<%d>" % a)

#

# dic = {"human": "사람", "dog": "강아지", "carrot": "당근"}

# oddnums = (1, 3, 5, 7, 9)
# evennums = [6, 8, 10, 22, 50]
# str = "Hello goorm!"

# for i in oddnums:
#     print(i, end = ' ')
# print()

# for i in evennums:
#     print(i, end = ' ')
# print()

# for i in str:
#     print(i , end = ' ')
# print()

# for key, val in dic.items():
#     print(key, val, end = ' ')
# print()

#

# for num in [1,2,3,4,5,6,7] :
#     print(num)

# for num in [1,2,3,4,5,6,7] :
#     print(num, end = ',')

# nums1 = [[1, 2, 3], [4, 5, 6], ['a', 'b', 'c']]
# nums2 = [(1,2), (3, 4)]

# for i, j, k in nums1 :
#     print(i, j, k)

# print()

# for i, j in nums2 :
#     print(i, j)

fruits = {"apple": "red", "banana": "yellow", "grape": "purple", "melon": "green"}

for color in fruits.values():
    print(color, end=' ')
print()

for fruit in fruits.keys():
    print(fruit, end=' ')
print()

for fruit, color in fruits.items():
    print("%s의 색은 %s" % (fruit, color), end=', ')


