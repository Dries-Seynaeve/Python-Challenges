def unique_chars(text):
    dummy = set()
    for char in text.lower():
        if char.isalpha() and not char in dummy:
            dummy.add(char)
            yield char


def inner_level(i, numbers):
    for j in numbers:
        yield (i, j)
        
def all_pairs(numbers):
    for i in numbers:
        yield from inner_level(i, numbers)



from math import sqrt
        
def is_prime(i, primes):
    for j in primes:
        if j > sqrt(i):
            return True
        elif i % j == 0:
            return False
    return True

def primes_up_to(n):
    if n < 2:
        return
    i = 2
    primes = set()
    while i <= n:
        if is_prime(i, primes):
            primes.add(i)
            yield i
        i += 1

from typing import Iterator, List # Need this for type hints

def chunked_lines(filename: str, chunk_size: int) -> Iterator[list[str]]:
    """
    Yields chuncks of up to chunk_size lines from filename.
    """
    # Let's make sure chunk_size >= 1
    if chunk_size < 1:
        raise ValueError(f"chunk_size should be >= 1, {chunk_size} was given")

    try:
        with open(filename, encoding='utf-8') as f:
            chunk = []
            for line in f:
                chunk.append(line.strip())
                if len(chunk) == chunk_size:
                    yield chunk
                    chunk = []

            if len(chunk) > 0:
                yield chunk
    except FileNotFoundError:
        raise FileNotFoundError(f"file {filename} was not found")
    
            







            




