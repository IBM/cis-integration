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

    #created iks sub-command as an example for to structure the next platform
    ks_parser = subparsers.add_parser("iks", aliases=['ks'], add_help=False)
    ks_parser.add_argument("-c","--crn")
    ks_parser.add_argument("-z","--zone_id")
    ks_parser.add_argument("-d","--cis_domain")
    ks_parser.add_argument("-t","--terraform", action='store_true')
    ks_parser.add_argument("-r","--resource_group")
    ks_parser.add_argument("-n","--name")
    ks_parser.add_argument("-h","--help", action='store_true')
    ks_parser.add_argument("-v","--verbose", action='store_true')
    ks_parser.add_argument("--delete", action='store_true')
    ks_parser.add_argument("-i","--iks_cluster_id")

    args = parser.parse_args()

    if args.uninstall:
        #removes the ci and cis-integration command from system
        confirm = input("Are you sure you wish to uninstall? (y/n): ").lower()
        if confirm == 'y' or confirm == 'yes':
            bash_cmd = "pip3 uninstall -y -r requirements.txt"
            for item in execute(bash_cmd):
                print(item, end="")
            if os.path.isfile("/usr/local/bin/cis-integration") and os.path.isfile("/usr/local/bin/ci"):
                os.remove("/usr/local/bin/cis-integration")
                os.remove("/usr/local/bin/ci")
        else:
            sys.exit(1)

    if args.command=="code-engine" or args.command=="ce":
        CodeEngine(args)

    elif args.command=="iks" or args.command=="ks":
        print("running iks command")
        iks(args)

if __name__ == "__main__":
    main()
