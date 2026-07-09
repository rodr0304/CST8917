# Database Choice

## Selected Database

**Azure Cosmos DB for NoSQL (Serverless)**

---

## Project Requirements

This project requires a database capable of:

* Storing text analysis results in JSON format
* Supporting serverless architecture
* Integrating easily with Azure Functions
* Providing scalable storage for future growth
* Supporting fast retrieval of historical analysis records

Since the application generates structured JSON documents containing analysis statistics and metadata, a document-oriented database is the most appropriate choice.

---

## Why Azure Cosmos DB?

Azure Cosmos DB for NoSQL was selected because it natively stores JSON documents without requiring a predefined relational schema.

Each text analysis result can be stored as a single document containing:

```json
{
  "id": "12345",
  "originalText": "Hello World",
  "analysis": {
    "wordCount": 2,
    "characterCount": 11
  },
  "metadata": {
    "analyzedAt": "2026-06-10T00:00:00"
  }
}
```

This structure closely matches the application's output, eliminating the need for complex table designs or object-relational mapping.

---

## Integration with Azure Functions

Azure Cosmos DB integrates directly with Azure Functions through the Azure Cosmos Python SDK.

Benefits include:

* Simple SDK integration
* Native cloud support
* Managed service with minimal administration
* Automatic scalability
* High availability

This allows the application to remain fully serverless while persisting analysis results.

---

## Serverless Benefits

The Serverless pricing model was selected because:

* No capacity planning is required
* Charges are based on actual usage
* Ideal for low-volume educational projects
* Reduces operational costs during development and testing

For a student project with occasional requests, serverless provides the most cost-effective solution.

---

## Alternatives Considered

### Azure SQL Database

Not selected because the application data is naturally represented as JSON documents rather than relational tables.

Using a relational database would require:

* Table design
* Schema management
* Additional mapping between Python objects and database records

This would add unnecessary complexity to the project.

---

### Azure Table Storage

Not selected because it offers more limited querying capabilities compared to Cosmos DB.

While it is suitable for simple key-value storage, Cosmos DB provides greater flexibility for future enhancements.

---

### Azure Blob Storage

Not selected because Blob Storage is optimized for file storage rather than structured application data.

Querying and filtering analysis records would be significantly more difficult.

---

## Cost Considerations

Azure Cosmos DB Serverless is well suited for educational projects.

Advantages include:

* Pay-per-request pricing
* No reserved throughput costs
* No infrastructure management
* Suitable for development, testing, and demonstration environments

This minimizes operational expenses while providing enterprise-grade cloud database capabilities.

---

## Conclusion

Azure Cosmos DB for NoSQL (Serverless) was selected because it aligns closely with the application's document-based data model, integrates seamlessly with Azure Functions, supports serverless architecture principles, and offers a cost-effective solution for a cloud-native text analysis application.
