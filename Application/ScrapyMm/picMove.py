#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

path = r'D:\Program Files\魔兽争霸III：冰封王座V1.20E\ship\Picture'

stars_name = (
    '李宇春 张靓颖 周笔畅 何洁 刘亦菲 张含韵 陈好 尚雯婕 汤唯 张筱雨 韩雪 孙菲菲 张嘉倪 霍思燕 陈紫函 朱雅琼 '
    '江一燕 厉娜 许飞 胡灵 郝菲尔 刘力扬 章子怡 谭维维 魏佳庆 张亚飞 李旭丹 孙艺心 巩贺 艾梦萌 闰妮 '
    '王蓉 汤加丽 汤芳 牛萌萌 范冰冰 赵薇 周迅 金莎 纪敏佳 黄雅莉 叶一茜 马苏 阿桑 董卿 金铭 徐行 '
    '姚笛 朱妍 夏颖 陈西贝 冯家妹 高娅媛 林爽 郑靖文 陶虹 徐静蕾 黄奕 董洁 巩俐 高圆圆 于娜 孟广美 '
    '美女奉奉 小龙女彤彤 张子萱 果子 丁贝莉 香香 段思思 二月丫头 刘羽琦 拉拉公主 沈丽君 周璟馨 '
    '丁叮 谢雅雯 陈嘉琪 宋琳 郭慧敏 卢洁云 佘曼妮 黄景 马艳丽 蒋雯丽 宁静 许晴 张静初 瞿颖 张延 孙俪 '
    '闵春晓 蔡飞雨 邓莎 白冰 程媛媛 吴婷 殷叶子 朱伟珊 孙菂 赵梦恬 龚洁 许晚秋 杨舒婷 乔维怡 王海珍 易慧 '
    '谢雨欣 陈娟红 舒畅 李小璐 曹颖 李冰冰 王艳 沈星 阿朵 周洁 杨林 李霞 陈自瑶 李小冉 李湘 金巧巧 '
    '蒋勤勤 梅婷 刘涛 秦海璐 安又琪 杨钰莹 马伊俐 陈红 鲍蕾 牛莉 胡可 杨幂 龚蓓苾 田震 杨童舒 吕燕 '
    '王姬 苗圃 李欣汝 王小丫 秦岚 徐帆 刘蓓 彭心怡 邓婕 眉佳 李媛媛 刘晓庆 杨若兮 黄圣依 林熙 薛佳凝 '
    '斯琴格日乐 宋祖英 郝蕾 乐珈彤 冯婧 宋丹丹 盖丽丽 田海蓉 杨澜 沈冰 王宇婕 王希维 姜培琳 何晴 焦媛 白灵 '
    '胡静 陈冲 刘怡君 韦唯 龚雪 周彦宏 刘丹 傅艺伟 谢东娜 朱媛媛 黑鸭子 周璇 吕丽萍 杨欣 陈小艺 伍宇娟 '
    '苏瑾 李玲玉 张凯丽 潘虹 沈丹萍 岳红 赵静怡 宋晓英 蔡依林 张韶涵 王心凌 徐若瑄 林志玲 王菲 S.H.E Twins '
    '徐熙媛 桂纶镁 林依晨 陈乔恩 梁静茹 蔡诗芸 范玮琪 廖碧儿 张柏芝 李嘉欣 容祖儿 李玟 贾静雯 MaggieQ 林心如 朱茵 '
    '叶璇 唐宁 曾之乔 安以轩 杨丞琳 侯佩岑 同恩 陈松伶 文颂娴 梁凯蒂 林韦君 陈思璇 曹敏莉 乐基儿 郑雪儿 佘诗曼 '
    '郑秀文 萧蔷 温碧霞 刘嘉玲 刘玉玲 林熙蕾 李若彤 张曼玉 关之琳 陈慧琳 萧淑慎 蔡少芬 萧亚轩 田丽 杨采妮 李丽珍 '
    '琦琦 天心 任港秀 杨思敏 郭静纯 钟丽缇 孙燕姿 叶玉卿 翁红 邱淑贞 蔡淑臻 梁咏琪 季芹 舒淇 莫文蔚 戴佩妮 '
    '刘若英 杨千桦 范伟琪 徐熙娣 陈宝莲 吴辰君 张庭 林嘉欣 俞飞鸿 叶子楣 周海媚 伊能静 蜜雪薇琪 侯湘婷 Hebe 应采儿 '
    '许茹芸 吴佩慈 郑希怡 范文芳 李彩桦 蔡淳佳 本多RuRu 范晓萱 张惠妹 林忆莲 关心妍 卓依婷 杨恭如 陈文媛 吴小莉 '
    '梅艳芳 林青霞 赵雅芝 孟庭苇 吴倩莲 陈慧珊 许慧欣 黎姿 周慧敏 钟楚红 蔡琴 齐豫 邓丽君 林凤娇 陈玉莲 周冰倩 '
    '杨惠姗 金素梅 翁美玲 高胜美 甄妮 胡慧中 邝美云 俞小凡 吕秀菱 萧芳芳 刘雪华 潘迎紫 梁雁翎 汪明荃 苏芮 冯宝宝 蔡依林 '
    '利智 张艾嘉 叶倩文 陈淑桦 郑裕玲 潘越云 凤飞飞 喻可欣 阿悄 本兮 庄心妍 李金铭 戚薇 唐嫣 杨幂 张檬 金莎 王媛可 '
    '唐艺昕 何洁 何曼婷 梁静茹 谢娜 吴昕 娄艺潇 邓家佳 赵霁 赵文琪 邓紫棋 古丽娜扎 刘诗诗 郑爽 李菲儿 刘涛 许晴 '
    '郑佩佩 张凯丽 王珞丹 高露 李小萌 白百合 赵丽颖 杨颖 小凌 刘丹萌 孙羽幽 童可可 佟丽娅 林心如 王丽坤 李小璐 '
    '周迅 刘亦菲 高圆圆 李冰冰 范冰冰 张嘉倪 袁姗姗 孙菲菲 朱丹 王智 徐若萱 刘萌萌 李宇春 杨蓉 刘雨欣 刘心悠 '
    '李沁 陶昕然 斓曦 程愫 安雅萍 郭采洁 郭碧婷 郁可唯 谢婷婷 舒畅 桂纶镁 BY2 蔡依林 周笔畅 尚雯婕 马伊利 '
    '姚笛 馨子 卓文萱 付梦妮 秦岚 A-lin 王诗安 姚贝娜 王鳞 赵子靓 叶一茜 董洁 钟欣潼 闫妮 杨曦 柳岩 赵韩樱子 '
    '钟洁 刘晓庆 吴莫愁 杨紫 张靓颖 张韶涵 王洋 江铠同 陈数 李晟 万茜 海陆 那英 热依扎 罗震环 张含韵 李波儿 贾玲 '
    'By2 刘惜君 郭婉婷 谢楠 Ella 郑亦桐 陈漫 蒋梦婕 谢楠 女团 艾菲 王子文 莫小棋 全智贤 李贞贤 邱欣怡 杨丽萍 '
    '司珂华 安心亚 关晓彤 孙磊磊 贾青 江语晨 江疏影 江伊涵 熊乃瑾 颜丹晨 杨千嬅 丁子高 陈妍希 SHE 安金莉娅 '
    '干露露 张雨绮 刘冬 景甜 李一桐 陶晶莹 梁洛施 钟嘉欣 李心洁 黄小柔 高海宁 李千娜 任家萱 金泫雅 歌手 '
    '徐洁儿 杨子祯 唐一菲 车永莉 陈若仪 林志颖 剧照 董璇 偶像 香港小姐 小s 小S 古力娜扎 陈法拉 吉丽 倪妮 '
    '冯丹滢 宋智孝 孔孝真 徐立纯 袁咏仪 方安娜 潘雨汛 李漫荻 牟星 申珉熙 孟美岐 张钧甯 泰勒斯威夫特 '
    '张馨比 许榕真 麦迪娜 赵卓娜 姚芊羽 夏梓桐 甘薇 万曦媛 曾宝仪 姚芊羽 郭露文 港星 邓英 颖儿 女星 '
    '蒋欣 演唱会 艾薇儿 王小玮 巨星 布兰妮 李宝美 广告 河智苑 申世京 魏羽潼 童瑶 吉克隽逸 组合 朴恩率 '
    '玖月奇迹 邓丽欣 海清 李莎旻子 网红 秀智 冠军 范琳琳'
)
stars_list = stars_name.split(' ')
stars_list = set(stars_list)
stars_list = [x for x in stars_list if x != '']

