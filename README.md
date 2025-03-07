Advertising Metrics API

Overview

The Advertising Metrics API is a FastAPI-based backend that manages advertising performance metrics. It includes a scheduled background job using APScheduler, which runs every 6 hours asynchronously to log timestamps.

Setup & Installation

Prerequisites

Python 3.8+

PostgreSQL (if using database features)

Virtual Environment (recommended)

Clone the Repository
git clone https://github.com/your-repo/advertising-metrics-api.git
cd advertising-metrics-api

Create a Virtual Environment & Install Dependencies

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

Running the Application

Start FastAPI Application

uvicorn main:app --host 0.0.0.0 --port 8000 --reload