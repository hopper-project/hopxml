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
    # re.findall expression to capture math prefix
    prefixmatches  = re.findall(r'(m(?:ml)?)\:math',text)
    if len(prefixmatches)==0:
        prefix = ""
    else:
        prefix = prefixmatches[0]
    # remove all prefixes
    # lxml has a hard time with non-universally prefixed namespaces
    text = re.sub(r'm(?:ml)?\:math',"math",text)
    root = etree.XML(text.encode())
    equations = root.findall(".//math")
    # parent tag list
    parenttags = []
    # math tag attribute list
    attriblist = []
    # list of strings to be written out to CSV
    csvlist = []
    for i, x in enumerate(equations):
        parenttag = x.getparent().tag
        props = []
        try:
            eqid=x.getparent().attrib['label']
        except:
            eqid=""
        for key, value in x.attrib.items():
            attriblist.append("{}={}".format(key, value))
            props.append("{}={}".format(key,value))
        if(outpath):
            # append: filename, eq index, math tag prefix, attributes, & parent tag
            toap = ",".join([os.path.basename(filename),str(i),eqid,prefix," ".join(props),parenttag])
            csvlist.append(toap)
        parenttags.append(x.getparent().tag)
    if(outpath):
        with open(os.path.join(outpath,os.path.basename(os.path.splitext(filename)[0])+'.csv'),'w') as fh:
            fh.write('\n'.join(csvlist))
    return(len(equations),Counter(parenttags), Counter(attriblist))

def main():
    global outpath
    if len(sys.argv)<2:
        print("Usage: python  3 mathmlstats.py /path/to/xml/files/ /path/to/desired/output/folder/")
        print("Output path is optional")
        exit(1)
    path = sys.argv[1]
    if len(sys.argv==2):
        outpath='phrvd_output'
    else:
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
    parent_tags = Counter()
    tag_attributes = Counter()

    for x in outlist:
        toteqs += x[0]
        parent_tags += x[1]
        tag_attributes += x[2]

    print("\n{} equations in the entire corpus".format(toteqs))

    mostcommon = 20

    maxmostcommon = parent_tags.most_common(20)
    displaymostcommon = tag_attributes.most_common(20)

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
