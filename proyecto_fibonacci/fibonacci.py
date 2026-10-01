def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

def fibdyn(n):
    if n <= 1:
        return n
    f = [0, 1]
    for i in range(2, n + 1): f.append(f[-1] + f[-2])
    return f[:n]


if __name__ == "__main__":
    print([fib(i) for i in range(10)])
    print(fibdyn(10))