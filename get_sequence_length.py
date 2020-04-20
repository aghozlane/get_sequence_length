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
"""Get sequence length"""
from __future__ import print_function
import os
import sys
import argparse
import gzip

__author__ = "Amine Ghozlane"
__copyright__ = "Copyright 2014, INRA"
__credits__ = ["Amine Ghozlane"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Amine Ghozlane"
__email__ = "amine.ghozlane@jouy.inra.fr"
__status__ = "Developpement"

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
    parser.add_argument('-n', dest='fullname', action="store_true",
                        default=False, help='Keep sequence annotation (Default cut after space).')
    parser.add_argument('-f', dest='fastq', action="store_true",
                        default=False, help='Input is a fastq file and not a fasta file.')
    args = parser.parse_args()
    return args

def parse_fasta_file(fasta_file, output_file, fullname, fastq):
    """
    """
    if not output_file:
        output = sys.stdout
    else:
        output = open(output_file, "wt")
    header = ""
    annotation = ""
    seq_len_tab = []
    try:
        if fasta_file.endswith(".gz"):
            fast = gzip.open(fasta_file, "rt")
        else:
            fast = open(fasta_file, "rt")
        for line in fast:
            if line.startswith(">") and not fastq:
                if len(header) > 0:
                    seq_len = len(sequence)
                    if fullname:
                        print("{0}\t{1}\t{2}".format(header, annotation, seq_len),
                               file=output)
                    else:
                        print("{0}\t{1}".format(header, seq_len), file=output)
                    seq_len_tab.append(seq_len)
                header = line[1:].replace("\n", "").replace("\r", "").split(" ")[0]
                annotation = " ".join(line[1:].replace("\n", "").replace("\r", "").split(" ")[1:])
                sequence = ""
            elif fastq:
                # sequence
                seq_len_tab.append(len(fast.next()))
                fast.next()
                fast.next()
            else:
                sequence += line.replace("\n", "").replace("\r", "")
        if header != "":
            seq_len = len(sequence)
            if fullname:
                print("{0}\t{1}\t{2}".format(header, annotation, seq_len),
                              file=output)
            else:
                print("{0}\t{1}".format(header, seq_len), file=output)
            seq_len_tab.append(seq_len)
        fast.close()
    except IOError:
        sys.exit("Error cannot open {0}".format(fasta_file))
    if output_file:
        output.close()
    #print(sum(seq_len_tab))
    print("Mean value:{1}{0}Median value:{2}{0}Max value:{3}{0}Min value:{4}".format(
          os.linesep, sum(seq_len_tab)/len(seq_len_tab),
          sorted(seq_len_tab)[len(seq_len_tab)//2], max(seq_len_tab), min(seq_len_tab)))
    return seq_len_tab

def N50(numlist):
    """
    Abstract: Returns the N50 value of the passed list of numbers.
    Usage:    N50(numlist)
    Based on the Broad Institute definition:
    https://www.broad.harvard.edu/crd/wiki/index.php/N50
    """
    numlist.sort()
    newlist = []
    for x in numlist :
        newlist += [x]*x
    # take the mean of the two middle elements if there are an even number
    # of elements.  otherwise, take the middle element
    if len(newlist) % 2 == 0:
        medianpos = len(newlist)/2
        return float(newlist[medianpos] + newlist[medianpos-1]) /2
    else:
        medianpos = len(newlist)/2
        return newlist[medianpos]

def main():
    """Main program
    """
    args = getArguments()
    seq_len_tab = parse_fasta_file(args.fasta_file, args.output_file,
                                   args.fullname, args.fastq)
    assert N50([2, 2, 2, 3, 3, 4, 8, 8]) == 6
    n50_result = N50(seq_len_tab)
    print("N50:{0}".format(int(n50_result)))
if __name__ == '__main__':
    main()
