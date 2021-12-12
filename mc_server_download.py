import requests  # fetch website
from bs4 import BeautifulSoup  # using bs4 for extraction
import re  # using regex to locate 'server.jar' on website
import hashlib  # using SHA-1 for validation

url = 'https://www.minecraft.net/en-us/download/server'
scrape_timeout = 3
download_timeout = 15

def hash_file(filename):  # https://www.programiz.com/python-programming/examples/hash-file
    """This function returns the SHA-1 hash
    of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:

        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()

# get webpage
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'},
                 timeout=scrape_timeout)  # GET request to url
if r.status_code != 200:
    print('error: webpage status code not 200, local server jar is untouched, exiting mc_server_download.')
    quit()

# locate server jar
soup = BeautifulSoup(r.content, features="html.parser")
server_jar_string = soup.find('a', href=re.compile(r'server\.jar')).get('href')

# check if server jar is up to date by comparing sha-1 values
sha1_hash = hash_file('server.jar')
if sha1_hash in server_jar_string:
    print('Local server jar is up to date, exiting mc_server_download.')
    quit()
else:
    print('New version found, initiating download.')

# download server jar
r_server = requests.get(server_jar_string, headers={'User-Agent': 'Mozilla/5.0'}, timeout=download_timeout, stream=True)
if r_server.status_code != 200:
    print('error: server file status code not 200, local server jar is untouched, exiting mc_server_download.')
    quit()

# overwrite server jar
try:
    open('server.jar', 'wb').write(r_server.content)
except:
    print('Error occurred when overwriting server jar. Link:', server_jar_string)

# validate server jar
sha1_hash = hash_file('server.jar')

if sha1_hash not in server_jar_string:
    print('Jar file validation failed, local server jar should be discarded, exiting mc_server_download. Link:', server_jar_string)
    quit()

print('Server jar update complete, exiting mc_server_download.')
