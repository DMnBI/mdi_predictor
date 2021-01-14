import sys

def getIO(file_path, type):
    fileReader = open(file_path, type)
    return fileReader

def writeAbstracts(writer, abstracts):
    isFirst = True
    for abst in abstracts:
        if isFirst:
            writer.write(abst+'\n')
        else:
            annotation = getOnlyAnnotation(abst)
            if annotation is not "":
                writer.write(annotation+'\n')
        isFirst = False

    writer.write('\n')

def getOnlyAnnotation(abstract):
    abst_arr = abstract.split('\n')
    anno_str = "\n"
    for annotation in abst_arr[2:]:
        anno_str = annotation+'\n'
    return anno_str.strip()

def getAbstract(file_reader):
    abstract = ""
    while True:
        eachline = file_reader.readline()

        if not eachline: break
        elif len(eachline) <= 2: break
        elif "|t|" in eachline:
            abstract = eachline
        elif "|a|" in eachline:
            abstract = abstract+eachline
        else:
            abstract = abstract+eachline
    return abstract.strip()           

def main():
    if len(sys.argv) == 1:
        print "please input TaggerOne output."
        exit(1)

    tagOne_fileList = sys.argv[1:-1]
    tagOne_fileReaders = []
    for tagOne_file in tagOne_fileList:
        print tagOne_file
        tagOne_fileReaders.append(getIO(tagOne_file, 'r'))
    
    output_writer = getIO(sys.argv[-1], 'w')
    while True:
        abst_list = []
        for reader in tagOne_fileReaders:
            abst = getAbstract(reader)
            if abst == "":
                break
            abst_list.append(abst)
        if len(abst_list) <= 0:
            break
        writeAbstracts(output_writer, abst_list)
    output_writer.flush()
    output_writer.close()

if __name__ == "__main__":
    exit(main())
