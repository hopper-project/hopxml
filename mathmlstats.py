from lxml import etree
import re
import glob
import os
import sys
import multiprocessing as mp
from collections import Counter

def analyze(filename):
    global outpath
    with open(filename) as fh:
        text = fh.read()
    prefixmatches  = re.findall(r'(m(?:ml)?)\:math',text)
    if len(prefixmatches)==0:
        prefix = ""
    else:
        prefix = prefixmatches[0]
    text = re.sub(r'm(?:ml)?\:math',"math",text)
    root = etree.XML(text.encode())
    equations = root.findall(".//math")
    outertaglist = []
    displaylist = []
    csvlist = []
    eqstrings = []
    for i, x in enumerate(equations):
        parenttag = x.getparent().tag
        props = []
        try:
            eqid=x.getparent().attrib['label']
        except:
            eqid=""
        for key, value in x.attrib.items():
            displaylist.append("{}={}".format(key, value))
            props.append("{}={}".format(key,value))
        toap = ",".join([os.path.basename(filename),str(i),eqid,prefix," ".join(props),parenttag])
        csvlist.append(toap)
        outertaglist.append(x.getparent().tag)
    with open(os.path.join(outpath,os.path.basename(os.path.splitext(filename)[0])+'csv'),'w') as fh:
        fh.write('\n'.join(csvlist))
    return(len(equations),Counter(outertaglist), Counter(displaylist))

def main():
    global outpath
    if len(sys.argv)!=3:
        print("Usage: python3 mathmlstats.py /path/to/xml/files/ /path/to/desired/output/folder/")
        exit(1)
    path = sys.argv[1]
    outpath = sys.argv[2]
    if not os.path.isdir(path):
        print("Error: input directory does not exist")
        exit(1)
    # path = '/media/jay/Data1/phrvd/all/'
    # outpath = '/media/jay/Data1/phrvd/metadata/'
    if not os.path.isdir(outpath):
        os.makedirs(outpath)
    filelist = glob.glob(os.path.join(path,'*.xml'))
    print("{} xml files found".format(len(filelist)))
    pool = mp.Pool(mp.cpu_count())
    outlist = pool.map(analyze,filelist)
    toteqs = 0
    maxthings = Counter()
    totdisplay = Counter()
    for x in outlist:
        toteqs += x[0]
        maxthings += x[1]
        totdisplay += x[2]
    print("\n{} equations in the entire corpus".format(toteqs))
    maxmostcommon = maxthings.most_common(10)
    displaymostcommon = totdisplay.most_common(10)
    print("\n10 most common parent tags:")
    for i, x in enumerate(maxmostcommon):
        print("{}: \"{}\" - {} occurrences".format(i+1,x[0],x[1]))
    print("\n10 most common attributes in the <math> tag:")
    for i, x in enumerate(displaymostcommon):
        print("{}: \"{}\" - {} occurrences".format(i+1,x[0],x[1]))
    pool.close()
    pool.join()
if __name__=='__main__':
    main()
