# CST8917 Lab 1 - Azure Functions Text Analyzer

## Overview

This project implements a serverless text analysis application using Azure Functions and Python 3.12.

The application exposes HTTP-triggered endpoints that analyze text and store the results in Azure Cosmos DB. Analysis results can later be retrieved through a history endpoint.

---

## Technologies Used

* Azure Functions
* Python 3.12
* Azure Cosmos DB (NoSQL)
* Azure Functions Core Tools
* Visual Studio Code
* Azurite Storage Emulator

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
    "analyzedAt": "2026-06-09T20:00:00",
    "textPreview": "Hello World"
  }
}
```

---

## Author

Diniz Rodrigues Martins

Course: CST8917 - Serverless Applications

Algonquin College
