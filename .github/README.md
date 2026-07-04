# Research Agent API

A FastAPI-based Research Agent that performs web research using an AI agent and returns structured research reports.

The agent is designed to answer research queries by utilizing external tools such as web search and generating concise, structured responses.

---

## Features

- REST API built with FastAPI
- AI-powered research agent
- Web search tool integration
- Structured JSON responses
- Health check endpoint
- Processing time tracking
- Error handling and logging

---

## Tech Stack

- Python 3.12+
- FastAPI
- Pydantic
- Uvicorn

---

## Agent Architecture

The Research Agent uses the following tools:

### 1. Web Search Tool

Used to search the internet for relevant and up-to-date information.
**Purpose**

- Search recent information
- Collect reliable sources
- Retrieve factual data
- Support research with references

## Installation

Clone the repository

```bash
git clone <https://github.com/acrobyte007/AutoSage>
cd project
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the API

```bash
uvicorn main:app --reload
```

The server starts on

bash```
<<http://localhost:8000>>

## API Endpoints

### Health Check

**GET /health**
Example response

```json
{
  "status": "ok",
}
```

---

### Research

**POST /research**
Performs research on the given query.

#### Request

```json
{
  "query": "Latest advancements in quantum computing",
  "conversation": [
    "Focus on practical applications."
  ]
}
```

`conversation` is optional.

---

#### Successful Response

```json
{
  "success": true,
  "data": {
    "report": "...",
    "sources": [
      "https://..."
    ]
  },
  "error": null,
  "processing_time": 2.41
}
```

---

#### Error Response

```json
{
  "success": false,
  "data": null,
  "error": "Error message",
  "processing_time": 0.21
}
```

---

## API Documentation

Interactive Swagger UI

bash```
<<http://localhost:8000/docs>>

## Example cURL

```bash
curl -X POST "http://localhost:8000/research" \
-H "Content-Type: application/json" \
-d '{
    "query":"Explain Retrieval-Augmented Generation",
    "conversation":[]
}'
```

---

## Logging

Application logs are handled through the custom logger located at

bash```
logger/logger.py

Logs include:

- Incoming requests
- Processing status
- Errors and exceptions

---

## Response Model

| **Field** | **Type** | **Description** |
| success | boolean | Request status |
| data | object | Research response |
| error | string | Error message if any |
| processing_time | float | Time taken in seconds |

---

## Future Improvements

- Citation validation
- Source ranking
- Research caching
- Authentication
- Rate limiting
- Async background research
- PDF report generation
