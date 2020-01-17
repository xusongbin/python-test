#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ParseRequest(object):
    def __init__(self):
        self.__file_name = 'request_1A0001.txt'

        self.send_data = (
            'FD FD FD FD 30 30 30 30 30 30 '
            '61 64 09 00 16 00 00 4E 10 12 00 09 00 21 01 00 00 00 00 1E 30 97 00 00 00 '
            '43 6F 64 65 4C 69 73 74 3D 31 36 28 31 41 30 30 30 31 2C 29 3B 0D 0A '  # CodeList=16(1A0001,);
            '44 61 74 61 54 79 70 65 3D 31 '
            '33 2C 31 31 2C 39 2C 38 2C 37 '
            '2C 31 39 2C 36 2C 38 30 33 2C '
            '38 30 32 2C 34 30 37 2C 34 36 '
            '33 2C 34 36 30 2C 34 35 36 2C '
            '34 35 35 2C 34 35 34 2C 31 33 '
            '33 30 2C 0D 0A '   # DataType=13,11,9,8,7,19,6,803,802,407,463,460,456,455,454,1330,
            '44 61 74 65 54 69 6D 65 3D 31 32 33 31 38 28 2D 31 38 38 2D 30 29 0D 0A '      # DateTime=12318(-188-0)
            '4C 61 63 6B 54 69 6D 65 3D 30 2C 30 2C 30 2C 33 2C 30 2C 30 2C 30 2C 30 0D 0A '  # LackTime=0,0,0,3,0,0,0,0
            '70 61 67 65 69 64 3D 35 37 30 33 0D 0A'    # pageid=5703
        )
        self.parse_send()

        self.recv_data = (
            'FD FD FD FD 30 30 30 30 31 35 30 38 09 00 16 00 00 '
            '4E 10 12 00 09 00 21 01 00 01 10 00 1E 30 EE 14 00 00 00 00 00 00 '
            '68 64 31 2E 30 00 BD 00 00 00 42 00 1C 00 07 00 01 30 00 04 0D 70 00 04 0B '
            '70 00 04 09 70 00 04 08 70 00 04 07 70 00 04 13 70 00 04 16 00 01 00 10 '
            '31 41 30 30 30 31 00 00 00 00 00 00 00 00 00 '
            'BD 00 DE 2A 7B 07 CE BE 0E 21 14 17 C9 C1 83 F3 C7 C1 A1 32 '
            'C9 C1 33 F6 C7 C1 AF AD 2F 31 5E 2B 7B 07 BF 0F 77 21 11 48 '
            'CA C1 B1 25 C9 C1 48 08 CB C1 77 36 C9 C1 7B D6 95 31 80 2B '
            '7B 07 AB 17 ED 20 18 7A C9 C1 B6 E4 C8 C1 EC 77 CA C1 30 69 '
            'CA C1 ED FC 0D 31 9E 2B 7B 07 0C DD EF 20 E9 59 C8 C1 1D 29 '
            'C8 C1 68 C5 C9 C1 8B 87 C9 C1 36 B5 10 31 C0 2B 7B 07 4B 3D '
            '4B 21 E6 79 C8 C1 8E CE C7 C1 28 8C C8 C1 19 72 C8 C1 1A 1E '
            '6D 31 80 32 7B 07 76 44 45 22 D8 88 C8 C1 45 B0 C7 C1 F2 C3 '
            'C8 C1 8F 8C C8 C1 36 C8 B5 32 9E 32 7B 07 01 5F 5D 21 83 AE '
            'C8 C1 3E DF C7 C1 2D 16 C9 C1 73 7B C8 C1 F5 ED 98 31 C0 32 '
            '7B 07 3B 5B 1E 21 4E 5B C7 C1 81 56 C7 C1 83 CF C8 C1 D1 A4 '
            'C8 C1 F6 8A 3B 31 DE 32 7B 07 9E 9E D0 20 F0 9C C7 C1 6E 3A '
            'C7 C1 1B 22 C8 C1 8F 6E C7 C1 7C E7 E2 30 5E 33 7B 07 DB 20 '
            'DD 20 40 FB C6 C1 F5 EF C6 C1 64 9A C7 C1 F2 97 C7 C1 AE 5F '
            'F1 30 80 33 7B 07 82 F3 CF 20 09 04 C7 C1 09 B1 C6 C1 8E 86 '
            'C7 C1 0C 1C C7 C1 ED F1 E8 30 9E 33 7B 07 CB A5 21 21 33 0A '
            'C6 C1 ED FF C5 C1 C2 33 C7 C1 31 F7 C6 C1 85 2A 27 31 C0 33 '
            '7B 07 43 61 79 21 63 7F C6 C1 DA 24 C5 C1 63 7F C6 C1 61 18 '
            'C6 C1 9A BF 88 31 80 3A 7B 07 38 72 D8 21 4C 56 C5 C1 9C 51 '
            'C5 C1 F4 7F C6 C1 FC 6D C6 C1 A0 30 22 32 9E 3A 7B 07 B9 D3 '
            '52 21 C0 BC C7 C1 3C 16 C5 C1 84 C6 C7 C1 EC 65 C5 C1 18 0D '
            '79 31 C0 3A 7B 07 55 93 F4 20 04 C0 C6 C1 0C 95 C6 C1 40 14 '
            'C8 C1 B8 CE C7 C1 7B A7 1C 31 DE 3A 7B 07 C2 5C FD 16 34 28 '
            'C5 C1 B4 1B C5 C1 44 DF C6 C1 80 BC C6 C1 67 C4 D1 30 5E 3B '
            '7B 07 5A 34 2A 16 64 84 C5 C1 64 20 C5 C1 9C B5 C5 C1 F4 21 '
            'C5 C1 AE 33 5D 27 80 3B 7B 07 A0 DB 87 16 38 CE C5 C1 AC 46 '
            'C5 C1 FC F0 C5 C1 A8 81 C5 C1 92 8B 58 27 9E 3B 7B 07 23 7D '
            'D6 20 30 F9 C5 C1 1C 90 C5 C1 F0 1E C7 C1 D4 CD C5 C1 F5 95 '
            'EE 30 C0 3B 7B 07 B9 73 3B 21 DC 83 C6 C1 54 C1 C5 C1 DC 83 '
            'C6 C1 3C F7 C5 C1 51 07 59 31 80 42 7B 07 59 09 24 22 63 EC '
            'C7 C1 21 A5 C7 C1 0A 93 C9 C1 3D D8 C8 C1 3D 10 A6 32 9E 42 '
            '7B 07 EE DF 20 21 1D 6B C7 C1 F4 3C C7 C1 AC 00 C8 C1 AC 00 '
            'C8 C1 B3 79 5E 31 C0 42 7B 07 07 1B E1 20 25 E2 C6 C1 AE BC '
            'C6 C1 C5 ED C7 C1 9A 77 C7 C1 4B 81 0C 31 DE 42 7B 07 0C 1E '
            'AB 17 57 1F C8 C1 B1 7D C6 C1 31 31 C8 C1 82 E0 C6 C1 D6 76 '
            'DE 30 5E 43 7B 07 7C 2F D1 20 2E 95 C6 C1 D3 7C C6 C1 A4 4D '
            'C8 C1 3B 25 C8 C1 33 E3 EB 30 80 43 7B 07 2E 31 BC 17 6C 6C '
            'C6 C1 1C D4 C5 C1 F8 D3 C6 C1 D4 A2 C6 C1 13 F9 E3 30 9E 43 '
            '7B 07 54 F7 0A 21 9A ED C4 C1 29 9F C4 C1 21 B2 C6 C1 93 69 '
            'C6 C1 0A 0F 1A 31 C0 43 7B 07 44 62 60 21 79 4C C4 C1 1F 18 '
            'C4 C1 E2 F5 C4 C1 76 EE C4 C1 7B 93 83 31 80 5A 7B 07 2C B6 '
            '5F 22 08 59 C0 C1 B9 AE BF C1 E3 20 C2 C1 E3 20 C2 C1 0E DF '
            '9A 32 9E 5A 7B 07 32 29 56 21 E9 BE BF C1 07 12 BF C1 3D 76 '
            'C0 C1 18 4B C0 C1 E1 78 67 31 C0 5A 7B 07 5C 89 E8 20 55 94 '
            'BF C1 40 DB BE C1 95 D9 BF C1 28 B6 BF C1 EE AF EF 30 DE 5A '
            '7B 07 A8 24 72 17 A3 C8 BE C1 A4 6B BE C1 A9 BE BF C1 B1 A4 '
            'BF C1 76 A5 B7 27 5E 5B 7B 07 EB 25 CD 20 56 DE BE C1 C9 F9 '
            'BD C1 A0 E7 BE C1 BC DE BE C1 F1 47 D8 30 80 5B 7B 07 3C 6C '
            'C9 16 0E 5D BE C1 11 3D BE C1 E9 06 BF C1 8A E6 BE C1 51 4B '
            '28 27 9E 5B 7B 07 AC 6D 2A 21 5B 77 BC C1 48 30 BC C1 DE 78 '
            'BE C1 E2 5C BE C1 3E 15 2E 31 C0 5B 7B 07 2E 44 67 21 E2 06 '
            'BC C1 AA 89 BB C1 CB 0E BD C1 DD 75 BC C1 01 1F 74 31 80 62 '
            '7B 07 21 E4 C8 21 4B 47 BB C1 9E 43 BB C1 36 4C BD C1 E4 7C '
            'BC C1 AC AF EF 31 9E 62 7B 07 82 F1 2E 21 23 62 BB C1 FB B9 '
            'BA C1 11 EB BB C1 2A 43 BB C1 AC 17 38 31 C0 62 7B 07 81 6A '
            'EB 20 97 A0 B9 C1 DE 5B B9 C1 DA BE BB C1 7B 6F BB C1 B2 F6 '
            'FA 30 DE 62 7B 07 B4 7E 02 17 AF 02 BA C1 A1 35 B9 C1 AF 58 '
            'BA C1 6B 9E B9 C1 80 64 5A 27 5E 63 7B 07 A6 0C D3 16 FF E5 '
            'BB C1 A4 D8 B9 C1 1D 07 BC C1 28 06 BA C1 B0 CE 6D 27 80 63 '
            '7B 07 60 30 6D 17 9F D1 BB C1 E5 9C BB C1 21 CD BC C1 BA E9 '
            'BB C1 3D 9E D1 30 9E 63 7B 07 D6 8C 8C 16 9F 0E BC C1 30 8C '
            'BB C1 12 96 BC C1 A7 DD BB C1 36 E3 43 27 C0 63 7B 07 B6 54 '
            '10 21 48 C4 BC C1 AC 75 BB C1 E6 D4 BC C1 62 0A BC'
        )
        self.parse_recv()

    def parse_send(self):
        _data_list = self.send_data.split(' ')
        _send_len = len(_data_list)
        print('Send length:{}'.format(_send_len))

    def parse_recv(self):
        _data = self.recv_data[self.recv_data.find('68 64'):]
        # _data = _data.split(' ')
        # _data = [int(x, 16) for x in _data]
        # _data = bytes(_data)
        # with open('dd.mn5', 'wb') as f:
        #     f.write(_data)
        head = _data[:50*3]
        code = _data[50*3:64*3]
        last = _data[64*3:] 
        print('head:{}'.format(head))
        print('body:{}'.format(code))
        print('last:{}'.format(last))


if __name__ == '__main__':
    res = ParseRequest()
