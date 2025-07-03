# Resume‑Parser API 📄✨

A **FastAPI** microservice that reads a résumé (PDF), sends the text to OpenRouter’s GPT‑4o‑mini, and returns structured JSON data (personal details, skills, education, experience).  
The API then exposes convenient REST endpoints for each section.

---

## Table of Contents
1. [Features](#features)
2. [Architecture](#architecture)
<!-- 3. [Prerequisites](#prerequisites)
4. [Setup](#setup)
5. [Environment Variables](#environment-variables)
6. [Running the App](#running-the-app)
7. [API Reference](#api-reference)
8. [Project Structure](#project-structure)
9. [Troubleshooting](#troubleshooting)
10. [Roadmap / Ideas](#roadmap--ideas)
11. [License](#license) -->

---

## Features
- **PDF ingestion** using [`pypdf`](https://pypi.org/project/pypdf/)  
- **LLM parsing** via OpenRouter (GPT‑4o‑mini) with a strict `pydantic` schema for safe JSON output  
- **Pretty JSON** preview printed to console for quick inspection  
- **FastAPI** routes for:
  - `GET /` → raw résumé text  
  - `GET /personal_details`  
  - `GET /skills`  
  - `GET /education`  
  - `GET /experience`  
- Simple, environment‑variable‑based secret management (`dotenv`)

---

## Architecture
```text
┌──────────┐       extract_text()       ┌───────────────┐
│  PDF CV  │ ─────────────────────────▶ │   FastAPI     │
└──────────┘                            │   service     │
                                         │ (business     │
┌──────────┐       LLM request           │  logic &      │
│  OpenAI   │ ◀──────────────────────── │  endpoints)   │
│ (via      │   structured JSON          └───────────────┘
│ OpenRouter)│
└──────────┘
