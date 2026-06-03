# Ticket Triage System

This folder contains a support ticket triage pipeline with synthetic ticket generation, AI-powered classification, human review feedback, and analytics for quality metrics.

## Overview

The ticket triage system is designed to:
- generate synthetic support tickets using `ticket_generator.py`
- classify tickets with a Gemini-powered triage engine in `triage_engine.py`
- capture human reviewer feedback via `1_Triage_Review.py`
- persist feedback into `feedback.csv` using `feedback_service.py`
- compute model quality metrics, threshold analysis, and drift dashboards in `analytics_service.py`
- display results in `2_Analytics_Dashboard.py`

## Folder Flow

1. `ticket_generator.py`
   - Builds synthetic ticket examples with categories such as Billing, Technical, Feature Request, Account Access, VIP, Cancellation Intent, Complaint Escalation, Jurisdictional, and Legal/Refund.

2. `triage_engine.py`
   - Sends ticket text to Gemini (`gemini-2.5-flash`) and returns a JSON classification response with `category`, `priority`, and `confidence`.

3. `1_Triage_Review.py`
   - Presents a sample ticket and model prediction in a Streamlit interface.
   - Allows a reviewer to confirm if the prediction is correct or choose the actual category.
   - Saves corrected feedback by calling `save_feedback()` in `feedback_service.py`.

4. `feedback_service.py`
   - Appends reviewer records to `feedback.csv`.
   - Ensures the CSV header is written once.

5. `analytics_service.py`
   - Computes key metrics such as override rate, accept rate, and accepted accuracy.
   - Generates threshold analysis for different confidence levels.
   - Builds a drift dashboard for acceptance rate over time.
   - Validates KPIs for auto-draft and acceptance thresholds.

6. `2_Analytics_Dashboard.py`
   - Loads feedback from `feedback.csv`.
   - Displays metrics, threshold analysis, and drift charts in Streamlit.

## Key Components

- `config.py`
  - Loads `GEMINI_API_KEY` from environment variables.
  - Defines `AUTO_ACCEPT_THRESHOLD` and `NEVER_AUTO_RESPOND` categories.
  - Maps escalation paths for sensitive categories.

- `ticket_generator.py`
  - Generates realistic-looking ticket fields using Faker.
  - Creates labels for category tracking.

- `triage_engine.py`
  - Builds the Gemini classification prompt.
  - Parses model output into structured JSON.

- `feedback_service.py`
  - Persists review feedback for model evaluation.

- `analytics_service.py`
  - Produces metrics that close the quality loop.

- `1_Triage_Review.py`
  - Collects human verification data.

- `2_Analytics_Dashboard.py`
  - Visualizes system performance and drift.

## Feedback Loop

The system closes the quality loop through these signals:
- model predictions are reviewed by humans
- incorrect triage decisions are marked and corrected
- feedback is stored in `feedback.csv`
- analytics compute override and acceptance rates
- results identify model gaps, threshold tuning opportunities, and drift

This workflow supports continuous improvement by letting human correction data drive evaluation and future model decisions.

## Running the System

1. Create a `.env` file with:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

2. Run the review app:
   ```bash
   streamlit run ticket_triage/1_Triage_Review.py
   ```

3. Run the analytics dashboard:
   ```bash
   streamlit run ticket_triage/2_Analytics_Dashboard.py
   ```

4. If `feedback.csv` does not exist yet, it is created automatically when feedback is saved.

## Notes

- The current triage model is configured for Gemini Flash and expects a JSON-formatted response.
- The review pipeline is currently a demo that loads a placeholder ticket; it can be extended to work with real ticket streams.
- `analytics_service.py` supports analysis and drift reporting to help identify when model quality requires intervention.
