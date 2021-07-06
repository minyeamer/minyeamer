# 계산기
'''
nums = input("두 수를 띄어쓰기로 입력하세요:").split()
nums = list(map(int, nums)) #nums의 요소를 한 번에 int로 변환
result = 0
cal = input("""
1. +
2. -
3. *
4. /
""")

if cal == "1":
    result = nums[0] + nums[1]
elif cal == "2":
    result = nums[0] - nums[1]
elif cal == "3":
    result = nums[0] * nums[1]
elif cal == "4":
    result = nums[0] / nums[1]
else :
    print("잘못된 입력입니다.")    
print(result)
'''

# map 함수는 리스트, 문자열 등에 포함된 요소를 한 번에 연산/함수 처리

def func(a) :
    return a + 1

nums = [1,2,3,4,5]	# 집합인자(튜플, 리스트, 문자열) 모두 가능
nums = list(map(func, nums)) # map(함수, 집합인자, ..) 형태
print(nums)

# 파일 열기: 파일 객체 이름 = open("파일 경로/파일 이름", "파일 열기 모드")
# 파일 닫기: 파일 객체.close()

# 파일 열기 모드
# 읽기 모드 (r), 쓰기 모드 (w), 추가 모드 (a)
# 쓰기 모드로 열 경우 기존 내용이 삭제 > 기존 파일에 입력 시 추가 모드 사용

# f = open("test.txt", 'r')
# f.close()

# f = open("test.txt", 'w')
# f.write("hello")
# f.close()

# f = open("test.txt", 'w')

# for i in range(1, 11) :
#     sentence = "%d번째 줄입니다." %i
#     f.write(sentence)
    
# f.close()

# 파일 읽기
# readline(): 파일 객체의 한 줄씩 읽고 그 문자열을 반환
# readlines(): 파일 객체의 모든 줄을 읽고 각 줄을 리스트로 반환
# f.read(): 파일 객체의 모든 문자열을 읽고 반환

# f = open("test.txt", 'w')
# for i in range(1, 11) :
#     sentence = "%d번째 줄입니다.\n" %i
#     f.write(sentence)
# f.close()

# a = open("test.txt", 'r')
# for i in range(1,11) :
#     data = a.readline() #파일을 닫기 전까지 한 줄 읽고
#     print(data) #한 줄 출력
# a.close()

# f = open("test.txt", 'w')
# for i in range(1, 11) :
#     sentence = "%d번째 줄입니다.\n" %i
#     f.write(sentence)
# f.close()

# a = open("test.txt", 'r')
# while 1 :
#     line = a.readline()
#     if not line : break #line이 None이 되면(=false) 반복문 탈출
#     print(line)
# a.close()
