str1 = "Hello"
str2 = "goorm: !@#$%^&*()\|/"
str3 = "3"
print(str1, str2, str1 + str3)

#

str1 = 'He said "I love you"'
str2 = "It's so beautiful"
str3 = """My name is "goorm" """
str4 = '''It's an apple'''

print(str1)
print(str2)
print(str3)
print(str4)

#

str1 = "한 눈에 읽는\n파이썬3"
str2 = '설치가 필요없는 클라우드 IDE, 구름IDE'
str3 = '''이스케이프 시퀀스를
배워봅시다.'''
str4 = """한 눈에 읽는
파이썬3"""

print(str1)
print(str2)
print(str3)
print(str4)

#

str1 = "한 눈에 읽는\n파이썬3"
str2 = '설치가 필요없는 클라우드 IDE, \n구름IDE'
str3 = '''이스케이프 시퀀스를\n배워봅시다.'''
str4 = """한 눈에 읽는\nPython3"""

print(str1)
print(str2)
print(str3)
print(str4)

#

str1 = "Hello "
str2 = "goorm!"
result = str1 + str2
print(result)

#

str = "Hello "
num = 5
result = str * num
print(result)

#

print(ord("A"))
print(chr(65))

#

str = "apple"
print("str의 첫 번째 문자는", str[0], "네 번째 문자는", str[3])

#

a = "Hello goorm!"
b = a[4] + a[5] + a[6]
print(a[0], a[1], a[2], a[3], a[4])
print(b)

#

a = "Hello goorm!"
b = a[-1] + a[-2] + a[-3]
c = a[-0]
print(b)
print(c)

# 문자열의 각 문자는 바꿀 수 없음 ex) str[2] = "u"가 불가

a = "Hello goorm!"
b = a[0:5]
print(b)

#

a = "Hello goorm!"

b = a[:5]
c = a[5:]
print(b)
print(c)

#

a = "Hello goorm!"

b = a[0:-5]
c = a[6:-11]
print(b)
print(c)

#

city = "seoul"
today = 12
day = "화요일"
temperature = 26

#정수형 temperature은 문자열과 덧셈 불가 -> str(문자열)로 형변환	
announcement = city + "의 " + "12" + "일 " +day + " 기온은 " + "26" + "도 입니다."

#1번 방법
print(city,"의",today,"일",day,"기온은",temperature,"도 입니다.")
#2번 방법
print(announcement)


#

city = "seoul"
today = 12
day = "화요일"
temperature = 26
announcement = "%s의 %d일 %s 기온은 %d도 입니다." %(city, today, day, temperature)
	
print("%s의 %d일 %s 기온은 %d도 입니다." %(city, today, day, temperature)) #1번 방법
print(announcement) #2번 방법

#

name = "goorm"
age = 25
height = 181.523456

print("저의 이름은 %s입니다." %name)

print("저는 %d살입니다." %25)
print("제 나이는 %d살입니다." %age)
print("제 나이는 %s살입니다." %age)
print("제 나이는 %.2f살입니다." %age)

print("저의 키는 %fcm입니다." %height)
print("저의 키는 %.2fcm입니다." %height)
print("저의 키는 %dcm입니다." %height)

print("저의 성은 '%c'입니다." %"남")

print("저의 나이는 16진수로 표현하면 %x, 8진수로 표현하면 %o입니다." %(age, age))

print("%10d %010d" %(10, 10))
	
#'김구름'을 포함하여 8칸의 공간 발생 -> 공백 5칸 + 김구름 3칸
print("%8s %8d %8s" %("김구름", 6, "컴퓨터공학"))
print("%-8s %-8d %-8s" %("김구름", 6, "컴퓨터공학"))

#

name1 = "김구름"
name2 = "박에듀"
age = 25
height = 181.123
print("저의 이름은 {2}입니다. 그리고 나이는 {1}살이고 키는 {0}cm입니다.".format(height, age, name1))
print("{1}의 나이:{0}, {2}의 나이: {0}".format(age, name1, name2))

#

print("저의 이름은 {1}입니다. 그리고 나이는 {age}살이고 키는 {0}cm입니다. 제 가장 친한 친구는 {name}입니다.".format(181.12, "김구름",height = 181.123, age = 25, name = "박에듀"))

#

print("{length: >10d}".format(length = 30))
# 공백문자: (공백) ,정렬: 오른쪽 정렬, 폭: 10
# 순서대로 입력해야하고 생략 가능

print("{0:0^10}".format("goorm"))
# 공백문자: 0 ,정렬: 가운데 정렬, 폭: 10
# 순서대로 입력해야하고 생략 가능

print("{height:!>13.2f}".format(height = 181.24363))
# 공백문자: ! ,정렬: 오른쪽 정렬, 폭: 13, 소수점 2자리 표시
# 순서대로 입력해야하고 생략 가능

#

name = "김구름"
age = 25
height = 181.123
print(f"저의 이름은 {name}입니다. 그리고 나이는 {age+10}살이고 키는 {height:!^10.2f}cm입니다.")

#

str = " Hello goorm! I study Python.  "

num = str.count(' ') #빈칸의 개수
print("빈칸의 개수는 %d입니다." %num)
print("처음 등장하는 'l'의 인덱스 값은 %d입니다." %str.find('l')) 
print("Good day에서 처음 등장하는 'y'의 인덱스 값은 %d입니다." %"Good day".index('y'))

print(" ".join(str))
print(str.upper())
print(str.lower())
print(str.lstrip())
print(str.rstrip())
print(str.replace('Python', 'C'))
print(str.split())

#

sentence = "I like studying Python" 
print(len(sentence), len("goorm"))
