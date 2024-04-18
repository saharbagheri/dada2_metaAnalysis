This Python script is designed to facilitate the submission of various 16S amplicon datasets to the FemMicro16S pipeline for analysis. 
First, users need to add their datasets' information to the info_structure.csv file as comma separated values per row for each dataset.
Then, by executing the configuration.py script <python configuration.py>, users can automatically update each dataset information in the config.yaml file within the Snakemake pipeline directory and submit each dataset for processing on a computational cluster. 
For more details and to access the pipeline, visit the FemMicro16S GitHub repository: https://github.com/SycuroLab/FemMicro16S/tree/main.
