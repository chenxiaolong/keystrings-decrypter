keystrings-decrypter
====================

keystrings-decrypter is a simple tool for decrypting `*_keystrings.dat` files from TouchWiz.


File format
-----------

The `keystrings.dat` file is an encrypted XML file describing various dialer codes and which Android packages are associated with them. It consists of 64-byte RSA-encrypted blocks without any headers or padding. The RSA modulus and private exponent are stored in `assets/mod_pri_key.txt` and `assets/exp_pri_key.txt` within `/system/app/DRParser.apk` from any TouchWiz ROM.


Usage
-----

The Python script does the RSA decryption itself and has no dependencies other than Python 3 itself. To decrypt the keystrings file, first extract the RSA modulus and private exponent files described above from `DRParser.apk`. Then run the script as follows:

```sh
python3 keystrings-decrypter.py \
    --rsa-mod-file /path/to/mod_pri_key.txt \
    --rsa-priv-exp-file /path/to/exp_pri_key.txt \
    -i /path/to/keystrings.dat \
    -o output.xml
```

The modulus and exponent can also be specified directly via the `--rsa-mod` and `--rsa-priv-exp` options. If `-i` is omitted, input is taken from stdin. Similarly, if `-o` is omitted, the decrypted file is output to stdout.
