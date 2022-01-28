import argparse
import os
import pathlib
import re


# #############################################################################
# Only letters in the Hebrew Unicode block are handled/considered.
# In particular, Hebrew letters in the APF block are ignored.
# (APF = Alphabetic Presentation Forms.)
# Many (but not all) letters in the APF have "built-in"
# versions of the marks of concern here.
# (The marks of concern here are dagesh/mapiq, shin dot, & sin dot.)
# So this denormalization would be irrelevant to those APF letters anyway.
#
# Only marks in the Hebrew Unicode block are handled/considered.
# In particular, clusters are considered to end before a CGJ or ZWJ.
# For some Hebrew processing purposes this would be wrong.
# But we think this is fine for our purposes here.
# In other words, we assume none of the 3 marks of concern here
# would ever appear after a CGJ or ZWJ.
#
# Or, alternately, we assume that if such a mark did appear after
# a CGJ or ZWJ, it would appear in that position for good reason
# and should not be moved.
# I'm not sure what that good reason would be, though.


def _denorm(string):
    patclu = r'[א-ת][\u0590-\u05cf]*'  # pattern for a cluster
    return re.sub(patclu, _repl_cluster, string)


def _repl_cluster(match):
    wmat = match.group()  # the whole match
    lett, marks = wmat[0], wmat[1:]
    return lett + ''.join(sorted(marks, key=_ccs_keyfn))


_NS_COMB_CLASSES = {  # non-standard combining classes
    '\N{HEBREW POINT SHIN DOT}': 2,
    '\N{HEBREW POINT SIN DOT}': 3,
    '\N{HEBREW POINT DAGESH OR MAPIQ}': 4,
}


def _ccs_keyfn(char):
    return _NS_COMB_CLASSES.get(char) or 5


def main():
    """
        Denormalize a file to have non-standard (but more reasonable)
        mark order, with shin & sin dot tightest up against letters,
        followed by dagesh/mapiq, followed by all other marks.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename')
    parser.add_argument('output_filename')
    args = parser.parse_args()
    with open(args.input_filename, encoding='utf-8') as ifp:
        _with_tmp_openw(args.output_filename, lambda ofp: _fp_main(ifp, ofp))


def _fp_main(in_fp, out_fp):  # the "file pointer" core of main
    for in_line in in_fp:
        out_fp.write(_denorm(in_line) + '\n')
    

def openw(pathobj):  # open for writing
    os.makedirs(pathobj.parent, exist_ok=True)
    return open(pathobj, 'w', encoding='utf-8')


def tmp_path(path):
    pathobj = pathlib.Path(path)
    # e.g. from /dfoo/dbar/stem.ext return /dfoo/dbar/stem.tmp.ext
    # where suffix = .ext
    return pathobj.parent / (str(pathobj.stem) + '.tmp' + pathobj.suffix)


def _with_tmp_openw(path, callback):
    tpath = tmp_path(path)
    with openw(tpath) as outfp:
        callback(outfp)
    os.replace(tpath, path)


if __name__ == '__main__':
    main()
