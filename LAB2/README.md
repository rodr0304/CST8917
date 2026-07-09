# CST8917 - Lab 2: Azure Durable Functions Image Analyzer

## Overview

This project implements an event-driven image processing pipeline using Azure Durable Functions.

Whenever a new image is uploaded to the Azure Blob Storage **images** container, a Blob Trigger starts a Durable Function orchestration that performs multiple image analyses in parallel before generating a final report and storing the results in Azure Table Storage.

---

# Architecture

```
Blob Storage
      │
      ▼
Blob Trigger
      │
      ▼
Durable Orchestrator
      │
      ├── analyze_colors
      ├── analyze_objects
      ├── analyze_text
      └── analyze_metadata
              │
              ▼
      generate_report
              │
              ▼
       store_results
              │
              ▼
 Azure Table Storage
```

---

# Technologies Used

- Azure Functions (Python v2 Programming Model)
- Azure Durable Functions
- Azure Blob Storage
- Azure Table Storage
- Pillow (PIL)
- Azure Storage SDK

---

# Project Structure

```
function_app.py
host.json
requirements.txt
local.settings.example.json
test-function.http
```

---

# Durable Function Workflow

The orchestration follows a hybrid pattern:

1. Blob Trigger detects a new image.
2. Durable Orchestrator starts.
3. Four Activity Functions execute in parallel:
   - Analyze Colors
   - Analyze Objects
   - Analyze Text
   - Analyze Metadata
4. Results are merged.
5. Report is generated.
6. Results are stored in Azure Table Storage.
7. HTTP endpoint returns stored analysis.

---

# Challenges Encountered

## Blob Trigger not executing

One of the main challenges during development was that the Blob Trigger was not starting automatically after uploading images.

Several possible causes were investigated, including:

- Incorrect storage connection strings
- Deployment synchronization
- Azure Function publishing
- Durable Function registration
- Blob Storage permissions
- Trigger synchronization
- Azure Flex Consumption behavior

After validating all configuration settings, the Function App was republished, connection strings were verified, and Blob Storage permissions were confirmed. The project was also tested using Azure Portal uploads and Azure Storage Account containers.

---

## Azure Portal Authentication

Uploading files using Microsoft Entra authentication initially resulted in permission errors.

The issue was resolved by switching the Storage Account authentication method to **Access Key**, allowing successful blob uploads.

---

## Local Configuration

Sensitive connection strings were removed from the repository.

A template configuration file (`local.settings.example.json`) was created so the project can be configured locally without exposing credentials.

---

# Security Considerations

The repository does **not** include:

- Azure Storage Account keys
- Local connection strings
- Secrets
- Sensitive configuration

Developers should copy:

```
local.settings.example.json
```

to

```
local.settings.json
```

and replace the placeholder values with their own Azure Storage credentials.

---

# Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the Azure Functions host:

```bash
func start
```

Upload an image to the **images** container to trigger the workflow.

---

# HTTP Endpoint

Retrieve stored analysis results:

```
GET /api/results
```

or

```
GET /api/results/{id}
```

---

# Lessons Learned

This project provided practical experience with:

- Azure Durable Functions
- Fan-Out / Fan-In orchestration
- Blob Storage Triggers
- Azure Table Storage
- Event-driven serverless architectures
- Azure Function deployment
- Azure Storage authentication
- Troubleshooting Azure trigger execution

---

# Author

Diniz Martins

Algonquin College

Cloud Development and Operations
