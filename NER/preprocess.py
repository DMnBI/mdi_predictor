import re
import sys

def remove_bracket(line) :
	line_len = 0	
	while not line_len == len(line):
        	line_len = len(line)
	        line = re.sub("(\(|\{|\[)[^\(|\)|\{|\}|\[|\]]+(\)|\}|\])", "", line)
	line = re.sub("\s+", " ", line)
	return line


input_file = sys.argv[1]
output_file = sys.argv[2]

rf = open(input_file, 'r')
wf = open(output_file, 'w')

readLines = rf.readlines()
for line in readLines:
	if not line: break
	if "|a|" in line:
		line = remove_bracket(line)+'\n'
	wf.write(line)

rf.close()
wf.close()
	
	
