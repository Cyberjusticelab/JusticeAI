# Machine Learning Service

## Installation Instructions

1. Add Cyberjustice Lab username as environment variables: <code>export CJL_USER={USERNAME}</code> either to your .bashrc or run it as a command
2. Add Cyberjustice Lab password as environment variables: <code>export CJL_PASS={PASSWORD}</code> either to your .bashrc or run it as a command
3. Run <code>pip install -r requirements.txt</code>
4. Run <code>pip install -r requirements_test.txt</code>

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