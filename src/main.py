import sys

'''
To get python script to run globally run following command: $ pip3 install -e /path/to/script/folder
'''

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

class IntegrationInfo:
    crn = ''
    zone_id = ''
    api_endpoint = 'https://api.cis.cloud.ibm.com'
    app_url = ''

def print_help():
    print(Color.BOLD + 'NAME:' + Color.END)
    print("\tcis-integration - a command line tool used to connect a CIS instance with an application deployed on Code Engine\n")

    print(Color.BOLD + "USAGE:" + Color.END)
    print("\t[enviornment variables] cis-integration [global options] [CIS CRN] [CIS ID] [APP URL]\n")

    print(Color.BOLD + "GLOBAL OPTIONS:" + Color.END)
    print("\t--help, -h \t\t show help\n")

def main():
    if sys.argv[1] == '-h':
        print_help()
        exit()

    try:
        IntegrationInfo.crn = sys.argv[1]
    except IndexError:
        print("You did not specify a CIS CRN.")
        sys.exit(1)

    try:
        IntegrationInfo.zone_id = sys.argv[2]
    except IndexError:
        print("You did not specify a CIS Zone_ID.")
        sys.exit(1)
    
    try:
        IntegrationInfo.app_url = sys.argv[3]
    except IndexError:
        print("You did not specify a application URL.")
        sys.exit(1)


    