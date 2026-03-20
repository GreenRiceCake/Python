num = int(input("Enter a number: "))

fact = 1

print(num, end="! = ")
for i in range(num, 0, -1):
    fact *= i
    if i > 1:
        print(i, end=" * ")
    else :
        print(i, end=" = ")

print(fact)
