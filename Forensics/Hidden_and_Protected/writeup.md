## PCTF '22

#### "Hidden and Protected" Write-up


On performing binwalk on image.png, with:
```
binwalk --dd='.*' -e image.png
```
We obtain the files "Double_Encrypted_Password.txt" and "image2.jpeg"

On examining image2.jpeg with exiftool with:
```
exiftool image2.jpeg
```

We notice it says  "Comment : Steghide FTW", but we need a passphrase to extract the files with steghide.
It also says "Author: Nero, Caligula, Julius, Augustus", who are all Caesars, indiacting the presence of a Caesar's cipher somewhere.


Double_Encrypted_Password.txt contains the following:
```
ABBBAABABBBAABABAABABABABAAAAAABBBAABABBBBAAAABABB
```

The presence of only A's and B's indicates its a Baconian cipher, which when deciphered, yields:
OLSSVAOLYL, which needs to be decrypted again (as it's double encrypted).

Decrypting it with Caesar's Cipher (N = 7, the only N where the passphrase resembles words), we obtain the passphrase: HELLOTHERE

Extracting from image2.jpeg with steghide:
```
steghide extract -sf image2.jpeg
```
with the passphrase: HELLOTHERE which reveals flag.txt, containing:
```
p_ctf{G3N3R4L_K3N0B1_TH3_N3G0T14T0R}
```
