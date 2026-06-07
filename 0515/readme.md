## 8. 객체와 클래스

객체지향 프로그래밍에서는 데이터와 기능을 하나로 묶어 객체로 표현합니다.  
클래스는 객체를 만들기 위한 설계도입니다.

```python
class Car:
    def __init__(self, model, color):
        self.model = model
        self.color = color
        self.speed = 0

    def speed_up(self):
        self.speed += 10
```

`__init__()`은 객체가 생성될 때 자동으로 실행되는 생성자입니다.  
`self`는 객체 자기 자신을 의미합니다.

클래스를 통해 자동차, 사람, 원, TV 같은 객체를 만들어 보며 속성과 메서드의 개념을 익혔습니다.