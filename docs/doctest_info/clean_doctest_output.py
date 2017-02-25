import re

try:
    fp=open('_build/doctest/output.txt')
except:
    raise("You should probably run `make doctest` first")
err_fp=open('errors_only.txt', 'w+')
dict={}
line=fp.readline()
file_header=re.compile("Document:")
err_header=re.compile('File "')
err_indicator=re.compile('\*\*\*\*')
while line != '':
    if re.match(file_header, line):
        cur_header=line
        line=fp.readline()
        line=fp.readline()
        if re.match(err_indicator, line):
            dict[cur_header]=[]
            err_text=fp.readline()
            more_errors=True
            err_fp.write(cur_header + '\n')
            err_fp.write("**********************************************\n")
            while more_errors:
                while not re.match(err_indicator, err_text):
                    dict[cur_header].append(err_text)
                    err_text = fp.readline()
                err_text = fp.readline()
                dict[cur_header].append("**********************************************\n")
                if not re.match(err_header, err_text):
                    more_errors=False
            err_fp.writelines("".join(dict[cur_header]))

    line=fp.readline()
err_fp.close()
fp.close()


