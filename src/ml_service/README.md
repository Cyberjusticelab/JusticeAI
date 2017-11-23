# Machine Learning Service

## Installation Instructions

1. Add Cyberjustice Lab username as environment variables: <code>export CJL_USER={USERNAME}</code> either to your .bashrc or run it as a command
2. Add Cyberjustice Lab password as environment variables: <code>export CJL_PASS={PASSWORD}</code> either to your .bashrc or run it as a command
3. Run <code>pip install -r requirements.txt</code>
4. Run <code>pip install -r requirements_test.txt</code>

### File Structure:

```

----| data <all data input and output>
--------| raw <extract the raw data here>
--------| binary <all saved binarized model/data>
--------| cache <temp files>
--------| cluster
------------| fact
------------| decision

----| feature_extraction <all data manipulation before supervised training>
--------| clustering
------------| dbscan
------------| hdbscan
------------| k_means
------------| optimization
------------| clustering.py <driver for clustering>
--------| pre_processing
------------| precedent_model
------------| regex_parse
------------| word_vector
------------| pre_processing.py <driver for pre_processing>
------------| pre_processor.py
--------| post_processing
------------| precedent_vector
------------| post_processing.py <driver for post_processing>
--------| feature_extraction.py <driver for feature extraction (using 3 drivers above)>

----| model_learning <supervised training>
------------| neural_net
------------| model_training.py <driver for supervised training>

----| util <common tool>
------------| log.py <logging tool>
------------| file.py <file save and load>
------------| constant.py <global variables>

init.py
main.py <driver for the pipeline (feature extraction + model training>

```

## Extracting Data

- For binarized data and model, place under `data/binary`
- For precedent raw data (*.txt), place under `data/raw`
- Run `python init` to download French word vector

## Run Tests and Lints

```
export COMPOSE_FILE=ci
./cjl up -d && ./cjl run ml_service
```

## Using Azure
1- cd JusticeAi
2- Run python3 -m src.ml_service.main to start
3- All outputs will be sotred in JusticeAi/src/ml_service/data/cluster
   cd to this directory to view, get, move them
4- Running the algorithm will overrite any existing files in the output folder.
5- Outputs are saved as text files and as binary models. The text files represent the clusters while the binary file is the model itself.