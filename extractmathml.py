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


def analyze(filename):
    global outpath
    with open(filename) as fh:
        text = fh.read()
    try:
        root = etree.XML(text.encode())
    except:
        print("{}: lxml parsing failed".format(filename))
        return
    for x in root.findall('.//'):
        x.tag = etree.QName(x).localname
    equations = root.findall(".//math")
    out = []
    if len(equations)>0:
        for i, eq in enumerate(equations):
            eqtext = etree.tostring(eq).decode()
            eqtext = re.sub(r'xmlns:m(?:ml)?',"xmlns",eqtext)
            eqtext = re.sub(r'xmlns:xlink=\".*?\"','',eqtext)
            eqtext = re.sub(r'xmlns:oasis=\".*?\"','',eqtext)
            out.append(eqtext)
        print(len(out))
        with open(os.path.join(outpath,os.path.basename(os.path.splitext(filename)[0][:-9]+'.xml')),'w',encoding="utf8") as fh:
            outtext = '\n'.join(out)
            outtext = outtext.split('\n')
            fh.write('<root>\n')
            for line in outtext:
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
    # outpath = '/media/jay/Data1/phrvd/extracted/'
    if not os.path.isdir(outpath):
        os.makedirs(outpath)
    filelist = glob.glob(os.path.join(path,'*.xml'))
    # filelist = [random.choice(filelist)]
    print("{} xml files found".format(len(filelist)))
    pool = mp.Pool(mp.cpu_count())
    outlist = pool.map(analyze,filelist)
    pool.close()
    pool.join()
if __name__=='__main__':
    main()
