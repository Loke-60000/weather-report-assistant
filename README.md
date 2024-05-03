
# Weather Report Assistant Setup Guide

## Overview

This document details the setup process for the Weather Report Assistant, a chatbot application designed to deliver weather reports. The application is structured into three main services: Data Collector, NLP Module, and HTTP Server (Frontend). Each service operates within its own Docker container and is stored in separate folders as outlined below. It is essential to have a PostgreSQL database running as it is required for storing the collected weather data.

## Services and Instructions

### 1. Data Collector (`backend_weather_data_collector`)

Responsible for fetching and storing weather data, which is then used by other components of the application. This service requires a PostgreSQL database to be running.

**Location:** `backend_weather_data_collector/`

**Docker Build:**

```bash
cd data_collector_weather
docker build -t data_collector_weather .
```

**Docker Run:**

```bash
docker run -d -p 5432:5432 data_collector_weather
```

### 2. NLP Module (`backend_nlp`)

This service processes the collected weather data to generate textual and audio weather reports, making it the core component of the chatbot's response system. It also relies on the PostgreSQL database for accessing the stored data.

**Location:** `backend_nlp/`

**Docker Build:**

```bash
cd nlp_weather
docker build -t nlp_weather .
```

**Docker Run:**

```bash
docker run -d -p 8000:8000 nlp_weather
```

### 3. HTTP Server (Frontend) (`frontend`)

Hosts the user interface for the chatbot, where users can interact with the application to receive weather updates.

**Location:** `frontend/`

**Docker Build:**

```bash
cd frontend
docker build -t frontend_server .
```

**Docker Run:**

```bash
docker run -d -p 3000:3000 frontend_server
```
