# hopxml
Tools for analyzing/extracting from/parsing xml files.

## mathmlstats.py

Usage:`python3 mathmlstats.py /path/to/xml/directory/ /path/to/output/directory/`

This script accepts a directory of .xml files.

For every .xml file in that directory, it generates a correspondingly-named csv (filename.xml becomes filename.csv) in the output directory.
os.path.basename(filename),str(i),eqid,prefix," ".join(props),parenttag
The output csv has five comma-delimited 'columns', in order as follows:
* File name
* Index of equation in document (0-indexed)
* Equation label (from parent), if applicable
* Math tag prefix (e.g. if the document was standardized to contain \&lt;m:math\> \&lt;mml:math\> instead of &lt;math&gt;, it will denote that)
* Math tag attributes (e.g. in &lt;math display="inline">, display is an attribute with a value of "inline") delimited by spaces
* Parent tag (formula, dformula)

Once the script has finished processing all of the documents, it prints to stdout a formatted list of:
* Total number of equations (denoted by &lt;math&gt;...&lt;/math&gt;) in the corpus
* 10 most common tags of the parent element of the &lt;math&gt;...&lt;/math&gt; element.
* 10 most common attributes of the &lt;math&gt; tag

Example output for ~35k example research papers:

> 14579353 equations in the entire corpus

> 10 most common parent tags:

> 1: "formula" - 9373955 occurrences

> 2: "inline-formula" - 3381389 occurrences

> 3: "dformula" - 1324780 occurrences

> 4: "disp-formula" - 485566 occurrences

> 5: "dformgrp" - 13510 occurrences

> 6: "p" - 121 occurrences

> 7: "{http://www.niso.org/standards/z39-96/ns/oasis-exchange/table}entry" - 16 occurrences

> 8: "article-title" - 8 occurrences

> 9: "title" - 4 occurrences

> 10: "italic" - 2 occurrences

> 10 most common attributes in the &lt;math&gt; tag:

> 1: "display = inline" - 12755663 occurrences

> 2: "display = block" - 1823687 occurrences

> 3: "altimg-valign = -6.5" - 121 occurrences

> 4: "altimg-valign = -2.5" - 56 occurrences

> 5: "altimg-valign = -7.5" - 41 occurrences

> 6: "altimg-valign = -9.5" - 36 occurrences

> 7: "altimg-valign = -12.5" - 23 occurrences

> 8: "altimg-valign = -1.5" - 19 occurrences

> 9: "altimg-valign = -11.5" - 12 occurrences

> 10: "altimg-valign = -21.5" - 11 occurrences
