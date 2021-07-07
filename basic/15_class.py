# def calArea(b, h) :
#     return b * h / 2

# triangle1_b = 20
# triangle1_h = 10

# triangle2_b = 12
# triangle2_h = 6

# triangle3_b = 5
# triangle3_h = 30

# print(calArea(triangle1_b, triangle1_h))
# print(calArea(triangle2_b, triangle2_h))
# print(calArea(triangle3_b, triangle3_h))

class Triangle :
	height = 10
	bottom = 4

tri1 = Triangle()
print(tri1.height)

tri1.height = 8
print(tri1.height)

#

class Triangle : 
    cal_count = 0
    
    def __init__(self, b, h = 5) : #생성자
        self.b = b
        self.h = h

    def area(self) :
        Triangle.cal_count += 1
        
        return self.b * self.h / 2

tri1 = Triangle(4)
tri2 = Triangle(6, 10)

print(tri1.b, tri1.h, tri1.area(), tri1.cal_count)
print(tri2.b, tri2.h, tri2.area(), tri2.cal_count)

print(Triangle.cal_count)

#

class Triangle :
    def __init__(self, b, h) : #생성자
        self.b = b
        self.h = h
    
    def area(self) :
        return self.b * self.h / 2

   
tri1 = Triangle(4, 5) #호출하면서 바로 인자 전달
tri2 = Triangle(6, 10)

print(tri1.b, tri1.h, tri1.area())
print(tri2.b, tri2.h, tri2.area())

#

class Triangle :    
    def __init__(self, b, h = 5) : #생성자 매개변수 미리 지정
        self.b = b
        self.h = h
    
    def area(self) :
        return self.b * self.h / 2

tri1 = Triangle(4)
tri2 = Triangle(6, 10)

print(tri1.b, tri1.h, tri1.area())
print(tri2.b, tri2.h, tri2.area())

#

class Triangle : 
    cal_count = 0
    
    def __init__(self, b, h = 5) :
        self.b = b
        self.h = h
        
    def area(self) :
        Triangle.cal_count += 1
        
        return self.b * self.h / 2
    
    @staticmethod
    def isIsosceles(a, b) :
        Triangle.cal_count += 1
        return a == b
    
    @classmethod
    def printCount(cls) :
        print(cls.cal_count)
   
tri1 = Triangle(4) #밑변 4 삼각형 객체 생성

print(tri1.b, tri1.h, tri1.area(), tri1.cal_count)
print(Triangle.isIsosceles(5,4))

tri1.printCount() #인스턴스로 접근
Triangle.printCount() #클래스로 직접 접근

#
# 상속
#

import math

#도형
class Shape :
    cal_count = 0
    figure = "Shape"

    @classmethod
    def class_printFigure(cls) :
        return cls.figure
    
    @staticmethod
    def static_printFigure() :
        return Shape.figure

#도형 상속 삼각형
class Triangle(Shape) : 
    figure = "triangle"
    
    def __init__(self, b, h=5) :
        self.b = b
        self.h = h
        
    def area(self) :
        Shape.cal_count += 1
        
        return self.b * self.h / 2

#도형 상속 정삼각형
class EquTriangle(Triangle) : 
    figure = "equilateral triangle"
    
    def __init__(self, b) :
        self.b = b
        
    def area(self) :
        Shape.cal_count += 1
        
        return 0.25 * math.sqrt(3) * self.b ** 2
    
    def circumference(self) :
        return self.b * 3

#도형 상속 원
class Circle(Shape) :
    figure = "circle"
    
    def __init__(self, r) :
        self.r = r
        
    def area(self) :
        Shape.cal_count += 1
        
        return math.pi * self.r ** 2
    
    def circumference(self) :
        return 2 * math.pi * self.r

tri = Triangle(10, 4)
eqtri = EquTriangle(3)
cir = Circle(8)

print(cir.static_printFigure(), cir.area(), cir.circumference())
print(tri.class_printFigure(), tri.area(), cir.circumference())
print(eqtri.class_printFigure(), eqtri.area(), cir.circumference())

print(Shape.cal_count, cir.cal_count, tri.cal_count)

#

# 부모 클래스
class Person :
    job = ""
    
    @classmethod
    def greeting(cls) :
        print("안녕하세요 저는",cls.job,"입니다.")
    
    def printAge(self) :
        print(self.age)

# Person 상속
class Student(Person) :
    job = "student"
    
    def __init__(self, age) :
        self.age = age
        
    def printAge(self) :
        print("저의 나이는", self.age, "입니다.")    

# Person 상속
class Professor(Person) :
    job = "professor"   
    
    def __init__(self, age) :
        self.age = age
        
    def printAge(self) :
        print("저의 나이는", self.age, "입니다.") 
   
std = Student(14)
pf = Professor(56)

std.greeting()
std.printAge()

pf.greeting()
pf.printAge()

#
# 다중 상속
#

class First :
    name = "first"
    def __init__(self) :
        print("First class")
    
    def printFirst(self) :
        print("first")
        
class Second :
    name = "second"
    def __init__(self) :
        print("First class")
    
    @classmethod
    def printName(cls) :
        print(cls.name)

#상속해야 할 부모클래스가 두 개인 경우 충돌 가능
#파이썬은 MRO에 따라 다중 상속을 진행
class Third(First, Second) :
    pass

third = Third()
third.printName()
third.printFirst()

# 오버로딩은 지원 안함
