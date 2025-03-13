
import argparse
from ltp import LTP
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--ltp_model', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
args = parser.parse_args()

ltp = LTP(args.ltp_model)
output = open(args.output, mode='w')

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
        word = line.strip()
        if len(word) != 2 or not isChinese(word):
            continue
        # 去除人名地名
        res = ltp.pipeline(word, tasks=["cws", "pos"])
        cws = res.cws
        pos = res.pos
        if len(cws) == 1 and pos[0] in ['nh', 'ns']:
            continue
        sogou.add(word)

baidu = set()
with open('sgns.baidubaike.words', mode='r', encoding='utf-8') as handle:
    for line in tqdm(handle):
        word = line.strip()
        if len(word) != 2 or not isChinese(word):
            continue
        # 去除人名地名
        res = ltp.pipeline(word, tasks=["cws", "pos"])
        cws = res.cws
        pos = res.pos
        if len(cws) == 1 and pos[0] in ['nh', 'ns']:
            continue
        baidu.add(word)

jieba = set()
with open('../jieba/jieba_dict.txt', mode='r', encoding='utf-8') as handle:
    for line in tqdm(handle):
        line = line.strip().split()
        assert len(line) == 3
        word, count, pos = line
        count = int(count)
        if len(word) != 2 or not isChinese(word):
            continue
        # 去除人名地名
        if count < 5 or pos.startswith('nr') or pos.startswith('ns'):
            continue
        jieba.add(word)

s = (sogou & baidu).union(jieba)
for word in s:
    output.write(word)
    output.write('\n')

