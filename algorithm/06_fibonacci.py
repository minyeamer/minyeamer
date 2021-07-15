# 피보나치 수열
#
# 피보나치수열의 재귀적 정의
# f_0 = 0, f_1 = 1
# f_n = f_n-1 + f_n-2, (n>=2)
#
# 문제: 피보나치 수열의 n번째 항을 구하시오
# 알고리즘: 재귀적 정의를 그대로 구현


def fib(n):
    if (n <= 1):
        return n
    else:
        return fib(n - 1) + fib(n - 2)


for i in range(11):
    print(fib(i), end=" ")
print()


# 재귀적 정의는 비효율적 (같은 값을 중복해서 계산)
# 개선: 이미 계산한 피보나치 항의 값을 리스트에 저장하여 꺼내씀


def fib2(n):
    f = [0] * (n + 1)
    if(n > 0):
        f[1] = 1
        for i in range(2, n + 1):
            f[i] = f[i - 1] + f[i - 2]
    return f[n]


for i in range(11):
    print(fib2(i), end=" ")
print()


# 연습문제
# 리스트 f를 사용하지 않고 반목문으로 피보나치 항을 구하시오

def fib3(n):
    a, b = 0, 1
    if(n <= 1):
        return n
    else:
        while(n):
            a, b = b, a + b
        return n


for i in range(11):
    print(fib2(i), end=" ")
print()
