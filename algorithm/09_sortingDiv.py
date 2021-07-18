# 합병 정렬: 분할정복
# [Divide] 원소가 n개인 S를 n/2개의 원소를 가진 두 개의 리스트로 분할
# [Conquer] 왼쪽의 리스트와 오른쪽의 리스트를 각각 재귀적으로 합병 정렬
# [Combine] 각각 정렬된 두 개의 리스트를 정렬된 하나의 리스트로 합병하여 리턴


def mergesort(S):
    n = len(S)
    if(n <= 1):
        return S
    else:
        mid = n // 2
        U = mergesort(S[0:mid])
        V = mergesort(S[mid:n])
        return merge(U, V)

def merge(U, V):
    S = []
    i = j = 0
    while(i < len(U) and j < len(V)):
        if(U[i] < V[j]):
            S.append(U[i])
            i += 1
        else:
            S.append(V[j])
            j += 1
    if(i < len(U)):
        S += U[i:len(U)]
    else:
        S += V[j:len(V)]
    return S


S = [27, 10, 12, 20, 25, 13, 15, 22]
print('Before: ', S)
X = mergesort(S)
print(' After: ', X)
