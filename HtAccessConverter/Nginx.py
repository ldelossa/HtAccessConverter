class Nginx:
    def __init__(self, Access_Obj=None, listen_directive=None, server_name_directive=None):
        """
        Nginx object. This holds the config writing logic. It's instantiated with an .htaccess object. This object
        uses the .htaccess's object 'redirect_array' in order to write Nginx specific server blocks
        """
        self.Access_Obj = Access_Obj
        self.listen_directive = listen_directive
        self.server_name_directive = server_name_directive

    def config_printer(self):
        """
        Creates the semantic rules for writing out the server blocks. I thought about using something like
        pyparsing, but this seemed relatively easy to just do with print statements.
        :return:
        """
        print('server {')
        print(' listen {};'.format(self.listen_directive))
        print(' server_name {};'.format(self.server_name_directive))
        print('\n')

        for rewrite in self.Access_Obj.redirect_array:

            #Nginx starts relative locations with forward slash, apache rules use the ^ character, let's fix this
            if rewrite['type'] == 'RewriteRule':
                temp_array = list(rewrite['regex'])
                temp_array[0] = '/'
                location_string = "".join(temp_array)


                print(" location ~* {} {{".format(location_string))
                print('    rewrite {} {} break;'.format(rewrite['regex'], rewrite['substitution']))
                print('  }')
                print('\n')

            if rewrite['type'] == 'Redirect':
                print("  location {} {{".format(rewrite['original_url']))
                print("    rewrite ^(.*)$ {} redirect;".format(rewrite['redirect']))
                print("  }")
                print('\n')

            if rewrite['type'] == 'RedirectMatch':
                print(" location ~ {} {{".format(rewrite['regex']))
                print("    rewrite ^(.*)$ {} redirect;".format(rewrite['substitution']))
                print('\n')
        print('}')
        print('\n')