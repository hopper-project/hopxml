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
    print(outpath)
    print(os.path.join(outpath,os.path.basename(filename)))
    with open(filename) as fh:
        text = fh.read()
    try:
        root = etree.XML(text.encode())
    except:
        print("{}: lxml parsing failed".format(filename))
        return
    for x in root.findall('.//'):
        x.tag = etree.QName(x).localname
    references = root.findall(".//eqref")
    reflist = []
    if len(references)>0:
        for ref in references:
            try:
                reflist += ref.attrib['rids'].split(' ')
            except:
                pass
        count = Counter(reflist).most_common(5)
        print(count[0][0])
    else:
        return
    out = []
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
    if len(out)>0:
        print(os.path.join(outpath,os.path.basename(filename)))
        with open(os.path.join(outpath,os.path.basename(filename)),'w') as fh:
            fh.write('<root>\n')
            for line in out:
                fh.write('\t'+line+'\n')
            fh.write('</root>')


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
    filelist = [random.choice(filelist)]
    print("{} xml files found".format(len(filelist)))
    pool = mp.Pool(mp.cpu_count())
    outlist = pool.map(mse,filelist)
    pool.close()
    pool.join()
if __name__=='__main__':
    main()
