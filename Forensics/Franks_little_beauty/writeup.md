
## Frank's little beauty - Writeup

We are given a memory dump file - MemDump.DMP, which we'll be using a tool called [Volatilty](https://github.com/volatilityfoundation/volatility) on

Running ```volatility -f MemDump.DMP --profile=Win7SP1x64 imageinfo``` (the suggested profile) which verifies that Win7SP1x64 is the most suitable profile for this particular dump <br><br>

The slow typer is a hint to Frank relying on the clipboard feature to avoid typing
```volatility -f MemDump.DMP --profile=Win7SP1x64 clipboard```

>    1 WinSta0       CF_UNICODETEXT               0x300265 0xfffff900c1c0b4a0 https://pastebin.com/3Ecrm2DY  

Going to the [link](https://pastebin.com/3Ecrm2DY) leads us to part 1 of the flag: ```"p_ctf{v0l4t1l1ty"``` <br><br>

To have a look at the running processes:
```volatility -f MemDump.DMP --profile=Win7SP1x64 pslist``` <br>
The only noteworthy one seems to be WinRAR.exe. To see the file that was accessed with WinRAR:
```volatility -f MemDump.DMP --profile=Win7SP1x64 consoles | grep WinRAR.exe``` <br><br>
The file we're looking for is comp.rar. Running 
```volatility -f MemDump.DMP --profile=Win7SP1x64 filescan | grep comp.rar``` <br>
dumping it with:
```volatility -f MemDump.DMP --profile=Win7SP1x64 dumpfiles -n -Q 0x000000003df4e450 --dump-dir .``` <br>
and renaming the file to comp.rar, and running
```unrar e comp.rar```  but it needs a password. <br><br>

Frank reuses password, he must be using the same password for his computer account
```volatility -f MemDump.DMP --profile=Win7SP1x64 hashdump```
> Frank Reynolds:1000:aad3b435b51404eeaad3b435b51404ee:a88d1e18706d3aa676e01e5943d15911:::
>
a88d1e18706d3aa676e01e5943d15911 is the NTLM hash which can be decrypted [online](https://hashes.com/en/decrypt/hash) to obtain the password "trolltoll" <br>
```unrar e comp.rar```  with trolltoll gives us flag.png containing the second part of the flag: ```"_i5_v3ry_h4ndy_at"```

<br>

The question refernces a shortcut to paddys. In Windows 7, shortcuts have the extension '.lnk'. searching for 'paddys.lnk':
```volatility -f MemDump.DMP --profile=Win7SP1x64 filescan | grep -i "paddys.lnk"``` and dumping it with
```volatility -f MemDump.DMP --profile=Win7SP1x64 dumpfiles -n -Q 0x000000003e1891d0 --dump-dir .```
Opening it with a hex editor, we see that it points to C:\Program Files\Microsoft Games\Minesweeper\sysinfo.txt
<br><br>
Running ```volatility -f MemDump.DMP --profile=Win7SP1x64 filescan | grep sysinfo``` and dumping it with
```volatility -f MemDump.DMP --profile=Win7SP1x64 dumpfiles -n -Q 0x000000003ef7bce0 --dump-dir .```
but there's no file that gets dumped, indicating that it has been deleted.
<br><br>
We need to get the file from the MFT that NTFS systems use with
```volatility -f MemDump.DMP --profile=Win7SP1x64 mftparser | grep -C10 sysinfo > mftsysinfo```


> $STANDARD_INFORMATION
> Creation                       Modified                       MFT Altered                    Access Date                    Type
> ------------------------------ ------------------------------ ------------------------------ ------------------------------ ----
> 2022-02-07 15:58:00 UTC+0000 2022-02-07 14:07:12 UTC+0000   2022-02-07 15:59:56 UTC+0000   2022-02-07 15:58:00 UTC+0000   Archive
> 
> $FILE_NAME
> Creation                       Modified                       MFT Altered                    Access Date                    Name/Path
> ------------------------------ ------------------------------ ------------------------------ ------------------------------ ---------
> 2022-02-07 15:58:00 UTC+0000 2022-02-07 15:58:00 UTC+0000   2022-02-07 15:58:00 UTC+0000   2022-02-07 15:58:00 UTC+0000   Program Files\Microsoft > Games\Minesweeper\sysinfo.txt
> 
> $OBJECT_ID
> Object ID: e069804c-2e88-ec11-b47e-080027e4eb34
> Birth Volume ID: 80000000-3000-0000-0000-180000000100
> Birth Object ID: 15000000-1800-0000-5f72-333464316e67
> Birth Domain ID: 5f64756d-7035-5f69-6173-69707d000000
> 
> $DATA
> 0000000000: 5f 72 33 34 64 31 6e 67 5f 64 75 6d 70 35 5f 69   _r34d1ng_dump5_i  <br>
> 0000000010: 61 73 69 70 7d &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; &emsp;   asip}

We see the third part of the flag: "_r34d1ng_dump5_iasip}" <br><br>
Thus, the final flag is:  <br>
```p_ctf{v0l4t1l1ty_i5_v3ry_h4ndy_at_r34d1ng_dump5_iasip}```
