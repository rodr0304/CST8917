# Database Choice

## Selected Database

Azure Cosmos DB for NoSQL (Serverless)

## Justification

Azure Cosmos DB is the best choice for this project because it stores JSON documents natively, which matches the structure of the Text Analyzer results.

The serverless pricing model is cost-effective for student projects because charges only occur when requests are made.

Cosmos DB integrates well with Azure Functions and provides excellent Python SDK support.

It also scales automatically and follows serverless architecture principles.

## Alternatives Considered

### Azure SQL Database

Rejected because the project data is naturally represented as JSON documents rather than relational tables.

### Azure Table Storage

Rejected because querying capabilities are more limited than Cosmos DB.

### Azure Blob Storage

Rejected because it is designed for file storage rather than structured application data.

## Cost Considerations

Cosmos DB offers a serverless pricing model and free-tier options that are suitable for educational and development environments. Costs are based on actual usage rather than reserved capacity.
