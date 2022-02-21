import os
import sys
import time
import math
import argparse


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

NERDIR_PATH = DIR_PATH+"/NER"
PREPROC_PATH = NERDIR_PATH+"/preprocess.py"
TAGGERONE_PATH = NERDIR_PATH+"/TaggerOne-0.2.1"
DBNER_PATH = NERDIR_PATH+"/DBNER.jar"
merge_proc_path = NERDIR_PATH+"/merge_taggerOne.py"

NER_time = 0.0

def setParser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input",
			dest="input",
			metavar="FILE",
			required=True,
			help="Please enter the input file name.")
	parser.add_argument("-o", "--output",
			dest="output",
			metavar="FILE",
			required=True,
			help="Please enter the output file name.")
	return parser

def readFile(read_file):
	fileReader = open(read_file, 'r')
	content = "" 
	while True:
		eachline = fileReader.readline()
		if not eachline: break
		content += eachline + "\n"
	fileReader.close()
	return content 

def getlist(list_path):
	listReader = open(list_path, 'r')
	abstList = list()
	while True:
		eachline = listReader.readline()
		if not eachline: break
		abstList.append(eachline.strip())
	listReader.close()
	return abstList
	
def runPreprocess(inputAbst, output):
	command = "python "+PREPROC_PATH+" "+inputAbst+" "+output
	print('[Preprocess/'+str(os.getpid())+"]"+command)
	output = os.system(command)

def runTaggerOne(inputAbst, model_path, output):
	input_format = "PubTator"
	
	path = os.getcwd()
	print(os.getcwd())
	
	#os.system('cd {}'.format(TAGGERONE_PATH))
	os.chdir(TAGGERONE_PATH)
	print(">>"+os.getcwd())
	command = "./ProcessText.sh "+input_format+" "+model_path+" "+inputAbst+" "+output
	print('[TaggerOne/'+str(os.getpid())+"]"+command)
	output = os.system(command)
	
	os.system('cd {}'.format(TAGGERONE_PATH))
	
def runDBNER(inputAbst, output):
	dbner_path="java -jar "+DBNER_PATH
	command = dbner_path+" "+inputAbst+" "+output 
	print("[DBNER/"+str(os.getpid())+"]"+command)
	output = os.system(command)

def mergeTaggerOneOutput(BC5CDRD_output, NCBID_output, outputFile):
	command = "python "+merge_proc_path+" "+BC5CDRD_output+" "+NCBID_output+" "+outputFile
	print("[merge tagone output/"+str(os.getpid())+"]"+command)
	output = os.system(command)

def runNER(input_file, output_file):
	tagOne_BC5CDRD_model = TAGGERONE_PATH+"/output/model_BC5CDRD.bin"
	tagOne_NCBID_model = TAGGERONE_PATH+"/output/model_NCBID.bin"
	
	input_abstract = input_file
	preproc_output = output_file+".preproc.txt"
	tagOne_BC5CDRD_output = output_file+".BC5CDRD.taggerOne.txt"
	tagOne_NCBID_output = output_file+".NCBID.taggerOne.txt"
	tagOne_merge_output = output_file+".merge.taggerOne.txt"
	dbner_output = output_file+".dbner"
	
	runPreprocess(input_abstract, preproc_output)
	runTaggerOne(preproc_output, tagOne_BC5CDRD_model, tagOne_BC5CDRD_output)
	runTaggerOne(preproc_output, tagOne_NCBID_model, tagOne_NCBID_output)
	mergeTaggerOneOutput(tagOne_BC5CDRD_output, tagOne_NCBID_output, tagOne_merge_output)
	runDBNER(tagOne_merge_output, dbner_output)

	os.remove(preproc_output)
	os.remove(tagOne_BC5CDRD_output)
	os.remove(tagOne_NCBID_output)
	os.remove(tagOne_merge_output)
	os.remove(dbner_output+".bacteria.txt")
	os.remove(dbner_output+".disease.txt")
	os.remove(dbner_output+".tagged_abstracts.pubtator.txt")
	os.rename(dbner_output+".sentences.txt", output_file)	
def main():
	parser = setParser()
	args = parser.parse_args()
	
	input_file = os.path.abspath(args.input)
	output_file = os.path.abspath(args.output)

	runNER(input_file, output_file)

# main
if __name__ == "__main__":
	exit(main())
