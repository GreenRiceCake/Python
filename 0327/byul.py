number = int(input("숫자를 입력하세요 : "))

for i in range(1, number+1):
    print(" "*(number-i),("*"*i)+("*"*(i-1)))

for i in range(number-1, 0, -1):
    print(" "*(number-i),("*"*i)+("*"*(i-1)))