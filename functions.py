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



