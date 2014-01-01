import httplib

conn = httplib.HTTPConnection('127.0.0.1:5000')
conn.request('GET','/000100')
print conn.getresponse().read()
