"""Map feature codes to human readable strings, e.g.:

    k5conf2 -> CONF2. Child has seen his/her biofather in the last year.
"""

import glob
import pickle
import codecs


def process_description(line):
    """Split a single line into its feature code and description.
    """
    line = line.rstrip()  # Remove trailing '\r\n'.
    parts = line.split(None, 1)  # Split on first whitespace.
    if len(parts) == 0:
        return None, None
    code, description = parts
    return unicode(code), unicode(description)


def process_metadata(line):
    """Process questionnaire metadata.
    """
    keys = ['type', 'label', 'range', 'units', 'unique values', 'missing']
    parts = line.split(':')
    if len(parts) == 2:
        key, val = parts
        key = clean(key)
        val = clean(val)
    elif len(parts) == 3:
        try:
            parts2 = parts[1].split()
            key1 = clean(parts[0])
            val1 = clean(parts2[0])
            key2 = clean(parts2[1])
            val2 = clean(parts[2])
            return [(key1, val1), (key2, val2)]
        except IndexError:
            return
    else:
        return
    if key in keys:
        return [(key, val)]


def clean(string):
    """Remove whitespace and convert string to unicode.
    """
    return unicode(string.strip())


def process_file(fname, f):
    """Process file into dictionary mapping feature codes to descriptions.
    """
    data = {}
    # Save next line flag.
    fl = False
    prev_code = None
    for line in f:
        if fl:
            code, description = process_description(line)
            if code and description:
                prev_code = code
                furl = 'http://fragilefamilies.princeton.edu/sites/' \
                       'fragilefamilies/files/%s' % fname
                data[code] = {
                    'description': description,
                    'source file': furl
                }
            fl = False
        else:
            key_vals = process_metadata(line)
            if key_vals:
                for key, val in key_vals:
                    if key == 'range':
                        # Convert list as string to real list.
                        val = eval(val)
                    if key == 'unique values':
                        val = int(val.replace(',', ''))
                    data[prev_code][key] = val
        if line.startswith('----------'):
            fl = True
    return data


def save_data(data):
    """Save data as pickle file and plain text file (for quick searching).
    """
    with open('codebook/db.pck', 'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


def process_feature_codes_and_pickle():
    data = {}
    for fpath in glob.glob('data/*.txt'):
        fname = fpath.split('/')[1]
        f = codecs.open(fpath, 'r', 'Windows-1252')
        data.update(process_file(fname, f))
        f.close()
    save_data(data)


if __name__ == '__main__':
    process_feature_codes_and_pickle()
