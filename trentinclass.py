2.3
words = ["kiwi", "fig", "banana", "plum", "apple"]

long_words = list(filter(lambda word: len(word) > 4, words))
print(long_words)  

by_length = sorted(words, key=lambda word: len(word))
print(by_length)  

2.4
class Adder:
    def __init__(self, amount):
        self.amount = amount

    def __call__(self, value):
        return value + self.amount

add_ten = Adder(10)

print(add_ten(5))      
print(callable(add_ten))  

3.1
def count_up_to(n):
    """Yield 1, 2, 3, ... up to n."""
    i = 1
    while i <= n:
        yield i
        i += 1

print(list(count_up_to(3)))  

gen = count_up_to(2)
print(next(gen))  
print(next(gen))  

3.4
squares = (x * x for x in range(5))

print(next(squares))  
print(next(squares))  
print(list(squares))  

4.1
def total(*numbers):
    """Return the sum of all the arguments."""
    return sum(numbers)

print(total(1, 2, 3))  
print(total())          

prices = [5, 10, 15]

result = total(*prices)
print(result)  

4.2
def describe(name, age):
    return f"{name} is {age}"

person = {"name": "Ada", "age": 36}

result = describe(**person)
print(result)  
