This Python script is designed to facilitate the submission of various 16S amplicon datasets to the FemMicro16S pipeline for analysis.
<br>
First, users need to add the raw fastq files of each dataset to the raw_data directory within each dataset's sub directory.
<br>
Second, add the datasets parameters to the info_structure.csv file as comma separated values per row for each dataset.
These parameters are the flags that can be found in the config.yaml file within the snakemake pipeline. For more details and to access the pipeline, visit the FemMicro16S GitHub repository: (https://github.com/SycuroLab/FemMicro16S/tree/main).
<br>
Then, by executing the configuration.py script <python configuration.py>, users can automatically update each dataset information in the config.yaml file within the Snakemake pipeline directory and submit each dataset for processing on a computational cluster. 
