#  Diceware Passphrases

In recent episodes of Security Now, a podcast I happen to listen to, the
strength of Diceware generated passphrases has been discussed. 

The relevant podcasts being:

* [SN #594 A Look into PHP Malware](https://twit.tv/shows/security-now/episodes/594)                 ([transcript](https://www.grc.com/sn/sn-594.htm))
* [SN #595 What's Up With Whatsapp](https://twit.tv/shows/security-now/episodes/596?autostart=false) ([transcript](https://www.grc.com/sn/sn-595.htm))
* [SN #596 Password Complexity](https://twit.tv/shows/security-now/episodes/596?autostart=false)     ([transcript](https://www.grc.com/sn/sn-596.htm))

I feel the point being made on the podcast may have become a little muddled
across the shows. I believe the point wasn't that Diceware passphrases are weak,
but that a *secure* Diceware passphrase requires more ASCII characters than a
randomly generated string. 
The key problem with Diceware passphrases being when websites limit the maximum
length of a password, which can dramatically reduce the effectiveness of a
passphrase. 

# Overview of diceware_equivalent.py

In an attempt to make the comparison between passwords and Diceware passphrases
I threw together the diceware_equivalent.py script.
This script calculates the size of an equivalent entropy Diceware passphrase
required to replace a password. The assumption made is that the the password
being replaced was randomly generated.

It uses the
[EFF's long wordlist](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases)
for it's word length calculations and the *example* Diceware passphrase.

The Python script takes the arguments:

* `--symbols` - The number of symbols available in the dictionary
* `--length`  - The number of symbols used to form the password
* `-h` - Print help information.

## 95 Symbols, Length 12

A password of length 12, randomly generated from the 95 printable ASCII symbols,
has an entropy of 78.84.
Using this script, an equivalent passphrase of the same entropy
would require 6.10 randomly chosen words, averaging 42.65 characters. Not chosing
a .10 fraction of a word, to get at *least* the same entropy we need to chose 7
Diceware words. This would on average be a string 49 characters long.

##  62 Symbols, Length 10

Alternatively, a 10 character password randomly generated from:

* a-z
* A-Z
* 0-9

such as `ZQ2cIMGaU6` has an entropy of 59.54.

An Diceware replacement passphrase of entropy 64.62 can be formed from combining
the following 5 random words, totalling 37 characters.

* sixteen
* reluctant
* appraisal
* stylus
* tablet

A Diceware passphrase of equal strength to a password will undoubtedly require
more typing from the user. What is somewhat subjective though is if `ZQ2cIMGaU6`
is easier to remember than `sixteenreluctantappraisalstylustablet`.

The output_examples directory contains more examples of diceware_equivalent.py's
output.

# An Amateur's Guide to Entropy

(The amateur being me).

[Entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)) is a
measure of the unpredictability of a signal. A signal is comprised of a sequence
of symbols, which have been chosen from a known symbol list. Entropy is
ultimately the number of bits required to uniquely represent each symbol in the
list of all the symbols. It is assumed there is an equal chance of selecting any
symbol from the dictionary.

The calculation of the number of bits to represent each symbol in a list uses
logarithms, in particular log base 2. I will use `log_2()` to denote this
calculation here.

Taking `log_2()` of the total number of symbols available gives the required
number of bits required to represent each one.

When a signal (password) consists of multiple samples from the dictionary,
the total entropy of the signal can be calculated with:

    total entropy = number of samples * entropy of a single symbol

## Coin Toss Example

Consider a coin toss, the outcome of which can result in either Heads or Tails -
i.e. the size of the dictionary is 2. 

    log_2(2) = 1.

Therefore, only one bit is required to represent members of this dictionary.
You could for example, directly map:

    0 = Heads
    1 = Tails

The entropy of the results of 5 coin tosses is:

    5 * 1 = 5

## ATM Pin Code Example

ATM pin codes consist of four of the digits selected from the dictionary
`[0,1,2,3,4,5,6,7,8,9]`. I will assume (and hope) the bank generates this 
code completely randomly.

The entropy of a single symbol is:

    log_2(10) = 3.322

The entropy of a 4 digit pin is:

    4 * 3.322 = 13.288

## Lower Case Password Example

When a password is randomly generated from the letters `[a-z]`, each individual
character has entropy:

    log_2(26) = 4.700

A random 8 letter, lowercase password such as `vwrjearf` or `dbylruii` has an
entropy of:

    8 * 4.700 = 37.604

It's important to note that an 8 character dictionary word such as `password`
has significantly less entropy than one randomly generated.

## Random Octets Example

This is a silly example, included just to highlight the difference between a byte and the 
previous example of a lower case ASCII character.

An [octet](https://en.wikipedia.org/wiki/Octet_(computing)) (aka byte) is a
sequence of 8 bits. 8 bits can represent numerical values between 0 to 255,
permitting 256 possible values.

The entropy of a byte is (shockingly):

    log_2(256) = 8

While the total entropy of 8 random bytes is:

    8 * 8 = 64

# Password Strength and Diceware

Computers use ASCII symbols to represent letters. An ASCII character is
represented by a byte (8 bits). However, not all of the 256 possible values are
"printable" ASCII - such as the backspace character. In fact only 95 of them are
printable, which includes lowercase, uppercase, digits and symbols.
The symbol list for a password therefore comprises of 95 characters.

While a full byte has entropy of 8, a printable character has entropy of:

    log_2(95) = 6.570

We want to chose passwords which are hard to guess, which means we should aim to
use passwords with a high entropy.

To achieve that we should:

- have a large dictionary of symbols to chooe from
- randomly choose the symbols
- choose a long sequence of symbols

Unfortunately, for us mere mortals, the above three guidelines result in
passwords which are hard to remember.

This is where the concept of Diceware passphrases comes from. Instead of
creating a sequence by combining single letter symbols ("0", or "a") with
Diceware we combine words. The idea being a sequence of random words is easier
to remember than a random characters.

The entropy of a single symbol/word depends on the number of words in the
dictionary.

If, for example the dictionary contains the words:

    he thrusts his fists against the posts

then the entropy of a symbol from this dictionary is:

    log_2(7) = 2.807

Diceware typcially uses a much larger dictionary size that this in order to
achieve a higher entropy per word. 
The [EFF long wordlist](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases)
expects 5 throws of a six sided dice to map to a single word. 

This requires a dictionary of:

    6*6*6*6*6 = 7776 words

with the entropy of a single word being:

    log_2(7776) = 12.925
    
The accompanying Python script takes care of the crude calculations to easily
compare passwords to Diceware passphrases based on entropy calculations.

## Notes

Nobody wants to remember a unique, randomly generated password/passphrase for
every website they use. For security purposes, no one should be reusing the same
password across multiple websites.
So the general advice is to limit yourself to remembering 1 *strong* password,
to use as the master password for a password manager such as:

* [KeePass](http://keepass.info/)
* [LastPass](https://www.lastpass.com/)
* [1Password](https://1password.com/)

Utilise the password manager to generate long, high entropy passwords for all
the sites you use.
Troy Hunt makes this point in his 
[blog post](https://www.troyhunt.com/im-sorry-but-were-you-actually-trying/) 
which was written to address this [XKCD comic](https://xkcd.com/936/). He, like
Steve Gibson makes the point that many sites limit password length, which
prevents the use of a strong enough Diceware passphrase.

[This](http://www.netmux.com/blog/cracking-12-character-above-passwords) was 
the article which started the discussion on Security Now, and demonstrates the
vulnerability of using short passphrases.

For further reading, Wikipedia has a pretty detailed page on
[Password Strength](https://en.wikipedia.org/wiki/Password_strength).
 
Also of note, The United States National Institute for Standards and Technology
(NIST), is drafting
[new password guidelines](https://nakedsecurity.sophos.com/2016/08/18/nists-new-password-rules-what-you-need-to-know/)
for websites and those implementing authentication. Whether or not anyone
will follow it remains to be seen.

## Disclaimer

I find the field of software security interesting, hence why I listen to
Security Now. However I do not work in this field or have practical experience
in it, so please take anything said here with a pinch of salt.
