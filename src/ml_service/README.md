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
