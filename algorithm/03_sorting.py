# 리스트의 정렬
# n개의 수로 구성된 리스트 S를 비내림차순으로 정렬
# 교환 정렬, 삽입 정렬, 선택 정렬, 합병 정렬, 퀵 정렬 등

# 교환 정렬
# i번째 자리에 있는 수와 (i+1)번째부터 n번째 자리에 있는 수를 차례대로 비교
# 주어진 자리의 수가 i번째 자리에 있는 수보다 작은 경우 두 수를 교환


def sort(S):
    n = len(S)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if(S[i] > S[j]):
                S[i], S[j] = S[j], S[i]
    return S


S = [-1, 10, 7, 11, 5, 13, 8]
print('Before =', S)
sort(S)
print('  Afer =', S)
