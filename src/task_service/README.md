# Optical Character Recognition Service

## Run Tests and Lints

```
export COMPOSE_FILE=ci
./cjl up -d && ./cjl run ocr_service
```

---
# OCR API

## Extract Text

From provided image data, returns the text extracted from this data as a string.

**URL** : `/ocr/extract_text`

**Method** : `POST`

**Headers** : `multipart/form-data`

**Data constraints**

Provide the 'file' key with image data data as the value.

#### Success Response

**Code** : `200 OK`

#### Error Response

**Code** : `400 Bad Request` - *No file key or no image data provided*


