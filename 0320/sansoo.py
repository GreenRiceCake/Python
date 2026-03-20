import random

x = random.randint(1, 100)
y = random.randint(1, 100)

answer = int(input(f"{x} + {y} ="))

flag = (answer == x + y)
print(flag)