require 'sinatra/base'
require 'sinatra'
require 'jwt'
require "sinatra/cookies"
require "base64"

set :public_folder, File.join(File.dirname(__FILE__), 'public')
set :views, File.join(File.dirname(__FILE__), 'views')
set :cookie_options, :domain => nil

def getUsername()    
    begin
        token = request.cookies['auth']
        if token==nil or token==''
            return nil
        else
            headerPart = Base64.decode64(token.split('.')[0])
        
            if headerPart.include? "HS256"
                decodedToken =  JWT.decode(token, "delta_is_a_state_of_mind", true, { algorithm: 'HS256' })
                return decodedToken[0]['user']
            elsif headerPart.include? "none"
                decodedToken = JWT.decode(token, nil, true, { algorithm: 'none' })
                return decodedToken[0]['user']
            end 
        end
        
        return nil

    rescue JWT::ImmatureSignature
        return nil
    rescue JWT::DecodeError
        return nil
    end
end

def setCookies(userName)
    payload = {"user": userName}
    header = {"alg":"HS256","typ":"JWS"}
    token = JWT.encode(payload, "delta_is_a_state_of_mind", "HS256", header)
    cookies[:auth] = token
end

get '/' do
    if request.cookies['auth']
        @user = getUsername()

        info = "Invalid Token"
        return erb :login, :locals => {:info => info} unless @user
        
        if @user.upcase == "MICHAEL"
            return erb :michael
        end
        if @user == "admin"
            return erb :admin
        end
        return erb :index

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
        setCookies(user)
    
    else
        info = "Try login with michael's credential"
        return erb :login, :locals => {:info => info}
    end
    redirect '/'
end

get '/login' do
    info = "GET /login"
    return erb :login, :locals => {:info => info}
end

get '/robots.txt' do
    @robots_file = File.open("./views/robots.txt","r")
    erb :robots
end

not_found do
    status = 404
    erb :oops
end