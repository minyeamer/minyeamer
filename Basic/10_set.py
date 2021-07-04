s1 = {3, 2, 5, 1, 8, 4, 3}  # 집합으로 바로 선언 및 초기화
print(s1, type(s1))

#

str = "Hello goorm!!!"
print(str, type(str))

s0 = set(str)
print(s0, type(s0))

l1 = ['a', 'a', 'c', "goorm", "hello", 10, 30, 30]
print(l1, type(l1))

s1 = set(l1)
print(s1, type(s1))

d = {"Anna": 25, "Bob": 23}
print(d, type(d))

s2 = set(d)
print(s2, type(s2))

t = (190,)
print(t, type(t))

s3 = set(t)
print(s3, type(s3))

#

str = "Hello goorm!!!"
print(str, type(str))

s0 = set(str)
print(s0, type(s0))

newstr = tuple(s0)
print(newstr, newstr[4], newstr[5:], type(newstr))  # 인덱싱, 슬라이싱 가능

l1 = [1, 2, 3, 4, 5, 6, 7, 8]
print(l1, type(l1))

s1 = set(l1)
print(s1, type(s1))

newlist = list(s1)
print(newlist, newlist[4], newlist[:-5], type(newlist))

#

s1 = set([2, 4, 6, 8, 10])
s2 = set([1, 2, 3, 4, 5, 6, 7, 8])

interset = s1 & s2  # 교집합
print(interset)
print(s1.intersection(s2), s2.intersection(s1))  # 함수 사용
print(s1)  # s1의 값이 바뀌는 것이 아님

uniset = s1 | s2  # 합집합
print(uniset)
print(s1.union(s2))
print(s1)  # s1의 값이 바뀌는 것이 아님

difset1 = s1 - s2  # 어떤 집합에서 어떤 집합을 빼느냐에 따라 다른 결괏값
difset2 = s2 - s1
print(difset1)
print(difset2)

#

s1 = {1, 2, 3, 4}

s1.add("hello")
print(s1)

s1.add(10)
print(s1)

s1.add((1, 2, 3))  # add() 사용 시 튜플/문자열은 값 하나로 인식
print(s1)


s1.update(['a', 'b', 'c'])  # set()과 같이 여러 값을 한 요소로 저장
s1.update((11, 12))
print(s1)

s1.update("zyx")  # s1.add("hello")와의 차이
print(s1)

s1.remove("hello")  # 하나의 값만 제거 가능
print(s1)
