## Zipped Scandal - Writeup


The zip files are neted in the order Aa, Ab, Ac, ... ,Az, Ba, Bb ...Bz, Ca, ... Zz.zip

Unzipping them with a simple bash script:
```bash
for char1 in {A..Z}
do

    for char2 in {a..z}
    do
        unzip ${char1}${char2}.zip
        rm ${char1}${char2}.zip        
    done
done
```
This reveals Checkpoint.zip- containing Final.zip (which is password protected) and Image.jpeg

Examining Image.jpeg (which seems to hint at a location) with
```
exiftool Image.jpeg
```

The fields that stand out are:

> Comment                         : b3abe5d8c69b38733ad57ea75e83bcae42bbbbac75e3a5445862ed2f8a2cd677
>
> GPS Position                    : 36 deg 20' 21.49" N, 96 deg 48' 10.32" W


A quick search of ```b3abe5d8c69b38733ad57ea75e83bcae42bbbbac75e3a5445862ed2f8a2cd677``` reveals that it is the SHA-256 hash of the phrase "SHA256"

Navigating to the given GPS co-ordinates on Google Maps, reveal it belongs to the "Pawnee City Hall", whose SHA-256 hash is ```b321a8b402ed2b78584a824b8558bb11177d7ea5985646d06787a91c86c8afca```, which is the password of Final.zip

Final.zip contains Image.png, which appears to be a completely black image on first glance. However on opening it with GIMP, using the colour picker tool, we notice two distinct but similar colours- **#000000** and **#060606**. 

On changing the **#060606** regions to **#ffffff** (In Gimp, Colors > Map > 'Colour Exchange' > #060606 to #ffffff), we obtain a QR code.

Scanning it leads us to hint.txt and audio.mp3, which resembles morse code. On decoding it with a morse audio decoder, we obtain a random string that leads nowhere. Moreover, we also notice that not all the characters in the audio file have a corresponding text output. 


Hint.txt contains the quote “ … Fast as we can. Really put the pedal to the metal, you know! Bill and Ted did it.” A web search of it lead us to the 'Going Backwards For Once' section of https://readyplayerone.fandom.com/wiki/Halliday%27s_Easter_Egg_Hunt. The challenge, according to the webpage, was won by moving in the reverse direction.

On reversing and then decoding the audio morse file, we obtain ```ic3t0wnc0stsic3cl0wnhist0wncr0wn```

Thus, the flag is 
```
p_ctf{ic3t0wnc0stsic3cl0wnhist0wncr0wn}
```
