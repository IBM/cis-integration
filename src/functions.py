import requests
class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def healthCheck(hostUrl):
   print("Checking if",hostUrl,"is up...")
   try:
      requests.request("GET", hostUrl)
      print(Color.GREEN+hostUrl,"has successfully been deployed."+Color.END)
   except:
      print(Color.YELLOW+hostUrl,"is not up yet. May take a few minutes to start."+Color.END)