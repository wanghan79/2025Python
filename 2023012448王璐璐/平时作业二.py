import random
import string

def sample_generator(num, typ):
    i = 0
    while i < num:
        if typ == 'int':
            yield random.randint(0, 100)
        elif typ == 'float':
            yield random.uniform(0, 100)
        elif typ == 'str':
            s = ''
            j = 0
            while j < 5:
                s += random.choice(string.ascii_letters)
                j += 1
            yield s
        i += 1

def main():
    g = sample_generator(5, 'int')
    for x in g:
        print(x)
    g = sample_generator(3, 'float')
    for x in g:
        print(x)
    g = sample_generator(4, 'str')
    for x in g:
        print(x)

main()
