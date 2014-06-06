'''
Created on Feb 22, 2014

@author: Renmiri
'''

import urllib.request
import xml.etree.ElementTree as ET
from io import BytesIO
from time import gmtime, strftime
import operator

def get_owner():
    tree = ET.parse('ownerdata.xml')
    root = tree.getroot()
    for odata in root:
        print("reading",odata.tag)
        if odata.tag == 'scroll':
            thescroll = odata.get("name")
            print(odata.tag," = ",thescroll)
        return thescroll


def get_dragons():
    try:
        tree = ET.parse('breedids'+thescroll+'.xml')
    except:
        tree = ET.fromstring('<?xml version="1.0"?><data><breedid name="/images/gtMN.png"><path>/images/gtMN.png</path><imgtoid>http://dragcave.net/images/gtMN.png</imgtoid><matchid>Horse.png</matchid><found>True</found><rms>0.0</rms></breedid></data>')
        tree = ET.ElementTree(tree)
    root = tree.getroot()
    j = 0
    breed_dict = {}
    breed_err = {}
    for breed in root:
        path = breed.find('path').text
        breed1 = breed.find('imgtoid').text
        result = breed.find('found').text
        match = breed.find('matchid').text
        rms = breed.find('rms').text
        intrms = int(float(rms))
        if intrms > 0 :
            breed_dict[path] = match
            breed_err[path] = rms
        print(path,breed1,result,match,rms)
    print("done reading known")
    return(breed_dict,breed_err)

def go_get_file(fp):
    fp.write("<HTML>"+"\n")
    fp.write("<HEAD>"+"\n")
    fp.write(' <meta http-equiv="Content-Type" content="text/html; charset:utf-8"> \n')
    fp.write('<title>'+ tguser + ' Dragon Breeds Found in Scroll</title> \n')
    fp.write ('<script src="jquery-1.6.1.min.js" type="text/javascript"></script>')
    fp.write('<style type="text/css">'+"\n")
    fp.write("   table { border: double #808080; border-collapse: collapse; }"+"\n")
    fp.write("    td { "+"\n")
    fp.write("        border: double #808080; "+"\n")
    fp.write("        text-align: center ; "+"\n")
    fp.write("        valign: center ;"+"\n")
    fp.write("    }"+"\n")
    fp.write("    img {"+"\n")
    fp.write("    display: block;"+"\n")
    fp.write("    margin-left: auto;"+"\n")
    fp.write("    margin-right: auto "+"\n")
    fp.write("}"+"\n")
    fp.write("</style>"+"\n")
    fp.write("<SCRIPT LANGUAGE='JavaScript'> "+"\n")
    fp.write("function init() { "+"\n")
    fp.write(" tjunk = 'new school' ; ")
    fp.write("}"+"\n")
    fp.write("</SCRIPT>"+"\n")
    fp.write("</HEAD>"+"\n")
    fp.write("<BODY  bgcolor='#EADAB9' onload=init()>"+"\n")
    fp.write("<h1 id='top'>"+tguser+" Dragon Breeds Found in Scroll: Problems</h1> \n")
    fp.write("<h3>"+mdate+"</h3>")
    fp.write("<br/><br/>\n")
    print('Header written')
    return
    

thescroll = get_owner()
print(thescroll)
if thescroll < " ":
    thescroll="khione"
dragons = get_dragons()
unkknownbreed_dict = dragons[0]
breed_err = dragons[1]
sorted_breed_dict = sorted(unkknownbreed_dict, key=unkknownbreed_dict.get)
print(breed_err)
print(unkknownbreed_dict)
print(sorted_breed_dict)

print("xml saved")
f = open('checkguess_'+thescroll+'.html', 'w')
tguser = thescroll
mdate = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
go_get_file(f)

f.write('<table>')

for k in sorted_breed_dict:
    v = unkknownbreed_dict[k]
    rms = breed_err[k][0:5]
    print(k,v, rms)
    f.write('<tr><td>path: '+k+'</td>\n')
    f.write('   <td><img src="http://dragcave.net'+k+'"/></td>\n')
    f.write('   <td><img src="./dragon/all/'+v+'"/></td>\n')
    f.write('   <td>error: '+rms+'</td>\n')
    f.write('   <td>breed: '+v+'</td>\n')
    f.write('</tr>\n')
    
print("page written")
f.write("</table>")
f.write("</BODY>"+"\n")
f.write("</HTML>"+"\n")
f.close
