#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

import pandas as pd
import numpy as np

class Quantile():
    """
    Quantile information
    """
    def __init__(self, freqs):
        self.freqs = freqs

    def quantiles(self, quantiles=2):
        """
        Find the quantiles of a list of frequencies
        """
        self.freqs['inst_frac'] = (self.freqs.instances.cumsum() /
                                   self.freqs.instances.sum())
        cuts = np.linspace(0.0, 1.0, num=quantiles+1)
        self.freqs['quantile'] = pd.cut(self.freqs.inst_frac,
                                        cuts,
                                        include_lowest=True,
                                        labels=False)
        return self.freqs['quantile'].value_counts(ascending=True).tolist()

    def head(self, quantiles=2):
        """
        List the queries comprising the top quantile
        """
        quantiles = self.quantiles(quantiles)
        return self.freqs['query'].head(quantiles[0]).tolist()

    def tail(self, quantiles=2):
        """
        List the queries comprising the bottom quantile
        """
        quantiles = self.quantiles(quantiles)
        return self.freqs['query'].tolist()[sum(quantiles[:-1]):]

    def middle(self, quantiles=3):
        """
        List the queries comprising the quantiles between
        the top and bottom quantiles
        """
        if(quantiles < 3):
            raise ValueError("quantiles must be greater than 2")
        quantiles = self.quantiles(quantiles)
        return self.freqs['query'].tolist()[quantiles[0]:sum(quantiles[:-1])]


def main():
    import sys
    import argparse
    import fileinput

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command',
                                       help='available commands')

    quantile = subparsers.add_parser('quantiles')
    quantile.add_argument('filename', nargs='?',
                          help='file to read, if empty, stdin is used')
    quantile.add_argument('-q', '--quantiles',
                          type=int, default=2,
                          help='file to read, if empty, stdin is used')
    head = subparsers.add_parser('head')
    head.add_argument('filename', nargs='?',
                      help='file to read, if empty, stdin is used')
    head.add_argument('-q', '--quantiles',
                      type=int, default=2,
                      help='file to read, if empty, stdin is used')
    tail = subparsers.add_parser('tail')
    tail.add_argument('filename', nargs='?',
                      help='file to read, if empty, stdin is used')
    tail.add_argument('-q', '--quantiles',
                      type=int, default=2,
                      help='file to read, if empty, stdin is used')
    middle = subparsers.add_parser('middle')
    middle.add_argument('filename', nargs='?',
                        help='file to read, if empty, stdin is used')
    middle.add_argument('-q', '--quantiles',
                        type=int, default=3,
                        help='file to read, if empty, stdin is used')

    args = parser.parse_args()

    freq_file = args.filename or sys.stdin
    freqs = pd.read_csv(freq_file, usecols=['query', 'instances'])
    quantile = Quantile(freqs)
    if args.command == 'quantiles':
        counter = 1
        for q in quantile.quantiles(args.quantiles):
            sys.stdout.write(str(counter) + '\t' + str(q) + '\n')
            counter += 1
    elif args.command == 'head':
        for q in quantile.head(args.quantiles):
            sys.stdout.write(q + '\n')
    elif args.command == 'tail':
        for q in quantile.tail(args.quantiles):
            sys.stdout.write(q + '\n')
    elif args.command == 'middle':
        for q in quantile.middle(args.quantiles):
            sys.stdout.write(q + '\n')


if __name__ == "__main__":
    main()
