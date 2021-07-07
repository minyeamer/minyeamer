# exception
# 에러 메시지 대신 devision by zero 메시지 출력
try:
  10 / 0
except ZeroDivisionError as e:
  print(e)

# else
# 정상적인 연산 시 에러 메시지가 아닌 문자열 출력
try:
  10 / 2
except ZeroDivisionError as e:
  print(e)
else:
  print("Success!")

# finally
# try 문이 수행된 후 예외 발생 여부와 관계 없이 실행
try:
  10 / 0
except ZeroDivisionError as e:
  print(e)
else:
  print("Success!")
finally:
	print("ZeroDivisionError Check")

# 오류 회피
try:
  10 / 0
except ZeroDivisionError:
  pass

# 오류 발생
try:
  raise NameError
except NameError:
  print("NameError occurred")
