import azure.functions as func
import logging
import json
import re
from datetime import datetime
import os
import uuid
from azure.cosmos import CosmosClient


COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
COSMOS_KEY = os.environ.get("COSMOS_KEY")
COSMOS_DATABASE = os.environ.get("COSMOS_DATABASE")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER")

client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.get_database_client(COSMOS_DATABASE)
container = database.get_container_client(COSMOS_CONTAINER)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="TextAnalyzer")
def TextAnalyzer(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Text Analyzer API was called!")

    text = req.params.get("text")

    if not text:
        try:
            req_body = req.get_json()
            text = req_body.get("text")
        except ValueError:
            pass

    if not text:
        instructions = {
            "error": "No text provided",
            "howToUse": {
                "option1": "Add ?text=YourText to the URL",
                "option2": "Send a POST request with JSON body: {\"text\": \"Your text here\"}",
                "example": "https://your-function-url/api/TextAnalyzer?text=Hello world"
            }
        }

        return func.HttpResponse(
            json.dumps(instructions, indent=2),
            mimetype="application/json",
            status_code=400
        )

    words = text.split()
    word_count = len(words)
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", ""))
    sentence_count = len(re.findall(r"[.!?]+", text)) or 1
    paragraph_count = len([p for p in text.split("\n\n") if p.strip()])
    reading_time_minutes = round(word_count / 200, 1)
    avg_word_length = round(char_count_no_spaces / word_count, 1) if word_count > 0 else 0
    longest_word = max(words, key=len) if words else ""

    response_data = {
        "analysis": {
            "wordCount": word_count,
            "characterCount": char_count,
            "characterCountNoSpaces": char_count_no_spaces,
            "sentenceCount": sentence_count,
            "paragraphCount": paragraph_count,
            "averageWordLength": avg_word_length,
            "longestWord": longest_word,
            "readingTimeMinutes": reading_time_minutes
        },
        "metadata": {
            "analyzedAt": datetime.utcnow().isoformat(),
            "textPreview": text[:100] + "..." if len(text) > 100 else text
        }
    }

    document_id = str(uuid.uuid4())

    document = {
        "id": document_id,
        "originalText": text,
        "analysis": response_data["analysis"],
        "metadata": response_data["metadata"]
    }

    container.create_item(body=document)

    response_data["id"] = document_id

    return func.HttpResponse(
        json.dumps(response_data, indent=2),
        mimetype="application/json",
        status_code=200
    )


@app.route(route="GetAnalysisHistory")
def GetAnalysisHistory(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Get Analysis History API was called!")

    try:
        limit = int(req.params.get("limit", 10))

        query = f"""
        SELECT TOP {limit}
            c.id,
            c.analysis,
            c.metadata,
            c.originalText
        FROM c
        """

        items = list(
            container.query_items(
                query=query,
                enable_cross_partition_query=True
            )
        )

        response = {
            "count": len(items),
            "results": items
        }

        return func.HttpResponse(
            json.dumps(response, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}, indent=2),
            mimetype="application/json",
            status_code=500
        )
