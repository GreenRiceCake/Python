def facto(n):
    fact = 1
    print(n, end="! = ")
    for i in range(n, 0, -1):
        fact *= i
        if i > 1:
            print(i, end=" * ")
        else:
            print(i,"=", fact)

    return fact 
    
inp = eval(input("정수를 입력하시오."))
facto(inp)