
import execjs


def get_js():
    try:
        f = open('test.js', 'r', encoding='utf-8')
        line = f.readline()
        jstr = ''
        while line:
            jstr = jstr + line
            line = f.readline()
        f.close()
        return jstr
    except:
        pass
    return False


def main():
    jstr = get_js()
    if jstr:
        ctx = execjs.compile(jstr)
        print(ctx.call('myadd', 5, 7))


if __name__ == '__main__':
    main()
