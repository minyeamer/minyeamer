# 이진 탐색


def binsearch(n, S, x):
    low = 1
    high = n
    location = 0
    while (low <= high and location == 0):
        mid = (low + high) // 2
        print(low, high, mid)
        if(x == S[mid]):
            location = mid
        elif(x < S[mid]):
            high = mid - 1
        else:
            low = mid + 1
    return location


S = [-1, 5, 7, 8, 10, 11, 13]
# x = 2
# x = 7
x = 13
loc = binsearch(len(S) - 1, S, x)
print('S =', S)
print('x =', x)
print('loc =', loc)


# 순차 탐색과 이분 검색 알고리즘의 효율성 비교
# 순차 탐색: 크기가 n인 리스트에서 n번의 비교를 수행
# 이분 검색: 크기가 n인 리스트에서 lgn + 1번의 비교를 수 행
# 리스트의 크기가 128일 때 순차 탐색은 128번 비교, 이분 검색은 8번 비교
