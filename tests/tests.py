from ..functions import is_palindrome
from ..functions import fibonacci
from ..functions import count_vowels
from ..functions import calculate_discount
from ..functions import flatten_list
from ..functions import word_frequences
from ..functions import is_prime


print("1. palindrome:")

print(is_palindrome("kajak"))
print(is_palindrome("Kobyła ma mały bok"))
print(is_palindrome("python"))
print(is_palindrome(""))
print(is_palindrome("A"))

print("2. fibonacci:")

print(fibonacci(0))
print(fibonacci(1))
print(fibonacci(5))
print(fibonacci(6)) #Zmieniłem na 6 bo bardzo długo liczył 55
print(fibonacci(-1))

print("3. vowels:")

print(count_vowels("Python"))
print(count_vowels("AEIOUY"))
print(count_vowels("bcd"))
print(count_vowels(""))
print(count_vowels("Próba żółwia"))

print("4. discount:")

print(calculate_discount(100, 0.2))
print(calculate_discount(50, 0))
print(calculate_discount(200, 1))
print(calculate_discount(100, -0.1))
print(calculate_discount(100, 1.5))

print("5. flatten list:")

print(flatten_list([1, 2, 3]))
print(flatten_list([1, [2, 3], [4, [5]]]))
print(flatten_list([]))
print(flatten_list([[[1]]]))
print(flatten_list([1, [2, [3, [4]]]]))

print("6. word frequences:")

print(word_frequences("To be or not to be"))
print(word_frequences("Hello, hello!"))
print(word_frequences(""))
print(word_frequences("Python Python python"))
print(word_frequences("Ala ma kota, a kot ma Ale."))

print("7. is prime:")

print(is_prime(2))
print(is_prime(3))
print(is_prime(4))
print(is_prime(0))
print(is_prime(1))
print(is_prime(5))
print(is_prime(97))

