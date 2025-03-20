# coding=utf-8

import argparse
import copy
import os
from pypinyin import lazy_pinyin

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vocab_path", type=str, required=True)
    parser.add_argument("--expand", action="store_true")
    parser.add_argument("--polyphonic", action="store_true")
    parser.add_argument("--polyphonic_path", type=str, default=None)
    args = parser.parse_args()
    return args

def isChinese(ch):
    cp = ord(ch)
    if cp >= 0x4E00 and cp <= 0x9FA5:
        return True
    return False

def get_pinyin_dict(args):
    pinyin_dict = {}
    with open(args.vocab_path, mode='r', encoding='utf-8') as handle:
        for line in handle:
            token = line.strip()
            if len(token) != 1 or not isChinese(token):
                continue
            pinyin = lazy_pinyin(token)[0]
            if pinyin in pinyin_dict:
                pinyin_dict[pinyin].append(token)
            else:
                pinyin_dict[pinyin] = [token]

    if args.polyphonic:
        assert args.polyphonic_path is not None
        assert os.path.exists(args.polyphonic_path)
        with open(args.polyphonic_path, mode='r', encoding='utf-8') as handle:
            for line in handle:
                line = line.strip().split()
                for pinyin in line[1:]:
                    if pinyin in pinyin_dict:
                        pinyin_dict[pinyin].append(line[0])
                    else:
                        pinyin_dict[pinyin]=[line[0]]

    # z->zh c->ch s->sh
    res = copy.deepcopy(pinyin_dict)
    for key, val in pinyin_dict.items():
        if key.startswith('zh'):
            pinyin = 'z' + key[2:]
            if pinyin in pinyin_dict:
                res[key].extend(pinyin_dict[pinyin])
        elif key.startswith('ch'):
            pinyin = 'c' + key[2:]
            if pinyin in pinyin_dict:
                res[key].extend(pinyin_dict[pinyin])
        elif key.startswith('sh'):
            pinyin = 's' + key[2:]
            if pinyin in pinyin_dict:
                res[key].extend(pinyin_dict[pinyin])
        elif key.startswith('z'):
            pinyin = 'zh' + key[1:]
            if pinyin in pinyin_dict:
                res[key].extend(pinyin_dict[pinyin])
        elif key.startswith('c'):
            pinyin = 'ch' + key[1:]
            if pinyin in pinyin_dict:
                res[key].extend(pinyin_dict[pinyin])
        elif key.startswith('s'):
            pinyin = 'sh' + key[1:]
            if pinyin in pinyin_dict:
                res[key].extend(pinyin_dict[pinyin])

    if args.expand:
        # l->n f->h an->ang in->ing en->eng
        for key, val in pinyin_dict.items():
            if key[0] == 'l':
                pinyin = 'n' + key[1:]
                if pinyin in pinyin_dict:
                    res[key].extend(pinyin_dict[pinyin])
            elif key[0] == 'n':
                pinyin = 'l' + key[1:]
                if pinyin in pinyin_dict:
                    res[key].extend(pinyin_dict[pinyin])
            elif key[0] == 'f':
                pinyin = 'h' + key[1:]
                if pinyin in pinyin_dict:
                    res[key].extend(pinyin_dict[pinyin])
            elif key[0] == 'h':
                pinyin = 'f' + key[1:]
                if pinyin in pinyin_dict:
                    res[key].extend(pinyin_dict[pinyin])
            if key.endswith('ang'):
                pinyin = key[:-3] + 'an'
                if pinyin in pinyin_dict:
                    res[key].extend(pinyin_dict[pinyin])
            elif key.endswith('ing'):
                pinyin = key[:-3] + 'in'
                if pinyin in pinyin_dict:
                    res[key].extend(pinyin_dict[pinyin])
            elif key.endswith('eng'):
                pinyin = key[:-3] + 'en'
                if pinyin in pinyin_dict:
                    res[key].extend(pinyin_dict[pinyin])
            elif key.endswith('an'):
                pinyin = key[:-2] + 'ang'
                if pinyin in pinyin_dict:
                    res[key].extend(pinyin_dict[pinyin])
            elif key.endswith('in'):
                pinyin = key[:-2] + 'ing'
                if pinyin in pinyin_dict:
                    res[key].extend(pinyin_dict[pinyin])
            elif key.endswith('en'):
                pinyin = key[:-2] + 'eng'
                if pinyin in pinyin_dict:
                    res[key].extend(pinyin_dict[pinyin])
    return res

if __name__ == '__main__':
    args = parse_args()
    char_dict = {}
    pinyin_dict = get_pinyin_dict(args)
    for pinyin, char_list in pinyin_dict.items():
        if len(char_list) < 2:
            continue
        chars = list(set(char_list))
        for i in range(len(chars)):
            ch = chars[i]
            chars[i] = chars[0]
            chars[0] = ch
            if ch in char_dict:
                val = char_dict[ch]
                val.extend(chars[1:])
                char_dict[ch] = list(set(val))
            else:
                char_dict[ch] = chars[1:]

    for key, val in char_dict.items():
        print('{} {}'.format(key, ''.join(val)))

