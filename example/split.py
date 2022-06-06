#!/usr/bin/python
# -*- coding:utf-8 -*-
import argparse
from pathlib import Path


def main(args):
    with args.input.open() as read:
        id = 1
        count = 0
        line = read.readline()
        while line:
            with (args.data / str(id)).open(mode='a') as write:
                write.write(line)
            line = read.readline()

            count += 1
            if count == 2000:
                count = 0
                id += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True, help='input path')
    parser.add_argument('-o', '--data', type=str, required=True, help='small data path')

    args = parser.parse_args()
    args.input = Path(args.input).resolve()
    args.data = Path(args.data).resolve()
    args.data.mkdir(parents=True, exist_ok=True)
    main(args)
