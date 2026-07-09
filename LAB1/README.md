# CST8917 Lab 1 - Azure Functions Text Analyzer

## Overview

This project implements a serverless text analysis application using Azure Functions and Python 3.12.

The application exposes HTTP-triggered endpoints that analyze text and store the results in Azure Cosmos DB. Analysis results can later be retrieved through a history endpoint.

---

## Technologies Used

* Azure Functions
* Python 3.12
* Azure Cosmos DB for NoSQL
* Azure Cosmos Python SDK
* Azure Functions Core Tools
* Visual Studio Code
* Azurite Storage Emulator

---

## Application Architecture

```text
Client
   |
   v
TextAnalyzer Function
   |
   v
Azure Cosmos DB
   |
   v
GetAnalysisHistory Function
```

---

## Functions

### TextAnalyzer

Analyzes text submitted through an HTTP request and returns:

* Word Count
* Character Count
* Character Count (without spaces)
* Sentence Count
* Paragraph Count
* Average Word Length
* Longest Word
* Estimated Reading Time

Example:

```http
GET /api/TextAnalyzer?text=Hello%20World
```

---

### GetAnalysisHistory

Returns previously stored analysis records from Azure Cosmos DB.

Example:

```http
GET /api/GetAnalysisHistory
```

Optional limit parameter:

```http
GET /api/GetAnalysisHistory?limit=5
```

---

## Cosmos DB Configuration

Database:

```text
TextAnalyzerDB
```

Container:

```text
AnalysisHistory
```

Partition Key:

```text
/id
```

Each text analysis request is automatically stored in Azure Cosmos DB and can later be retrieved using the GetAnalysisHistory endpoint.

---

## Local Development Setup

### Prerequisites

* Python 3.12
* Azure Functions Core Tools v4
* Azure Functions VS Code Extension
* Azurite Storage Emulator

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Local Settings

Create a file named `local.settings.json` in the project root.

Example:

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "COSMOS_ENDPOINT": "<your-cosmos-endpoint>",
    "COSMOS_KEY": "<your-cosmos-key>",
    "COSMOS_DATABASE": "TextAnalyzerDB",
    "COSMOS_CONTAINER": "AnalysisHistory"
  }
}
```

---

## Running the Application

Start Azurite:

```bash
azurite
```

Start Azure Functions:

```bash
func start
```

The application will be available at:

```text
http://localhost:7071
```

Local endpoints:

```text
http://localhost:7071/api/TextAnalyzer
http://localhost:7071/api/GetAnalysisHistory
```

---

## Azure Deployment

Login to Azure:

```bash
az login
```

Deploy to Azure:

```bash
func azure functionapp publish rg-cst8917-lab1
```

---

## Production Endpoints

### Text Analyzer

```text
https://rg-cst8917-lab1-eehkbmg5d6a0audq.canadacentral-01.azurewebsites.net/api/TextAnalyzer
```

### Analysis History

```text
https://rg-cst8917-lab1-eehkbmg5d6a0audq.canadacentral-01.azurewebsites.net/api/GetAnalysisHistory
```

---

## Azure Resources

### Function App

```text
rg-cst8917-lab1
```

### Runtime

```text
Python 3.12
```

### Hosting Plan

```text
Flex Consumption
```

### Region

```text
Canada Central
```

---

## Example Response

```json
{
  "analysis": {
    "wordCount": 2,
    "characterCount": 11,
    "characterCountNoSpaces": 10,
    "sentenceCount": 1,
    "paragraphCount": 1,
    "averageWordLength": 5,
    "longestWord": "Hello",
    "readingTimeMinutes": 0
  },
  "metadata": {
    "analyzedAt": "2026-06-10T00:00:00",
    "textPreview": "Hello World"
  }
}
```

---

## Example History Response

```json
{
  "count": 1,
  "results": [
    {
      "id": "8e8c8a7f-1234-5678-9999-abcdef123456",
      "originalText": "Hello World",
      "analysis": {
        "wordCount": 2,
        "characterCount": 11
      }
    }
  ]
}
```

---

## Author

Diniz Rodrigues Martins

Algonquin College
