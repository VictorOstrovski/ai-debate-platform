# AI Debate Platform

#### Video Demo: <YOUTUBE_URL_HERE>

#### Description:

AI Debate Platform is a web application designed to analyze a statement through a structured AI debate process.

The idea behind the project is simple: instead of asking a language model to generate a single answer, the application creates a debate between two opposing sides and then asks a third AI role to evaluate the arguments and produce a verdict.

The system uses three roles:

- **PRO** – generates the strongest argument supporting a statement
- **CON** – generates the strongest argument opposing a statement
- **ARBITER** – evaluates both arguments and determines which one is stronger

For example, if a user enters the statement:

> Life is bad

the application generates one argument supporting the statement, one argument opposing the statement, and finally a judgment explaining which side presented the stronger case.

The project is implemented using Python, FastAPI, SQLite and Ollama.

The AI model runs locally through Ollama using the Qwen 2.5 1.5B model. I intentionally chose a local model instead of a cloud API because I wanted the application to be fully usable without external subscriptions or API costs.

## Main Features

- Statement-based AI debates
- Three-role architecture (PRO / CON / ARBITER)
- Editable prompts through a web interface
- Local AI execution using Ollama
- Debate history stored in SQLite
- Viewing previously generated debates
- Prompt management without modifying source code

## Application Architecture

The application follows a simple layered architecture:

```text
User Interface
       ↓
FastAPI Routes
       ↓
Debate Engine
       ↓
Prompt System
       ↓
Provider Layer
       ↓
Ollama (Local LLM)
```

The Debate Engine is responsible for orchestrating the debate process.

First, it loads prompts from external text files.

Then it sends a request to the model acting as PRO.

The second request generates the CON argument.

Finally, both arguments are passed to the ARBITER prompt which decides which side produced the stronger argument.

This separation makes the system easy to extend and modify.

## Files and Components

### main.py

This is the application's entry point.

It contains all FastAPI routes:

- Home page
- Debate generation
- Prompt editor
- Debate history
- Viewing saved debates

### debate_engine.py

This file contains the core debate logic.

It creates prompts for the different roles and coordinates communication with the language model.

The entire debate workflow is implemented here.

### provider.py

This file acts as the provider layer.

Its purpose is to isolate the application from the AI model implementation.

Currently it communicates with Ollama, but the design allows replacing the model provider later without changing the rest of the application.

### prompt_loader.py

This utility loads prompt templates from text files.

Separating prompts from Python code made prompt experimentation significantly easier.

### database.py

Handles all SQLite database operations.

Responsibilities include:

- Database initialization
- Storing debates
- Retrieving debate history
- Loading saved debates

### prompts directory

This directory contains prompt templates:

- pro.txt
- cons.txt
- arbiter.txt

The application loads these prompts dynamically.

One of my design goals was allowing non-programmers to modify debate behavior without editing Python code.

### templates directory

Contains all HTML pages used by FastAPI:

- index.html
- result.html
- prompts.html
- history.html
- saved_debate.html

## Database Design

The application uses SQLite.

The main table stores:

- id
- statement
- pro argument
- con argument
- arbiter decision
- creation date

I selected SQLite because it is simple, lightweight and does not require any external database server.

For the scale of this project it is more than sufficient.

## Prompt Editor

One feature I consider particularly important is the Prompt Editor.

Instead of hardcoding instructions inside Python files, prompts are stored separately and can be edited through a web page.

This allows rapid experimentation with debate behavior and demonstrates prompt engineering concepts.

For example, during development I adjusted prompts multiple times to force the AI to:

- Generate only one argument instead of long essays
- Focus on argument quality rather than quantity
- Force the arbiter to select a clear winner

These changes produced significantly better debates.

## Design Decisions

One design decision I debated was whether to use cloud AI APIs or a local language model.

I ultimately chose Ollama because:

- No API keys are required
- No usage fees exist
- The project can run completely offline
- Installation remains simple

Another important decision was introducing a dedicated ARBITER role.

A typical chatbot provides a single answer.

In contrast, this project evaluates competing perspectives before delivering a final verdict, which makes it more interesting and educational.

## Future Improvements

Possible future improvements include:

- Multiple AI providers
- Richer user interface
- Prompt version control

## Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ollama

Download and install Ollama.

### 3. Download model

```bash
ollama pull qwen2.5:1.5b
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

### 5. Open the browser

```text
http://127.0.0.1:8000
```

## AI Assistance Disclosure

Artificial intelligence tool MS Copilot was used during development for brainstorming, debugging assistance, prompt engineering and code suggestions.

All architecture decisions, implementation, testing, customization and final integration were performed by the project author.