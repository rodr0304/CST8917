
# PhotoPipe --- Event-Driven Image Processing with Azure Event Grid & Functions

**Course:** CST8917 --- Serverless Applications\
**Lab:** Lab 4 --- PhotoPipe\
**Student:** Diniz Rodrigues Martins

## Overview

PhotoPipe is an event-driven image processing pipeline built with Azure
Blob Storage, Azure Event Grid, Azure Functions, and Azure Table
Storage.

Files are uploaded through a web client to the `image-uploads`
container. Azure Event Grid detects `BlobCreated` events and routes them
to Azure Functions. JPG and PNG images are processed and metadata is
stored in the `image-results` container, while uploads are also recorded
in Table Storage for auditing.

## Architecture

``` text
Upload File
    |
    v
[ Blob Storage ]
  image-uploads
    |
    v
[ Event Grid System Topic ]
    |
    +------------------------------+
    |                              |
    v                              v
[ process-image ]              [ audit-log ]
 JPG / PNG only                All uploads
    |                              |
    v                              v
[ image-results ]             [ Table Storage ]
 Metadata JSON                 processinglog
```

## Azure Services Used

-   **Azure Blob Storage**
    -   `image-uploads` --- receives uploaded files
    -   `image-results` --- stores generated metadata JSON files
-   **Azure Event Grid** --- captures BlobCreated events
-   **Azure Functions** --- processes images and exposes HTTP endpoints
-   **Azure Table Storage** --- stores the processing audit trail
-   **PhotoPipe Web Client** --- uploads files and displays results and
    audit entries

## Azure Functions

### `process-image`

Event Grid-triggered function that processes JPG and PNG uploads. It
extracts information from the BlobCreated event and creates a metadata
JSON file in `image-results`.

Generated metadata includes:

-   Original file name and URL
-   Content type
-   File size
-   Processing timestamp
-   Event information
-   Simulated image dimensions
-   Thumbnail reference

### `audit-log`

Event Grid-triggered function that records uploads from the
`image-uploads` container in the `processinglog` Azure Table.

The audit entry contains information such as:

-   Blob name and URL
-   Content type
-   Content length
-   Event type
-   Event timestamp
-   Processing timestamp
-   Status

### `get-results`

HTTP-triggered function that retrieves the metadata JSON files stored in
`image-results`.

Endpoint:

``` text
/api/get-results
```

### `get-audit-log`

HTTP-triggered function that retrieves audit entries from the
`processinglog` table.

Endpoint:

``` text
/api/get-audit-log
```

### `health`

HTTP endpoint used to verify that the Function App is running.

Endpoint:

``` text
/api/health
```

Expected response:

``` json
{
  "status": "healthy",
  "service": "PhotoPipe Function App"
}
```

## Event Grid Configuration

Two Event Grid subscriptions are used.

### Image Processing Subscription

Routes BlobCreated events from `image-uploads` to the `process-image`
function.

The subscription filters image files so that only:

``` text
.jpg
.png
```

are processed.

### Audit Log Subscription

Routes BlobCreated events from the `image-uploads` container to the
`audit-log` function.

This subscription does not use a file-extension filter, allowing image
and non-image uploads to be recorded in the audit log.

## Project Files

``` text
LAB4/
├── client.html
├── function_app.py
├── host.json
├── requirements.txt
├── test-function.http
├── local.settings.example.json
├── .funcignore
├── .gitignore
└── README.md
```

Sensitive/local files such as `local.settings.json`, SAS tokens, storage
account keys, virtual environments, and Azurite data must not be
committed.

## Requirements

The Python dependencies are defined in `requirements.txt`.

Install them with:

``` bash
python -m pip install -r requirements.txt
```

## Local Configuration

Create `local.settings.json` based on `local.settings.example.json`.

Example:

``` json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "STORAGE_CONNECTION_STRING": "<your-storage-account-connection-string>"
  },
  "Host": {
    "CORS": "*"
  }
}
```

Replace the placeholder with the appropriate Azure Storage connection
string.

> **Security:** Never commit the real `local.settings.json`, storage
> account keys, connection strings, or SAS tokens to GitHub.

## Running the Web Client

Start a local HTTP server from the Lab 4 directory:

``` bash
python3 -m http.server 5500
```

Then open:

``` text
http://localhost:5500/client.html
```

Configure the web client with:

-   Storage Account Name
-   SAS Token
-   Function App URL

The Function App must allow the web client's origin through CORS.

## Testing

### JPG Upload

Uploading a `.jpg` file should:

1.  Store the file in `image-uploads`
2.  Generate a BlobCreated event
3.  Trigger `process-image`
4.  Create metadata in `image-results`
5.  Trigger `audit-log`
6.  Create an entry in `processinglog`

### PNG Upload

Uploading a `.png` file should produce the same processing and audit
behavior as JPG.

### Non-Image Upload

Uploading a non-image file such as `.txt` should:

1.  Store the file in `image-uploads`
2.  Trigger the audit subscription
3.  Create an audit entry in `processinglog`
4.  **Not** create an image processing result

This demonstrates Event Grid filtering between different subscriptions.

## Monitoring

Event Grid metrics can be used to verify event delivery, including:

-   Published Events
-   Matched Events
-   Delivery Succeeded Events

Processing results can also be verified in the `image-results` Blob
container and audit entries in the `processinglog` Table Storage table.

## Demo Video

YouTube demo: https://youtu.be/xQaZLX7j-sI



## Security Notes

This project is configured for educational/lab use. Some settings, such
as permissive CORS or anonymous blob access, should be restricted in a
production environment. Production systems should use appropriately
scoped authentication and short-lived SAS tokens.
