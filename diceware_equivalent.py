#! /usr/bin/env python3
################################################################################
# Copyright (c) 2017, Alan Barr
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
################################################################################

import os
import argparse
import urllib.request
from random import SystemRandom
from math import log,ceil
import textwrap

NUM_DICE            = 5
DICE_SIDES          = 6
DICT_SIZE           = DICE_SIDES**NUM_DICE
NUM_PRINTABLE_ASCII = 126 - 32 + 1
EFF_LIST_URL        = "https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt"

def entropy_of_random_ascii(ascii_symbols, string_length):
    single_ascii_entropy = log(ascii_symbols,2)
    return single_ascii_entropy * string_length

def entropy_of_diceware(words):
    single_word_entropy = log(DICT_SIZE,2)
    return words * single_word_entropy

def words_for_equiv_entropy(desired_entropy):
    passphrase_entropy = log(DICT_SIZE, 2)
    num_words = desired_entropy / passphrase_entropy
    return num_words

def avg_dict_value_length(dictionary):
    total_chars = 0
    for key,value in dictionary.items():
        total_chars += len(value)
    average_chars = float(total_chars) / len(dictionary)
    return average_chars

def download_dictionary(url, filename):
    req = urllib.request.urlopen(url)
    with open(filename, "b+w") as f:
        f.write(req.read())

def to_dictionary(text):
    dictionary = {}
    for line in text.split("\n"):
        if len(line) > DICE_SIDES:
            num, word = line.split("\t")
            dictionary[num] = word

    if (len(dictionary)) != DICT_SIZE:
        print("Dictionary had %u entries", len(dictionary))
        raise ValueError

    return dictionary

def get_dictionary(url):
    filename = "./" + os.path.basename(url)

    if not os.path.isfile(filename):
        print("Word list does not exist, downloading...")
        download_dictionary(url, filename)

    with open(filename) as f:
        page = f.read()
    return to_dictionary(page)

def diceware_password(dictionary, throws):
    sr = SystemRandom()
    passphrase = []

    for i in range(throws):
        key = ""
        for i in range(NUM_DICE):
            key += str(sr.randint(1,6))
        passphrase += [dictionary[key]]

    return passphrase

def cli_parser():
    parser = argparse.ArgumentParser(
            formatter_class = argparse.RawTextHelpFormatter,
            description=textwrap.dedent("""
            Calculates Diceware equivalents to a *random* password. The
            specification of the random password is provided via user input.
            The Diceware calculations are based on the EFF's long Diceware list. See:
            https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases

            This also creates an example Diceware password. The calculations for
            this are based on the next best entropy of the user input parameters.

            For more information, see the accompanying README.md.
            """))

    parser.add_argument(
        "--symbols",
        nargs=1,
        type=int,
        help=textwrap.dedent("""
        The number of different symbols available to the random password.

        For a pin code, the digits 0-9, this is 10.
        For a symbol-less ASCII set, "a-z A-Z 0-9", this is 62.
        For the largest printable ASCII set, this is 95 (the default).
        For Diceware this is the number of words in the dictionary - not the 
         number of characters.

        """),
        default=[NUM_PRINTABLE_ASCII])

    parser.add_argument(
        "--length",
        nargs=1,
        type=int,
        help=textwrap.dedent("""
        The length of the sequence of symbols.

        For a pin code this is the number of digits, e.g. ATMs use 4.
        For an ASCII password this is the number of characters used.
        For Diceware this is the word count.

        This defaults to 12.
        """),
        default=[12])

    return parser.parse_args()

def main():

    args = cli_parser()

    dictionary      = get_dictionary(EFF_LIST_URL)
    average_chars   = avg_dict_value_length(dictionary)
    entropy         = entropy_of_random_ascii(args.symbols[0],
                                              args.length[0])
    req_words       = words_for_equiv_entropy(entropy)
    phrase_len      = req_words * average_chars

    print("A random ASCII password of length {:d} generated from {:d} symbols".format(args.length[0], args.symbols[0]))
    print("  Has Entropy:                       {0:.2f}".format(entropy))
    print("  Requires diceware words:           {0:.2f}".format(req_words))
    print("  Average diceware word length:      {0:.2f}".format(average_chars))
    print("  Estimated length of passphrase:    {0:.2f}".format(phrase_len))
    print("")

    throws          = ceil(req_words)
    passphrase      = diceware_password(dictionary, throws)
    throws_entropy  = entropy_of_diceware(throws)
    passphrase_len  = length = sum(len(w) for w in passphrase)

    print("Example diceware passphrase with:")
    print("  words:     {}".format(throws))
    print("  length:    {}".format(passphrase_len))
    print("  entropy:   {0:.2f}".format(throws_entropy))
    print("")

    single_string = ""
    for i in passphrase:
        print("  " + i)
        single_string += i
    
    print("")
    print("  " + single_string)
    print("")

    return 0

if __name__ == "__main__":
    main()
