'''
DISCLAIMER OF WARRANTIES:
Permission is granted to copy this Tools or Sample code for internal use only, provided that this
permission notice and warranty disclaimer appears in all copies.

THIS TOOLS OR SAMPLE CODE IS LICENSED TO YOU AS-IS.
IBM AND ITS SUPPLIERS AND LICENSORS DISCLAIM ALL WARRANTIES, EITHER EXPRESS OR IMPLIED, IN SUCH SAMPLE CODE,
INCLUDING THE WARRANTY OF NON-INFRINGEMENT AND THE IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A
PARTICULAR PURPOSE. IN NO EVENT WILL IBM OR ITS LICENSORS OR SUPPLIERS BE LIABLE FOR ANY DAMAGES ARISING
OUT OF THE USE OF OR INABILITY TO USE THE TOOLS OR SAMPLE CODE, DISTRIBUTION OF THE TOOLS OR SAMPLE CODE,
OR COMBINATION OF THE TOOLS OR SAMPLE CODE WITH ANY OTHER CODE. IN NO EVENT SHALL IBM OR ITS LICENSORS AND
SUPPLIERS BE LIABLE FOR ANY LOST REVENUE, LOST PROFITS OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL,
CONSEQUENTIAL,INCIDENTAL OR PUNITIVE DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY,
EVEN IF IBM OR ITS LICENSORS OR SUPPLIERS HAVE BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
'''
import os
import sys
import argparse
from src.ce.codeEngine import CodeEngine
from src.iks.iks import iks
import subprocess

def execute(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, universal_newlines=True)
    for line in iter(process.stdout.readline, ""):
        yield line
    process.stdout.close()
    ret = process.wait()
    if ret:
        raise subprocess.CalledProcessError(ret, cmd)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--uninstall", help="uninstalls cis-integration from your system", action="store_true",)
    parser.add_argument("-s", "--sudo", help="adds sudo privileges for uninstall process", action="store_true",)

    subparsers = parser.add_subparsers(dest="command")
    
    #created code-engine sub-command with alias
    #disabled argparse default help flag for subcommandcto use our own custom help message
    ce_parser = subparsers.add_parser("code-engine", aliases=['ce'], add_help=False)
    ce_parser.add_argument("-c","--crn")
    ce_parser.add_argument("-z","--zone_id")
    ce_parser.add_argument("-d","--cis_domain")
    ce_parser.add_argument("-a","--app")
    ce_parser.add_argument("-t","--terraform", action='store_true')
    ce_parser.add_argument("-r","--resource_group")
    ce_parser.add_argument("-n","--name")
    ce_parser.add_argument("-e","--env", action='store_true')
    ce_parser.add_argument("-h","--help", action='store_true')
    ce_parser.add_argument("-v","--verbose", action='store_true')
    ce_parser.add_argument("--delete", action='store_true')
    ce_parser.add_argument("--standard",action='store_true')

    #created iks sub-command as an example for to structure the next platform
    ks_parser = subparsers.add_parser("iks", aliases=['ks'], add_help=False)
    ks_parser.add_argument("-c","--crn")
    ks_parser.add_argument("-z","--zone_id")
    ks_parser.add_argument("-d","--cis_domain")
    ks_parser.add_argument("-t","--terraform", action='store_true')
    ks_parser.add_argument("-r","--resource_group")
    ks_parser.add_argument("-n","--name")
    ks_parser.add_argument("--namespace")
    ks_parser.add_argument("--service_name")
    ks_parser.add_argument("--service_port")
    ks_parser.add_argument("-h","--help", action='store_true')
    ks_parser.add_argument("-v","--verbose", action='store_true')
    ks_parser.add_argument("--delete", action='store_true')
    ks_parser.add_argument("-i","--iks_cluster_id")
    ks_parser.add_argument("-p", "--vpc_name")

    args = parser.parse_args()

    if args.uninstall:
        #removes the ci and cis-integration command from system
        confirm = input("Are you sure you wish to uninstall? (y/n): ").lower()
        if confirm == 'y' or confirm == 'yes':
            try:
                bash_cmd = ""
                if args.sudo:
                    bash_cmd = "sudo pip3 uninstall -y -r requirements.txt"
                else:
                    bash_cmd = "pip3 uninstall -y -r requirements.txt"
                for item in execute(bash_cmd):
                    print(item, end="")
            except Exception as e:
                reinstall_cmd = "pip3 install -r requirements.txt"
                subprocess.Popen(reinstall_cmd.split(), stdout=subprocess.PIPE)
                print("Uninstall failed, try again using the sudo option.")
                print(e)
            else:
                if os.path.isfile("/usr/local/bin/cis-integration") and os.path.isfile("/usr/local/bin/ci"):
                    os.remove("/usr/local/bin/cis-integration")
                    os.remove("/usr/local/bin/ci")
        else:
            sys.exit(1)

    if args.command=="code-engine" or args.command=="ce":
        CodeEngine(args)

    elif args.command=="iks" or args.command=="ks":
        iks(args)

if __name__ == "__main__":
    main()
