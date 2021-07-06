#함수 선언
# def plusThree(num) :
#     return num + 3

# #함수 호출
# result = plusThree(10)

# print(result)

#

#함수 선언
# def stdInfo(rrn) :
#     if int(rrn[6]) == 3 or int(rrn[6]) == 4 :
#         biryear = int(rrn[0]+rrn[1]) + 2000
#     else :
#         biryear = int(rrn[0]+rrn[1]) + 1900
    
#     age = year - biryear + 1
#     birmonth = int(rrn[2] + rrn[3])
#     birday = int(rrn[4] + rrn[5])
    
#     if rrn[6] == "2" or rrn[6] == "4" :
#         gen = "여자"
#     else :
#         gen = "남자"
        
#     return [age, birmonth, birday, gen] #리스트 형식으로 반환

# year = 2018
# stdlist = []

# stdrrn = input("학생의 주민등록번호를 7자리 입력하세요:")

# stdlist.append(stdInfo(stdrrn)) #함수 호출

# print(stdlist[0])

#

# def guide() : #매개변수 X, 반환값 X
#     print("두 정수를 입력받아 곱한 결과를 출력하는 프로그램입니다.")
    
# def inputnums() : #매개변수 X, 반환값 O
#     a = int(input("첫번째 정수를 입력하세요:"))
#     b = int(input("두번째 정수를 입력하세요:"))
#     return a, b

# def multi(num1, num2) : #매개변수 O, 반환값 O
#     return num1 * num2
    
# def printResult(result) : #매개변수 O, 반환값 X
#     print("두 수의 곱셈 결과는 %d입니다." %result)
    
# guide()
# n1, n2 = inputnums() #반환 값이 두 개이니 두 변수에 초기화
# res = multi(n1, n2)
# printResult(res)

#

# def subNums(*t) :
#     print(t, type(t)) #튜플인지 확인
#     total = 0
    
#     for i in t :
#         total = total + i
    
#     return total

# print(subNums(1, 5, 32, 3, 4, 57, 5))
# print(subNums(5, 29))

#

# def calNums(ch, *t) :
#     if ch == "sum" : #모든 값을 더합니다.
#         total = 0
#         for i in t :
#             total = total + i

#     elif ch == "mul" :	#모든 값을 곱합니다.
#         total = 1
#         for i in t :
#             total = total * i

#     else :
#         print("실행할 수 없습니다.")
        
#     return total
    
# choice = input("덧셈은 sum, 곱셈은 mul를 입력하세요:")
# print(calNums(choice, 1, 2, 3, 2, 5, 3, 2))  

#

# def func(**kwargs) :
#     print(kwargs)
    
# num = 10
# func(apple="사과", a = num, num = 4)

#

# def func(*nums, **kwargs) :
#     print(nums)
#     print(kwargs)
    
# num = 10
# func(1, 3, 5, 7, apple="사과", a = num, num = 4)

#

def calculator(a, b) :
    sum = a + b
    sub = a - b
    mul = a * b
    div = a / b
    return [sum, sub, mul, div]

reslist = calculator(10, 2)
print(reslist)

# 반환값이 여러개면 자동으로 튜플

def calculator(a, b) :
    sum = a + b
    sub = a - b
    mul = a * b
    div = a / b
    return sum, sub, mul, div

reslist = calculator(10, 2)
print(reslist, type(reslist))

#

def division(a, b) :
	if b == 0 :
		return
	else :
		res = a / b
		
	print("division")
	return res

result = division(10, 3)
print(result)

result = division(10, 0)
print(result)

#

num = 1 #전역변수 선언

def plusNum() :
	global num #전역변수를 함수 내에서 사용함을 선언
	num += 1
	print(num)

plusNum()
print(num)
