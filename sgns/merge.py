
from tqdm import tqdm

def isChinese(word):
    for ch in word:
        cp = ord(ch)
        if cp >= 0x4E00 and cp <= 0x9FA5:
            continue
        return False
    return True

sogou = set()
with open('sgns.sogounews.words', mode='r', encoding='utf-8') as handle:
    for line in tqdm(handle):
        line = line.strip()
        if len(line) == 2 and isChinese(line):
            sogou.add(line)

baidu = set()
with open('sgns.baidubaike.words', mode='r', encoding='utf-8') as handle:
    for line in tqdm(handle):
        line = line.strip()
        if len(line) == 2 and isChinese(line):
            baidu.add(line)

s = sogou & baidu
for word in s:
    print(word)

