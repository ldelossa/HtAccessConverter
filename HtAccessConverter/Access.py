class Access:
    def __init__(self, access_file):
        """
        Access object, The object is instantiated with a path to a .htaccess file. It reads the .htaccess file
        then re-declares it's self.access_file to hold the actual strings of the file.
        :param access_file:
        :return:
        """
        self.access_file = access_file
        self.redirect_array = []

        with open(self.access_file, 'r') as file:
            self.access_file = file.read()

    def parse_access_file(self):
        """
        Simple keywoard parsing of the .htaccess file. We identify the keyword then build a dictionary structure
        which represents the fields that are necessary in order to convert to nginx rewrite blocks.
        :return:
        """
        for line in self.access_file.split('\n'):
            if line.split()[0] == 'RewriteRule':
                self.redirect_array.append({'type': 'RewriteRule', 'regex': line.split()[1],
                                            'substitution': line.split()[2], 'flag_string': line.split()[3]})
            if line.split()[0] == 'Redirect':
                self.redirect_array.append({'type': 'Redirect', 'http_code': line.split()[1], 'original_url': line.split()[2],
                                           'redirect': line.split()[3]})

            if line.split()[0] == 'RedirectMatch':
                self.redirect_array.append({'type': 'RedirectMatch', 'http_code': line.split()[1], 'regex': line.split()[2],
                                            'substitution': line.split()[3]})





