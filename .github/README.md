# Research Agent API

A FastAPI-based Research Agent that performs web research using an AI agent and returns structured research reports.

The agent is designed to answer research queries by utilizing external tools such as web search and generating concise, structured responses.

---

## Deployed URLs

- Frontend: <<https://ajoy0071998-autosage-forntend.hf.space>>
- Backend: <<https://ajoy0071998-autosage.hf.space>>

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

```bash
set environment variable
TAVELI_API_KEY=your_api_key
EXA_API_KEY=your_api_key
MISTRAL_API_KEY=your_api_key
## Running the API

```bash
uvicorn main:app --reload -- port 8000
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
  "query": "Latest research in AI",
  "conversation": [
    " "
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
    "report": {
      "summary": "Artificial Intelligence (AI) continues to advance rapidly in 2025–2026, with significant progress in multimodal foundation models, autonomous AI agents, robotics, scientific discovery, and enterprise adoption. Research is increasingly focused on improving reasoning, efficiency, and safety while enabling real-world deployment across industries.",
      "keypoints": "- Advances in multimodal large language models.\n- AI agents capable of planning and tool use.\n- Significant improvements in robotics and embodied AI.\n- Increased focus on AI safety and governance.\n- Wider enterprise adoption of generative AI.",
      "important_findings": "Recent research highlights major improvements in reasoning capabilities, long-context understanding, and autonomous task execution. Organizations are integrating AI into healthcare, software engineering, finance, and scientific research. Efficiency techniques such as quantization, distillation, and Mixture-of-Experts continue to reduce deployment costs.",
      "actionable_insights": "Organizations should evaluate AI agent workflows, invest in retrieval-augmented generation for enterprise knowledge, monitor developments in open-source foundation models, and establish AI governance practices before large-scale deployment.",
      "urls": [
        "https://example.com/article1",
        "https://example.com/research-paper",
        "https://example.com/blog"
      ]
    },
    "pdf": "JVBERi0xLjQKJcTl8uXr....base64...."
  },
  "error": null,
  "processing_time": 8.41
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
