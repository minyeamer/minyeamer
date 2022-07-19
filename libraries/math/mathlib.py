import numpy as np


def pprint(msg: str, A: np.ndarray):
    print(f'[ {msg} ]')
    A[np.where(A == -0.)] = 0.
    for row in A:
        [print(f'{s:.3f}', end='\t') for s in row[:-1]]
        print(f'| {row[-1]:.3f}')
    print()


def gauss(A: np.ndarray, start=0):
    (n,m) = A.shape

    for i in range(start, n):
        if np.all(A[i:,i] == 0):
            gauss(A, i+1)
            print('There are infinite number of solutions')
            return A[:,-1]

        max_row = abs(A[i:,i]).argmax()
        if max_row != 0:
            A[[i,max_row+i]] = A[[max_row+i,i]]
            pprint(f'{i+1}행과 {max_row+i+1}행을 교환: R{i+1} ↔ R{max_row+i+1}', A)

        pivot = A[i,i]
        A[i] = A[i]/pivot
        pprint(f'{i+1}행 {i+1}열 피벗을 1로 변환: R{i+1} ← ( {1} / {pivot:.3f} ) * R{i+1}', A)

        for k in range(n):
            if (k != i) and (A[k,i] != 0):
                c = A[k,i]*-1
                A[k] = A[k]+(A[i]*c)
                pprint(f'{k+1}행 {i+1}열 성분을 0으로 변환: R{k+1} ← ( {c:.3f} * R{i+1} ) * R{k+1}', A)

    return A[:,-1]
