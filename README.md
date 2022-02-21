# mdi_predictor

This repository proviedes the ensemble model of deep learning and parse tree-based extraction to extract microbe-disease association.

## Installation
We provide a docker environment for microbe-disease association extraction. install the docker image as follows:

```
$ docker build -rm=true -t [image_name] .
```

Our NER is based on [TaggerOne](https://www.ncbi.nlm.nih.gov/research/bionlp/tools/taggerone/). Please install TaggerOne-0.2.1 in the [NER] folder.

```
$ cd NER
$ wget https://www.ncbi.nlm.nih.gov/research/bionlp/taggerone/TaggerOne-0.2.1.tgz
$ tar -xvzf TaggerOne-0.2.1.tgz
$ cd ..
```

You can create jar files with code in [executable_jar_code] or download excutable jar files from Google Docs.
* dep_ensemble.jar https://drive.google.com/file/d/1t8-DXiP7HExqIj5cZUxSdJgd8fILZ00H/view?usp=sharing (place it in **mdi_predictor**/)
* NER/DBNER.jar https://drive.google.com/file/d/1rKBjgkyKGcCYVSlb-gOnNckx8LPhWKyb/view?usp=sharing (place it in **mdi_predictor/NER**/)


## Exec
*Run it in a docker container
### NER

NER takes a pubTator format file as input (see ```example_data/example.pubTator.txt```).
```
$ python run_ner.py --input ./input/example.pubTator.txt --output ./output/example.dbner.txt
```

### Relation Extraction
#### bi-LSTM
 * training
  ```
  $ python code/train.py --train_data=./train_data/train.txt --valida_data=./train_data/valid.txt --resource_dir=./resource/ --model=models/model.h5 --batch_size=64 --epochs=50
  ```
  
 * predicting
 ```
  $ python code/predict.py --input=./output/example.dbner.txt --output=./output/example.lstm.output.txt --resource_dir=./resource/
 ```

#### predict by ensemble of TPE and DBE 
The ensemble model extract microbe-disease associations with higher accuracy by combining TPE, which analyzes the structural pattern of the parse tree, and DBE, which explores the dpendency tree.

The ensemble model is provided as an executable jar file ```dep_ensemble.jar``` with the configuration file.
```
$ java -jar dep_ensemble.jar -i ./output/example.lstm.output.txt -o ./output/example.bdi.output.txt -c configs/config.properties
```
*If a parsed corpus file already exists, the program will not create a new parsed corpus file (the parsed corpus file is automatically named output_file_name.parsed.txt).*
