#!/usr/bin/env python3

# Copyright (C) 2018  Andrew Gunnerson <andrewgunnerson@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import contextlib
import sys


def read_be_int_from_file(path):
    """
    Read arbitrary big-endian encoded integer from file
    """
    with open(path, 'rb') as f:
        return int.from_bytes(f.read(), byteorder='big')


@contextlib.contextmanager
def open_or_use(*args, **kwargs):
    """
    Open a file or use an alternate file-like object if no path is specified

    Takes any parameters accepted by open() in addition to an `alt` keyword
    argument for specifying the altnernate file-like object.
    """
    alternate = kwargs['alt']
    del kwargs['alt']

    if args and args[0]:
        fh = open(*args, **kwargs)
    else:
        fh = alternate

    try:
        yield fh
    finally:
        if fh is not alternate:
            fh.close()


def encrypted_blocks(file_obj):
    """
    Iterate through 64-byte blocks in file_obj
    """
    while True:
        data = file_obj.read(64)
        if not data:
            break
        yield data


def main():
    parser = argparse.ArgumentParser()

    # RSA modulus
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--rsa-mod', type=int,
                       help='RSA modulus')
    group.add_argument('--rsa-mod-file',
                       help='RSA modulus file')

    # RSA private exponent
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--rsa-priv-exp', type=int,
                       help='RSA private exponent')
    group.add_argument('--rsa-priv-exp-file',
                       help='RSA private exponent file')

    # Optional input/output file arguments
    parser.add_argument('-i', '--input-file',
                        help='Encrypted keystrings file (default: stdin)')
    parser.add_argument('-o', '--output-file',
                        help='Decrypted keystrings file (default: stdout)')

    args = parser.parse_args()

    if args.rsa_mod_file:
        rsa_mod = read_be_int_from_file(args.rsa_mod_file)
    else:
        rsa_mod = args.rsa_mod

    if args.rsa_priv_exp_file:
        rsa_priv_exp = read_be_int_from_file(args.rsa_priv_exp_file)
    else:
        rsa_priv_exp = args.rsa_priv_exp

    with open_or_use(args.output_file, 'wb', alt=sys.stdout.buffer) as fout:
        with open_or_use(args.input_file, 'rb', alt=sys.stdin.buffer) as fin:
            for block in encrypted_blocks(fin):
                c = int.from_bytes(block, byteorder='big')
                m = pow(c, rsa_priv_exp, rsa_mod)
                bits = m.bit_length()

                fout.write(m.to_bytes((bits + 7) // 8, byteorder='big'))


if __name__ == '__main__':
    main()
