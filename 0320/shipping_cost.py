price = int(input("상품의 가격을 입력하세요: "))

if price > 20000 :
    cost = 0
else :
    cost = 3000

print("상품의 가격: ", price, "\n배송비: ", cost)