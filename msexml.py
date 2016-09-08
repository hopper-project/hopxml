from lxml import etree
from lxml import objectify
import re
import glob
import os
import sys
import multiprocessing as mp
from collections import Counter
import random
import html


def mse(filename):
    global outpath
    with open(filename) as fh:
        text = fh.read()
    try:
        root = etree.XML(text.encode())
    except:
        print("{}: lxml parsing failed".format(filename))
        return("{}: lxml parsing failed".format(filename))
    for x in root.findall('.//'):
        x.tag = etree.QName(x).localname
    references = root.findall(".//eqref")
    reflist = []
    out = []
    toret = ""
    if len(references)>0:
        for ref in references:
            try:
                reflist += ref.attrib['rids'].split(' ')
            except:
                pass
        count = Counter(reflist).most_common(5)
        print(count[0][0])
        math = root.findall(".//math")
        for eq in math:
            try:
                parentid = eq.getparent().attrib['id']
                if parentid==count[0][0]:
                    eqtext = etree.tostring(eq).decode()
                    eqtext = re.sub(r'xmlns:m(?:ml)?',"xmlns",eqtext)
                    eqtext = re.sub(r'xmlns:xlink=\".*?\"','',eqtext)
                    eqtext = re.sub(r'xmlns:oasis=\".*?\"','',eqtext)
                    out.append(eqtext)
                    continue
            except:
                continue
    else:
        math = root.findall('.//math')
        if len(math)>0:
            parent = math[0].getparent().getchildren()
            for math in parent:
                eqtext = etree.tostring(math).decode()
                eqtext = re.sub(r'xmlns:m(?:ml)?',"xmlns",eqtext)
                eqtext = re.sub(r'xmlns:xlink=\".*?\"','',eqtext)
                eqtext = re.sub(r'xmlns:oasis=\".*?\"','',eqtext)
                out.append(eqtext)
            toret = os.path.join(outpath,os.path.basename(filename))

    if len(out)>0:
        with open(os.path.join(outpath,os.path.basename(filename)),'w') as fh:
            fh.write('<root>\n')
            for line in out:
                fh.write('\t'+line+'\n')
            fh.write('</root>')
    return(toret)

def main():
    global outpath
    if len(sys.argv)!=3:
        print("Usage: python3 extractmathml.py /path/to/xml/files/ /path/to/desired/output/folder/")
        print("Output path is optional")
        exit(1)
    path = sys.argv[1]
    if len(sys.argv==2):
        outpath=''
    else:
        outpath = sys.argv[2]
    if not os.path.isdir(path):
        print("Error: input directory does not exist")
        exit(1)
    # path = '/media/jay/Data1/phrvd/all/'
    # outpath = '/media/jay/Data1/phrvd/msexml/'
    print(outpath)
    if not os.path.isdir(outpath):
        os.makedirs(outpath)
    filelist = glob.glob(os.path.join(path,'*.xml'))
    print("{} xml files found".format(len(filelist)))
    pool = mp.Pool(mp.cpu_count())
    outlist = pool.map(mse,filelist)
    with open(outpath[:-1]+'.log','w') as fh:
        for x in outlist:
            if x:
                fh.write(x+'\n')
    pool.close()
    pool.join()
if __name__=='__main__':
    main()
