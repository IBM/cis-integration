import sys
import getpass
import os
import certcreate
from functions import Color as Color
'''
To get python script to run globally run following command: $ pip3 install -e /path/to/script/folder
'''

class IntegrationInfo:
    crn = ''
    zone_id = ''
    api_endpoint = 'https://api.cis.cloud.ibm.com'
    app_url = ''
    cis_api_key = ''
    schematics_url = 'https://us.schematics.cloud.ibm.com'
    github_pat = ''     # might need to be removed later

    # used to create .env file
    def create_envfile(self):
        os.environ["CRN"] = self.crn
        os.environ["ZONE_ID"] = self.zone_id
        os.environ["API_ENDPOINT"] = self.api_endpoint
        os.environ["CIS_SERVICES_APIKEY"] = self.cis_api_key

        info = ["CRN=\""+self.crn+"\"\n", "ZONE_ID=\""+self.zone_id+"\"\n", "API_ENDPOINT=\""+self.api_endpoint+"\"\n", "CIS_SERVICES_APIKEY=\""+self.cis_api_key+"\"\n", "SCHEMATICS_URL=\""+self.schematics_url+"\"\n", "GITHUB_PAT=\""+self.github_pat+"\"\n"]
        file = open("credentials.env", "w")
        file.writelines(info)
        file.close()

def print_help():
    print(Color.BOLD + 'NAME:' + Color.END)
    print("\tcis-integration - a command line tool used to connect a CIS instance with an application deployed on Code Engine\n")

    print(Color.BOLD + "USAGE:" + Color.END)
    print("\t[enviornment variables] cis-integration [global options] [CIS CRN] [CIS ID] [APP URL] [GITHUB PAT]\n")

    print(Color.BOLD + "GLOBAL OPTIONS:" + Color.END)
    print("\t--help, -h \t\t show help\n")

def main():
    UserInfo = IntegrationInfo()
    
    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        print_help()
        sys.exit(1)

    try:
        UserInfo.crn = sys.argv[1]
    except IndexError:
        print("You did not specify a CIS CRN.")
        sys.exit(1)

    try:
        UserInfo.zone_id = sys.argv[2]
    except IndexError:
        print("You did not specify a CIS Zone_ID.")
        sys.exit(1)
    
    try:
        UserInfo.app_url = sys.argv[3]
    except IndexError:
        print("You did not specify a application URL.")
        sys.exit(1)

    # temp variable github PAT while the project is private, will need to be removed once prject is public
    '''
    try:
        UserInfo.github_pat = sys.argv[4]
    except IndexError:
        print("You did not specify a GitHub PAT.")
        sys.exit(1)
    '''
    UserInfo.cis_api_key = getpass.getpass(prompt="Enter CIS Services API Key: ")
    UserInfo.create_envfile()
   
    certcreate.main()
