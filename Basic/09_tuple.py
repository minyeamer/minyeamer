t1 = ('a', 'b', 'c', 1, 2, 3)
print(t1, t1[2])

t2 = ("hello",)  # 하나의 값이면 뒤에 콤마 입력
print(t2)

t3 = "goorm", 'b', "hello", 1, 2, 3  # 괄호 생략 가능
print(t3, t3[2])

s1 = list(set([1, 2, 3]))  # 다음에 배우게 될 집합 Mutable 타입
t4 = ([1, 2, 3], {"사과": "apple", "포도": "grape"}, ('a', 'b', 'c'), s1)
# 리스트 내 어떤 값도 가능
print(t4, t4[1])

t4[3][2] = "edit"  # 중요: 튜플 요소가 Mutable하면 수정할 수 있음
t4[1]["사과"] = "edit"
t4[0][2] = "edit"
print(t4)

#

t1 = ('a', 'b', 'c', 1, 2, 3)
t2 = ("hello",)
t3 = "goorm", 'b', "hello", 1, 2, 3

print(t1 + t2 + t3)  # 튜플 결합
print(t2 * t3[4])  # 곱셈으로 반복 출력

#

t = (13, 6, 9)
print(t)
print(t.index(13), t.count(6))
