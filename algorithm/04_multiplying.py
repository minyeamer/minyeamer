# 행렬의 곱셈
# 두 n x n 행렬의 곱을 구하시오
# C = A x B, c_ij = a_ik*b_kj + ... , k = n


def matrixMult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]  # [0]을 n번 곱하여 n차원 리스트 생성
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


A = [[2, 3], [4, 1]]
B = [[5, 7], [6, 8]]
print('C =', matrixMult(A, B))
