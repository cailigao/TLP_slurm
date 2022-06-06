#!/usr/bin/python
# -*- coding:utf-8 -*-
import argparse
from pathlib import Path


def main(args):
    print(args.input.read_text())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True, help='input file')
    parser.add_argument('-o', '--output', type=str, required=True, help='output file')

    args = parser.parse_args()
    args.input = Path(args.input).resolve()
    args.output = Path(args.output).resolve()
    main(args)
