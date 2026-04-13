# 🧠 System Architecture

## Overview

This system processes user queries using an AI agent with guardrails to ensure safe and accurate responses.

## Workflow

1. User enters query
2. Input guardrails check query
3. FAQ data is searched
4. Response is generated
5. Output guardrails validate response
6. Final answer is shown

## Components

* Input Guardrails → filter bad queries
* Retrieval System → fetch FAQ answers
* AI Agent → generate response
* Output Guardrails → ensure safety

## Key Features

* Prevents harmful input
* Avoids wrong answers (hallucination)
* Works only in FAQ domain
