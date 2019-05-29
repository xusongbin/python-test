
import time
import random
import uiautomator2 as u2


def read_file():
    with open('title.txt', 'a+', encoding='UTF-8') as f:
        pass
    with open('title.txt', 'r', encoding='UTF-8') as f:
        _list = f.read().split('\n')
    return _list


def write_file(data):
    with open('title.txt', 'a+', encoding='UTF-8') as f:
        f.write(data + '\n')


def read_one_new(_d, _ss, _list):
    si = _ss(className='android.widget.ListView')
    try:
        num = int(si.info['childCount'])
    except:
        return None
    for i in range(num):
        try:
            tt = si.child(resourceId='com.ss.android.article.lite:id/gm')[i].get_text(1)
            if tt not in _list:
                print('获取新闻标题：' + tt)
                si.child(resourceId='com.ss.android.article.lite:id/gm')[i].click()
                start_time = time.time()
                time.sleep(random.randint(20, 50) / 10)
                while True:
                    _d.swipe(360, 900, 360, 500, 0.02)
                    time.sleep(random.randint(20, 50) / 10)
                    stop_time = time.time()
                    if stop_time - start_time > 15:
                        break
                _d.press('back')
                return tt
        except:
            pass
    return None


def main():
    last_text = read_file()

    d = u2.connect()
    ss = d.session('com.ss.android.article.lite', attach=True)
    if ss.running():
        while True:
            tt = read_one_new(d, ss, last_text)
            if tt:
                last_text.append(tt)
                write_file(tt)
            else:
                d.swipe(360, 900, 360, 500, 0.02)


def test():
    d = u2.connect()
    ss = d.session('com.ss.android.article.lite', attach=True)
    if ss.running():
        si = ss(className='android.widget.ListView')
        for i in range(si.info['childCount']):
            try:
                tt = si.child(resourceId='com.ss.android.article.lite:id/gm')[i].get_text(1)
                print('获取新闻标题：' + tt)
            except:
                pass


if __name__ == '__main__':
    main()
    # test()
