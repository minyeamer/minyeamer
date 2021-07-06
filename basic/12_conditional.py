# for jump_count in range(20):
#     if jump_count % 2 == 0:
#         print("쌩쌩이를 하고 줄넘기를 %d회 했습니다." % jump_count)
#     else:
#         print("줄넘기를 %d회 했습니다." % jump_count)

#

# num = int(input("1부터 4까지 정수를 입력하세요:"))

# if num == 4:
#     print("4를 입력했습니다.")
# elif num == 3:
#     print("3을 입력했습니다.")
# elif num == 2:
#     print("2을 입력했습니다.")
# elif num == 1:
#     print("1을 입력했습니다.")
# else:
#     print("잘못 입력했습니다.")

#

# if "" :							#False
#     print("빈칸")
# elif " " :						#True
#     print("공백")

# if [1,2,3] :					#True
#     print("리스트")
# elif [] :						#False
#     print("빈리스트")
    
# if 0 :							#False
#     print("0")
# elif 1 :						#True
#     print("1")

#

# money = int(input("가지고있는 금액을 입력하세요:"))

# if money >= 5000 :
#     print("택시를 탈 수 있습니다.")
# elif money < 5000 and money >= 2000 :
#     print("버스를 탈 수 있습니다.")
# else :
#     print("걸어가야 합니다.")

#

# l = [10, 20, 30, 'a', 'b', 'c', "hello"]

# if 20 in l :
#     print("요소가 존재합니다.")
# else :
#     print("요소가 존재하지 않습니다.")
    
# if "Hello" not in l :
#     print("요소가 존재하지 않습니다")
# else :
#     print("요소가 존재합니다.")

#

# num = int(input("입력할 단어 개수를 입력하세요:"))
# wordslist = []

# for i in range(num) :
#     word = input("단어를 입력하세요:")
#     wordslist.append(word)

# for w in wordslist :
#     print(w, end = ' ')   

#

# wordslist = []

# while True :
# 	word = input("단어를 입력하세요. 1 입력시 중단됩니다.:")
# 	if word == "1" :
# 		break
# 	else :
# 		wordslist.append(word)

# for w in wordslist :
# 	print(w, end = ' ')

#

nums = []

while True :
	num = int(input("숫자를 입력하세요. -1 입력시 중단됩니다.:"))
	if num == -1 :
		break #반복문 탈출
	else :
		if num % 2 == 1 :
			continue #반복문 맨 처음으로
		nums.append(num)
		
for n in nums:
	print(n, end = ' ')
