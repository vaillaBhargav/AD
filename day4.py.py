
def sum_of_evens(n):
    if n <= 0:
        return 
    even_sum = sum(i for i in range(2, n + 1, 2))
    return even_sum
n = 10  
result = sum_of_evens(n)
print(f"The sum of all even numbers between 1 and {n} is: {result}")





