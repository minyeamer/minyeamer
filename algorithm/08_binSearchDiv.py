# 정렬되지 않은 리스트 - 순차 탐색
# 정렬된 리스트 - 이분 검색

# 이분 검색: 분할정복(Divide-and-Conquer)
# 문제: 정렬된 리스트 S에 어떤 키 x가 존재하는가?
# 해답: 존재하면 S에서 x의 위치, 아니면 -1을 리턴

# 알고리즘: 분할정복
# S의 정가운데 원소와 x를 비교하여 같으면 해당 위치를 리턴, 아니면:
# [Divide] 정가운데 원소를 기준으로 S를 두 개의 리스트로 분할
# [Conquer] x가 정가운데 원소보다 크면 오른쪽, 작으면 왼쪽을 재귀 호출
# [Obtain] 선택한 리스트에서 얻은 답을 리턴


def location(S, low, high):
    if(low > high):
        return 0
    else:
        mid = (low + high) // 2
        if(x == S[mid]):
            return mid
        elif(x < S[mid]):
            return location(S, low, mid - 1)
        else:
            return location(S, mid + 1, high)


S = [-1, 10, 12, 13, 14, 18, 20, 25, 27, 30, 35, 40, 45]
x = 18

loc = location(S, 1, len(S) - 1)
print('S =', S)
print('x =', x)
print('loc =', loc)
