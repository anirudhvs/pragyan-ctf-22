
## Ye Olde Threat - Writeup

The string in intel.txt (```aHR0cHM6Ly9kcml2ZS5nb29nbGUuY29tL2ZpbGUvZC8xQUVremJqV1JDZFVwNEY3ZjJ3dExnSWQyd2RTRlkwUXE=```) seems to be BASE64 encoded. On decoding it, we get 
```https://drive.google.com/file/d/1AEkzbjWRCdUp4F7f2wtLgId2wdSFY0Qq``` which gives us intel.zip.

Its only content is Just_A_Plane_Image.png which can't be opened, due to it being corrupted. On opening it with a hex editor, we see that the PNG header and some of the chunks are incorrect.


Replacing the PNG header to: **89 50 4E 47 0D 0A 1A 0A**

IHDR chunk: **49 48 44 52**  from 31 48 44 72 (at 0x0000000C - 0x0000000F)

IDAT chunk: **49 44 41 54**  from 31 64 61 37 (at 0x00000025 - 0x00000028)


The image still cannot be opened, though. Running pngcheck on it with:

```
pngcheck -v Just_A_Plane_Image.png
```

> chunk IDAT at offset 0x02031, length 134285570
> 
> :  EOF while reading data


This indicates that the size of the IDAT chunk is incorrect. Corrected size of IDAT chunk: 

0x00002035 to 0x00004034 = 8192 bytes = 00 00 20 00 in hexadecimal

**00 00 20 00** from 08 01 09 02 (at 0x0000202D - 0x00002030)

Running pngcheck on it again:

> chunk IDAT at offset 0x0403d, length 8192
> 
> CRC error in chunk IDAT (computed a89b381a, expected f64839a4)

corrected CRC chunk (at 0x00006041-0x00006044) should be:
**A8 9B 38 1A**  


The image seems to be fine now. It depicts an artwork of an expoding earth, but the name "Just_A_Plane_Image" seems to hint at something to do with the bit planes of the image.

On browsing all the bitplanes of the image (with a tool like https://stegonline.georgeom.net), we find the flag on the Blue-2 bit plane.

The flag is 
```
p_ctf{K@nye_w@nt5_To_Buy_Th3_3n71r3_E4rth}
```

