# coding=utf-8

import argparse
from tqdm import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    args = parser.parse_args()

    with open(args.input, mode='r', encoding='utf-8') as handle:
        for line in tqdm(handle):
            line = line.strip().split()
            word = line[0]
            data = [word]
            for w in line[1:]:
                if w[0] in word or w[1] in word:
                    data.append(w)
            if len(data) > 1:
                print(' '.join(data))

