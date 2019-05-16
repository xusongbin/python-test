
import re

if __name__ == '__main__':
    str1 = '400x400+483+184'
    print(re.findall(r'(\d+)', str1))
