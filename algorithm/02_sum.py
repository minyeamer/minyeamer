# 리스트 원소의 합 구하기
# n개의 원소를 가진 리스트 S의 원소의 합 구하기


def sum(n, S):
    result = 0
    for i in range(1, n + 1):
        result += S[i]
    return result


S = [-1, 10, 7, 11, 5, 13, 8]
print('sum =', sum(len(S)-1, S))
