import argparse
from codeEngine import CodeEngine
def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")
    
    #created code-engine sub-command with alias
    #disabled argparse default help flag for subcommandcto use our own custom help message
    ce_parser = subparsers.add_parser("code-engine", aliases=['ce'], add_help=False)
    ce_parser.add_argument("-c","--crn")
    ce_parser.add_argument("-z","--zone_id")
    ce_parser.add_argument("-d","--cis_domain")
    ce_parser.add_argument("-a","--app_url")
    ce_parser.add_argument("-t","--terraform", action='store_true')
    ce_parser.add_argument("-r","--resource_group")
    ce_parser.add_argument("-n","--name")
    ce_parser.add_argument("-p","--pat")
    ce_parser.add_argument("-e","--env", action='store_true')
    ce_parser.add_argument("-h","--help", action='store_true')

    #created iks sub-command as an example for to structure the next platform
    ks_parser = subparsers.add_parser("iks", aliases=['ks'], add_help=False)
    ks_parser.add_argument("-a")
    ks_parser.add_argument("-b")
    ks_parser.add_argument("-c")

    args = parser.parse_args()

    if args.command=="code-engine" or args.command=="ce":
        CodeEngine(args)

    elif args.command=="iks" or args.command=="ks":
        print("running iks command")

if __name__ == "__main__":
    main()
