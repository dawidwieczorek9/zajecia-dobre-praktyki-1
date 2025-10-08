def is_palindrome(text: str) -> bool:
    new_text = text.replace(" ", "").lower()
    palindrome = ''.join(reversed(new_text))

    if new_text == palindrome:
        return True
    else:
        return False


def fibonacci(n: int) -> int:
    if n < 0:
        return None
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def count_vowels(text: str) -> int:
    text_lower = text.lower()
    vowels = "aioeuyóąę"
    counter = 0

    for vowel in vowels:
        counter += text_lower.count(vowel)

    return counter


def calculate_discount(price: float, discount: float) -> float | ValueError:
    if 0 <= discount <= 1:
        last_price = price - price * discount
        return last_price
    else:
        return ValueError("Wartość rabatu musi być pomiędzy 0 a 1")


def flatten_list(nested_list: list) -> list:
    lista_koncowa = []
    for element in nested_list:
        if isinstance(element, list):
            lista_koncowa.extend(flatten_list(element))
        else:
            lista_koncowa.append(element)
    return lista_koncowa


def word_frequences(text: str) -> dir:
    to_delete = [",", ".", "!", "?", ":", ";", "(", ")", "[", "]", "'"]

    for i in to_delete:
        text = text.replace(i, "")

    words = text.lower().split()
    frequency = {}


    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1

    return frequency


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    elif n == 2:
        return True
    else:
        for i in range(2,n):
            if n % i == 0:
                return False
            else:
                return True


# testy
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

