import argparse
import os
import sys
import json

from HtAccessConverter.Access import Access
from HtAccessConverter.Nginx import Nginx

if __name__ == "__main__":
    """
    Parse arguments. We do not 'require' arguments here in order to allow the --json flag to be used without
    requiring any other arguments and values
    """
    #parse arguments
    parser = argparse.ArgumentParser(
        description='Script parses Redirect, RedirectMatch, and RewriteRule directies in Apache'
                    ' .htaccess files and converts this to a nginx server block'
    )

    parser.add_argument(
        '--json', action='store_true', help="Run in json-batch mode, must have HtAccessConverter/config/config.json present"
    )

    parser.add_argument(
        '-s', '--server', type=str, help="Server name for server_name directive in nginx server block"
    )

    parser.add_argument(
        '-l', '--listen', type=str, help="The string that follows the listen directive of an nginx server block"
    )

    parser.add_argument(
        '-f', '--file', type=str, help="The absolute path to the .htaccess file, file must be named .htaccess for validation"
    )

    args = parser.parse_args()

    """
    If ran with --json flag, search for json file. Parse json structure, loop through all dictionaries within the list
    and print a block for each config dictionary.
    """
    if args.json:
        #validate confid.json is located in ./config/
        config_file = os.path.abspath('HtAccessConverter/HtAccessConverter/config/config.json')

        with open(config_file, 'r') as config_json:
            config = json.load(config_json)

        for config_dict in config['config']:
            if config_dict['path'].split('/')[-1] != ".htaccess":
                print("You have not specified a .htaccess file in your json configuration")
                sys.exit(0)

            if not os.path.isfile(config_dict['path']):
                print("You have not specified a valid .htaccess file in your json configuration, does it exist?")
                sys.exit(0)


            AC = Access(config_dict['path'])
            AC.parse_access_file()

            NG = Nginx(Access_Obj=AC, listen_directive=config_dict['listen_directive'], server_name_directive=config_dict['server_name'])
            NG.config_printer()
    else:
        """
        If json flag is not found, then parse out arguments to variables. Then check if any are set to None, do our
        complaining about arguments here.

        Do some basic file checks on the passed in .htaccess file

        Instantiate our Acess and Nginx classes, and print the configuration
        """
        file = args.file
        listen_directive = args.listen
        server_name_directive = args.server

        argslist = [file, listen_directive, server_name_directive]

        if any(arg is None for arg in argslist):
            print("""You did not specify the correct arguments
            -f | --file         The absolute path to the .htaccess file, file must be named .htaccess for validation
            -s | --server       Server name for server_name directive in nginx server block
            -l | --listen       The string that follows the listen directive of an nginx server block"""
            )

            sys.exit(0)

        #file level checks
        if file.split('/')[-1] != ".htaccess":
            print("You have not specified a .htaccess file")
            sys.exit(0)

        if not os.path.isfile(file):
            print("You have not specified a valid .htaccess file, does it exist?")
            sys.exit(0)

        #instantiate htaccess parser object, parse the file passed in
        AC = Access(file)
        AC.parse_access_file()

        #instantiate nginx
        NG = Nginx(Access_Obj=AC, listen_directive=listen_directive, server_name_directive=server_name_directive)
        NG.config_printer()