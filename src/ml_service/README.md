# Machine Learning Service

## Installation Instructions

1. Add Cyberjustice Lab username as environment variables: <code>export CJL_USER={USERNAME}</code> either to your .bashrc or run it as a command
2. Add Cyberjustice Lab password as environment variables: <code>export CJL_PASS={PASSWORD}</code> either to your .bashrc or run it as a command
3. Run <code>pip install -r requirements.txt</code>
4. Run <code>pip install -r requirements_test.txt</code>



## Extract Facts from Data

1. Download the precedent data
2. Extract the zip to the root directory (e.g. JusticeAI/text_bk)
3. Run <code>python feature_extraction/fact_clustering/main.py</code>

## Run Tests and Lints

```
export COMPOSE_FILE=ci
./cjl up -d && ./cjl run ml_service
```

## Using Azure
1 - cd JusticeAi
2- python3 -m src.ml_service.feature_extraction.main <command>
3- The <command> list is as follows (a '/' indicates an 'or'):

    i) --dbscan -facts/decisions min_sample_size epsilon
       example: --dbscan -facts 10 0.3

    ii) --hdbscan -facts/decisions min_cluster_size min_sample_size
       example: --hdbscan -decisions 20 5

    iii) k-means ** still needs refactoring

    iv) --parse -facts/decision
       example: --parse -facts
       ** this command generates the preprocessing models needed for the clustering

4- The preprocessing models need to be moved to JusticeAi/src/ml_service/ml_models/
   The reason they are not automatically moved is to prevent the risk of overwriting
   a previously better model

5- All outputs will be sotred in JusticeAi/src/ml_service/output/*
   cd to this directory to view, get, move them

6- Running the algorithm will overrite any existing files for that particular
   algorithm in the output folder.
        (running hdbscan twice consecutively will destroy the first run's results)
        (running k-means followed by hdbscan won't destroy results -- they are saved in seperate folders)

   **If you run DBSCAN then please clear JusticeAi/src/ml_service/output/dbscan_cluster_dir/
     The algorithm will overrite files, however if cluster size is lesser than the
     previous run then you will not overrite ALL files and you will end up with more text files than actual clusters.
     The binary model however will always be the most up to date.

7- Outputs are saved as text files and as binary models. The text files represent
   the clusters while the binary file is the model itself.