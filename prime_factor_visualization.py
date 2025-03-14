from math import sqrt
import matplotlib.pyplot as plt




def generate_primes(max_num):
    """Generate prime numbers up to max_num"""
    if max_num < 0:
        return

    primes = [] # Keep tracks of all prime numbers
    for i in range(2, max_num+1):
        if isprime(i, primes):
            primes.append(i)
            yield i


def isprime(n, primes):
    """Determines if n is prime where primes containes all prime numbers smaller then i"""
    if n < 2:
        raise ValueError("n should be larger than 2")

    for i in primes:
        if i > sqrt(n):
            return True
        if n % i == 0:
            return False

    # When we have an empty list
    return True     




def prime_factors(num):
    """Yields all the prime factors of a number"""
    if num < 2:
        return
    remaining = num
    for i in generate_primes(num):
        while remaining % i == 0:
            yield i
            remaining /= i
        if remaining == 1:
            break


def plot_primes(max_num):
    
    all_primes = [p for num in range(max_num+1) for p in prime_factors(num)]
    print(all_primes)
    primes = {p : all_primes.count(p) for p in set(all_primes)}

    plt.bar(list(primes.keys()), list(primes.values()), tick_label=list(primes.keys()), color="skyblue", edgecolor="black")
    plt.title(f"Occurrences of prime numbers up to {max_num}")
    plt.xlabel("Unique prime numbers found")
    plt.ylabel("Frequency of each prime")
    plt.show()


plot_primes(10)


