import json

f = open('static/countryCodes.json', 'r')
data = json.load(f)

def countryCodes(cName):
    for key, value in data.items():
        if cName == value.replace(' ', '').lower():
            imgLink = "https://flagcdn.com/256x192/" + key + ".png"
            details = {
                'code': key, 
                'name': value,
                'imgLink': imgLink
            }
            return details
    
    return 0