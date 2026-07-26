# FleetBook – Booking Evaluation System

**Course:** CST8917 – Lab 3: Azure Functions, Logic Apps & Serverless Computing

## 🎥 Video Demo

[Watch the demo on YouTube](https://youtu.be/N2hjmwXREZs)

## Overview

FleetBook is a serverless vehicle booking evaluation system built using **Azure Functions** and **Azure Logic Apps**.

The application receives booking requests through an HTTP endpoint, evaluates vehicle availability from a mock fleet database, calculates rental pricing, and returns a JSON response indicating whether the booking is confirmed or rejected.

This project demonstrates how Azure serverless services can be integrated to automate business workflows without managing infrastructure.

---

## Architecture

```
Client
   │
   ▼
HTTP POST Request
   │
   ▼
Azure Logic App
   │
   ▼
Azure Function
   │
   ├── Validate Request
   ├── Search Fleet
   ├── Calculate Pricing
   └── Generate Response
   │
   ▼
Logic App Response
   │
   ▼
JSON Result
```

---

## Technologies Used

- Microsoft Azure
- Azure Functions (Python)
- Azure Logic Apps
- HTTP Trigger
- JSON
- Python 3.x

---

## Features

- HTTP-triggered booking requests
- Vehicle availability validation
- Mock fleet management
- Vehicle selection based on lowest mileage
- Rental price calculation
- Optional add-ons
  - GPS
  - Child Seat
  - Insurance Upgrade
- Weekly discount for rentals of 7 days or more
- JSON API responses
- Health check endpoint

---

## Project Structure

```
FleetBook/
│
├── function_app.py
├── host.json
├── requirements.txt
├── local.settings.json
└── README.md
```

---

## Fleet Data

The application uses a mock fleet database containing:

- Vehicle ID
- Vehicle Type
- Availability
- Location
- Mileage
- Daily Rental Rate

Example:

| ID | Type | Location | Available |
|----|----------|----------|-----------|
| V001 | Sedan | Ottawa | Yes |
| V002 | SUV | Toronto | Yes |
| V009 | SUV | Ottawa | Yes |

---

## Request Example

```json
{
  "bookingId": "BK001",
  "customerName": "Diniz Martins",
  "customerEmail": "diniz@email.com",
  "vehicleType": "SUV",
  "pickupLocation": "Ottawa",
  "pickupDate": "2026-08-01",
  "returnDate": "2026-08-05",
  "notes": "GPS, insurance"
}
```

---

## Successful Response Example

```json
{
  "bookingId": "BK001",
  "customerName": "Diniz Martins",
  "customerEmail": "diniz@email.com",
  "status": "confirmed",
  "vehicleId": "V009",
  "vehicleType": "SUV",
  "location": "Ottawa",
  "estimatedPrice": 395,
  "reason": "Vehicle V009 (SUV) available in Ottawa."
}
```

---

## Booking Evaluation Logic

The Azure Function performs the following steps:

1. Receives the booking request.
2. Validates required fields.
3. Searches the fleet for matching vehicles.
4. Filters available vehicles.
5. Selects the vehicle with the lowest mileage.
6. Calculates the estimated rental cost.
7. Returns a confirmation or rejection response.

---

## Pricing Rules

Base price:

```
Daily Rate × Number of Days
```

Optional add-ons:

| Add-on | Cost |
|---------|------|
| GPS | $5/day |
| Child Seat | $10/day |
| Insurance Upgrade | $15/day |

Discount:

- 10% discount for rentals lasting 7 days or longer.

---

## Azure Services

### Azure Function

Responsible for:

- Business logic
- Fleet validation
- Pricing calculation
- JSON response generation

---

### Azure Logic App

Responsible for:

- Receiving HTTP requests
- Calling the Azure Function
- Returning the function response to the client

---

## Health Endpoint

```
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "FleetBook Function App",
  "fleet_size": 10
}
```

---

## Learning Objectives

This project demonstrates:

- Serverless Computing
- Azure Functions
- Azure Logic Apps
- Workflow Automation
- HTTP APIs
- JSON Processing
- Business Rule Implementation
- Cloud Integration

---

## Author

**Diniz Rodrigues Martins**

Cloud Development and Operations  
Algonquin College – Ottawa, Canada

---

