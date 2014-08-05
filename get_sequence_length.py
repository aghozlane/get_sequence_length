#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    A copy of the GNU General Public License is available at
#    http://www.gnu.org/licenses/gpl-3.0.html
from __future__ import print_function
import os
import sys
import argparse

def isfile(path):
    """Check if path is an existing file.
      Arguments:
          path: Path to the file
    """
    if not os.path.isfile(path):
        if os.path.isdir(path):
            msg = "{0} is a directory".format(path)
        else:
            msg = "{0} does not exist.".format(path)
        raise argparse.ArgumentTypeError(msg)
    return path


def getArguments():
    """Retrieves the arguments of the program.
      Returns: An object that contains the arguments
    """
    # Parsing arguments
    parser = argparse.ArgumentParser(description=__doc__, usage=
                                     "{0} -h".format(sys.argv[0]))
    parser.add_argument('-i', dest='fasta_file', type=isfile, required=True,
                        help='Path to the query file.')
    parser.add_argument('-o', dest='output_file', type=str, default="",
                        help='Output file.')
    args = parser.parse_args()
    return args


def parse_fasta_file(fasta_file, output_file):
    """
    """
    if not output_file:
        output = sys.stdout
    else:
        output = open(output_file, "wt")
    header = ""
    seq_len_tab = []
    try:
        with open(fasta_file, "rt") as fast:
            for line in fast:
                if line[0] == ">":
                    if len(header) > 0:
                        seq_len = len(sequence)
                        print("{0}\t{1}".format(header, seq_len),
                              file=output)
                        seq_len_tab.append(seq_len)
                    header = line[1:].replace("\n", "").replace("\r", "").split(" ")[0]
                    sequence = ""
                else:
                    sequence += line.replace("\n", "").replace("\r", "")
    except IOError:
        sys.exit("Error cannot open {0}".format(fasta_file))
    if output_file:
        output.close()
    print("Mean value:{1}{0}Median value:{2}{0}".format(
          os.linesep, sum(seq_len_tab)/len(seq_len_tab),
          sorted(seq_len_tab)[len(seq_len_tab)//2]))


def main():
    """Main program
    """
    args = getArguments()
    parse_fasta_file(args.fasta_file, args.output_file)


if __name__ == '__main__':
    main()