actress_name = (
    '麻生希 桃谷绘里香 大桥未久 早乙女露依 橘梨纱 美竹铃 天海翼 泷泽萝拉 樱井莉亚 铃原爱蜜莉 '
    '滨崎步 小池荣子 深田恭子 小仓优子 安室奈美惠 滨野裕子 川岛和津实 长谷川京子 饭洼五月 '
    '高井麻帆 优香 井上晴美 今井惠理 川村光 相马茜 新山千春 释由美子 友坂理惠 小向美奈子 原史奈 中岛史惠 安西广子 '
    '细川典江 金泽明子 小泽圆 夕树舞子 佐藤蓝子 加藤爱 三津谷叶子 金素妍 桥本丽香 广末凉子 宇多田光 '
    '宝儿 藤原纪香 宋允儿 小柳由纪 仓木麻衣 田中丽奈 酒井法子 崔真实 松岛菜菜子 中谷美纪 川村亚纪 爱内里菜 '
    '铃木亚美 工藤静香 白智英 沈银河 朴志胤 宫泽理惠 李秀英 山口百惠 大黑摩季 今井绘理子 松隆子 中岛美雪 '
    '朴正炫 朴惠京 上原多香子 黑木瞳 相川七濑 内山理名 铃木保奈美 林秀晶 常盘贵子 川岛茉树代 濑户朝香 '
    '吉泽明步 松岛枫 水咲萝拉'
)
actress_list = actress_name.split(' ')
actress_list = set(actress_list)
actress_list = [x for x in actress_list if x != '']


