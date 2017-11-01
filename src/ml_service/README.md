# Machine Learning Service

## Extract Facts from Data

1. Download the precedent data
2. Extract the zip to the root directory (e.g. JusticeAI/text_bk)
3. Run <code>python feature_extraction/fact_clustering/main.py</code>

## Run Tests and Lints

```
export COMPOSE_FILE=ci
./cjl up -d && ./cjl run ml_service
```