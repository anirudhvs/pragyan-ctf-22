# Pragyan CTF 2022: Lost Flag
## Write-Up

1) On exploring the challenge, you will find that this is just a site which displays all the countries flag. And it also has a feature of reporting the URL endpoint which Casshe will visit in search of challenge flag.

2) On reading the challenge description proper you will find few words which sounds similar to CACHE (eg. cash, casshe). By this we get to know that this challenge is something related to CACHING.

3) To find where the pctf flag is located, lets first try to visit /flag route. 

4) On visiting that page, it tells
```
    Only admin can view this!
```

5) Since only admin can visit that page, we can report it. Also in description it was mentioned that, 
```
Casshe(admin) may not be searching properly so do visit that page again.
```

6) So on revisiting the same route /flag , we will notice a change in the message which tell that,
```
You are missing few characters in endpoint and those charaters should satisfy what a strong password contains.
```

7) But on reloading after few seconds (ie., after 10 seconds of reporting), you will again see the first warning message which says 
```
Only admin can view this!
```

8) By this what we infer is that, on reporting admin is visiting that endpoint which is getting cached. And that cache version is displayed for us when we revisit the page within 10seconds of reporting.

9) Now our ultimate aim is to find the missing few characters. Since it says characteristics of strong password, we can take the following cases
```
At least one upper case English letter, (?=.*?[A-Z])
At least one lower case English letter, (?=.*?[a-z])
At least one digit, (?=.*?[0-9])
At least one special character, (?=.*?[?!@$%^&*-])
Minimum eight in length .{8,} (with the anchors)
```
and by appending the endpoint with some extension ( .html, .css, .js, .txt ).

10) Now on reporting an endpoint with those conditions (eg. flag@dumy$1B.html), admin will visit the page and it will get cached. On revisiting the route, we will get the flag for this challenge.

Flag is
```
p_ctf{w3b_c4ch3_p0is1on1ng_1s_m0r3_d4ng3r}
```