def delete_less_pic_dir():
    main_path = path
    for d1 in os.listdir(main_path):
        second_path = os.path.join(main_path, d1)
        for d2 in os.listdir(second_path):
            cur_path = os.path.join(second_path, d2)
            if len(os.listdir(cur_path)) < 4:
                print(d2)
                shutil.rmtree(cur_path)


def move_stars_to_dest():
    dest_path = r'D:\Program Files\魔兽争霸III：冰封王座V1.20E\ship\Picture\明星'
    for d in os.listdir(path):
        for name in stars_list:
            if name in d:
                this_path = os.path.join(path, d)
                next_path = os.path.join(dest_path, d)
                print('{} => {}'.format(this_path, next_path))
                try:
                    shutil.move(this_path, next_path)
                except:
                    pass


def move_actress_to_dest():
    dest_path = r'D:\Program Files\魔兽争霸III：冰封王座V1.20E\ship\Picture\女优'
    for d in os.listdir(path):
        for name in actress_list:
            if name in d:
                this_path = os.path.join(path, d)
                next_path = os.path.join(dest_path, d)
                print('{} => {}'.format(this_path, next_path))
                try:
                    shutil.move(this_path, next_path)
                except:
                    pass


def move_keyword_to_dest(key, dir):
    dest_path = r'D:\Program Files\魔兽争霸III：冰封王座V1.20E\ship\Picture'
    dest_path = os.path.join(dest_path, dir)
    for d in os.listdir(path):
        if key in d:
            this_path = os.path.join(path, d)
            next_path = os.path.join(dest_path, d)
            print('{} => {}'.format(this_path, next_path))
            try:
                shutil.move(this_path, next_path)
            except:
                pass


def move_keylist_to_dest(key, dir):
    dest_path = r'D:\Program Files\魔兽争霸III：冰封王座V1.20E\ship\Picture'
    dest_path = os.path.join(dest_path, dir)
    if not os.path.isdir(dest_path):
        return
    for d in os.listdir(path):
        ctn = False
        for k in key:
            if not k:
                continue
            if k not in d:
                ctn = True
                break
        if ctn:
            continue
        this_path = os.path.join(path, d)
        next_path = os.path.join(dest_path, d)
        print('{} => {}'.format(this_path, next_path))
        try:
            shutil.move(this_path, next_path)
        except:
            pass


def repair_mistake():
    file = 'tmp.log'
    dest_path = r'D:\Program Files\Picture'
    with open(file, 'r', encoding='utf-8') as f:
        src_path = f.read()
    src_path = src_path.split('\n')
    src_path = [x.split('>')[1].strip() for x in src_path]
    for this_path in src_path:
        if not os.path.isdir(this_path):
            continue
        this_name = this_path.split('\\')[-1]
        next_path = os.path.join(dest_path, this_name)
        print('{} => {}'.format(this_path, next_path))
        try:
            shutil.move(this_path, next_path)
        except:
            pass


# repair_mistake()
# move_actress_to_dest()
# move_stars_to_dest()
# move_keyword_to_dest('Angelina Danilova', '性感')
# move_keyword_to_dest('陈巧蓓', '大奶')
# move_keyword_to_dest('崔宝月', '清新')
# move_keylist_to_dest(['韩国', '妩媚'], '性感')
delete_less_pic_dir()

