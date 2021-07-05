dic1 = {"apple": "사과", "bird": "새", "bug": "벌레"}
print(dic1)

dic2 = dict(apple="사과", bird="새", bug="벌레")
print(dic2)

#

dic = {}

dic["apple"] = "사과"
dic["grape"] = "포도"
dic["fruits"] = ["바나나", "딸기", "오렌지"]
print(dic)

#

dic1 = {"apple": "사과", "bird": "새", "bug": "벌레"}
print(dic1)

del dic1["bug"]
print(dic1)

#

# 중복 저장 되지 않고 "num" : 4로 수정
dic = {"num": 3}
dic["num"] = 4

# dic[[1]] = True -> 리스트는 key로 저장할 수 없음
dic[False] = 0

# value는 어느 값이든 저장 가능
dic[True] = [1, 10, 100]
dic["nums"] = {"one": 1, "two": 2}
print(dic)

#

mem = {"김구름": 25, "박에듀": 23, "온라인": 24}
mem = {"김구름": 25, "박에듀": 23, "온라인": 24}
print(mem.keys())
names = list(mem.keys())  # 새로운 리스트 변수에 초기화

names.append("윤레벨")
print("새로운 리스트", names)
print("원래 딕셔너리에서 key 모음", list(mem.keys()))
print(mem.values())
print(list(mem.values()))
print("key와 value를 튜플로", mem.items())
print(mem.get("정판교", "없습니다"), mem.get("온라인", "없습니다"))

exist = '박에듀' in mem  # 굉장히 직관적인 용법
print(exist)

exist = '한바로' in mem
print(exist)

mem.clear()
print(mem)  # 빈 딕셔너리 출력
