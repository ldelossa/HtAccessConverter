# HtAccessConverter

This tool is used to parse apache .htaccess rules and convert them into nginx server blocks. A few assumptions are made about your .htaccess file

- Right now, HtAccessConverter only supports the following apache directives: RewriteRule, RedirectMatch, and Redirect
- HtAccessConverter expects your .htaccess file represents matches on a single hostname. I.e all rewriting is occuring after www.example.com/
- HtAccessConverter assumes all .htaccess flags are [L], and resprents this with the appropriate break; command in nginx

## Requirements:
This is a pure-python solution. It's writen in python3.4. You only need to provide the .htaccess file.

## Usage:
HtAccessConverter can be ran in two ways. The first is a one-off fashion where you supply your command line arguments directly to the python module. The other method is supplying a config.json file in ./HtAccessConverter/config/

If you're using the json batch method, you will need to fill in the appropriate information to create your server blocks. There's a sample json file provided, along with a sample .htaccess file provided.

The application always expects that your .htaccess file is named .htaccess. It will exit if the file is not named this.


#### One off fashion:
```
$ python3.4 HtAccessConverter -f '~/HtAccessConverter/HtAccessConverter/contrib/.htaccess' -s 'example.com' -l '80'
```
#### Json configuration
```
$ python3.4 HtAccessConverter -json
```