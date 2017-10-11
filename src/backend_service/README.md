# Backend Service

## Run Tests

```
./cjl up -d && ./cjl run --rm backend_service bash -c "pytest"
```

## Run Lints

```
./cjl up -d && ./cjl run --rm backend_service bash -c "flake8"
```

