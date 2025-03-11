# coding=utf-8

import argparse
from tqdm import tqdm
from pypinyin import lazy_pinyin

def isChinese(word):
    for ch in word:
        cp = ord(ch)
        if cp >= 0x4E00 and cp <= 0x9FA5:
            continue
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    args = parser.parse_args()

    pinyin_dict = {}
    with open(args.input, mode='r', encoding='utf-8') as handle:
        for line in tqdm(handle):
            word = line.strip()
            if len(word) != 2 or not isChinese(word):
                continue
            pinyin = '_'.join(lazy_pinyin(word))
            if pinyin in pinyin_dict:
                pinyin_dict[pinyin].append(word)
            else:
                pinyin_dict[pinyin] = [word]

    for pinyin, words in pinyin_dict.items():
        if len(words) < 2:
            continue
        print(' '.join(words))
        for i in range(1, len(words)):
            word = words[0]
            words[0] = words[i]
            words[i] = word
            print(' '.join(words))

