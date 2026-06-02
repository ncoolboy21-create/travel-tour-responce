# Ticket Triage System - Documentation

## Overview

The **Ticket Triage System** is an AI-powered support ticket classification pipeline that combines synthetic data generation with intelligent ticket categorization. It enables organizations to automatically triage incoming support tickets, capture human feedback, and measure model performance metrics like override rates and calibration.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    TICKET TRIAGE PIPELINE                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │  faker_fake_tickets.py                  │
        │  ─────────────────────────────────────  │
        │  • Generate synthetic tickets (Faker)   │
        │  • Generate realistic tickets (Gemini)  │
        │  • Triage tickets with Gemini Flash     │
        │  • Capture feedback & override metrics  │
        └─────────────────────────────────────────┘
                              │
                    ┌─────────┴──────────┐
                    ▼                    ▼
          triage_results.csv    Override Rate Metrics
                    │
                    ▼
        ┌─────────────────────────────────────────┐
        │  streamlit_feedback.py                  │
        │  ─────────────────────────────────────  │
        │  • Interactive feedback UI              │
        │  • Review predictions vs actual         │
        │  • Submit human corrections             │
        │  • Persist feedback to CSV              │
        └─────────────────────────────────────────┘
                              │
                              ▼
                        feedback.csv
                    (Human corrections)
```

---

## Scripts Overview

### 1. **faker_fake_tickets.py** 
**Purpose:** Generate synthetic support tickets and perform AI-based triage

#### Key Functions:

| Function | Purpose |
|----------|---------|
| `generate_ticket()` | Creates realistic fake tickets using Faker library with random categories (billing, technical, feature request, account access, performance) |
| `triage_ticket(ticket_text)` | Classifies tickets using Google Gemini 2.5 Flash model into predefined categories with priority levels |

#### Workflow:

```
Step 1: Generate Fake Tickets (Faker)
   └─> Creates 100 synthetic support tickets
   └─> Each ticket has: ticket_id, customer name, email, subject, description
   └─> Random categories: billing issue, technical bug, feature request, account access, performance issue

Step 2: Generate Additional Realistic Tickets (Gemini 2.5 Flash)
   └─> Uses Gemini to create realistic SaaS support ticket examples
   └─> Demonstrates prompt-based synthetic generation

Step 3: Triage Tickets (Gemini 2.5 Flash)
   └─> Sends each ticket to Gemini model
   └─> Model returns classification + priority level (Low, Medium, High)
   └─> Results saved to: triage_results.csv

Step 4: Calculate Feedback Metrics
   └─> Compares predicted vs human-verified categories
   └─> Calculates Override Rate (% of incorrect predictions)
   └─> Identifies model calibration issues
```

#### Input & Output:

**Input:**
- Gemini API Key (via `.env` file)
- 100 synthetic tickets generated internally

**Outputs:**
- `triage_results.csv` - Predictions for all tickets
- Console output - Override rate metrics

**Sample Output:**
```json
{
  "ticket_id": "550e8400-e29b-41d4-a716-446655440000",
  "customer": "John Doe",
  "email": "john@example.com",
  "subject": "Billing Issue",
  "description": "I was charged twice for my subscription this month...",
  "actual_category": "billing issue"
}
```

---

### 2. **streamlit_feedback.py**
**Purpose:** Interactive UI for human review and feedback capture on ticket classifications

#### Features:

| Feature | Description |
|---------|-------------|
| Ticket Display | Shows support ticket subject and current AI prediction |
| Feedback Form | User rates prediction accuracy (Yes/No) |
| Category Selector | User selects actual correct category if prediction was wrong |
| Persistent Storage | Appends feedback to `feedback.csv` for model improvement |

#### Workflow:

```
Step 1: Load Ticket & Display
   └─> Show ticket subject from triage results
   └─> Display current AI prediction (e.g., "Technical")

Step 2: Human Review Interface
   └─> User sees radio button: "Was prediction correct?"
   └─> Options: Yes / No

Step 3: Correction (if wrong)
   └─> User selects actual category from dropdown
   └─> Dropdown options: Technical, Billing, Feature, Access

Step 4: Submit & Persist
   └─> User clicks "Submit"
   └─> Feedback saved to: feedback.csv (append mode)
   └─> Success message displayed

Step 5: Iterate
   └─> Load next ticket from queue
   └─> Repeat Steps 1-4
```

#### Input & Output:

**Input:**
- Streaming ticket from triage pipeline
- User feedback via interactive UI

**Outputs:**
- `feedback.csv` - Appended human feedback records
- Structured format: `[subject, predicted_category, actual_category, correct]`

---

## Data Flow Diagram

```
┌─────────────────────┐
│ Faker Library       │  (Generate 100 synthetic tickets)
│ ─────────────────   │
│ • Names             │
│ • Emails            │
│ • Descriptions      │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │ Ticket Pool  │  (100 realistic support tickets)
    │ (Memory)     │
    └──────┬───────┘
           │
           ├────────────────────┐
           │                    │
           ▼                    ▼
    ┌────────────────┐   ┌─────────────────┐
    │ Gemini Flash   │   │ Gemini Flash    │
    │ (Triage)       │   │ (Generate)      │
    │                │   │                 │
    │ Input: ticket  │   │ Input: prompt   │
    │ Output: class  │   │ Output: ticket  │
    └────────┬───────┘   └────────┬────────┘
             │                    │
             ▼                    ▼
    ┌─────────────────────────────────┐
    │ triage_results.csv              │
    │ ─────────────────────────────    │
    │ ticket_id | prediction | ...     │
    └────────────┬────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────┐
    │ Streamlit Feedback UI            │
    │ ──────────────────────────────   │
    │ • Display ticket                 │
    │ • Show prediction                │
    │ • Collect human feedback         │
    │ • Store corrections              │
    └────────────┬─────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────┐
    │ feedback.csv                     │
    │ ──────────────────────────────   │
    │ ticket_id | predicted | actual   │
    │           | correct   | ...      │
    └──────────────────────────────────┘
```

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Google Gemini API Key
- Required Libraries

### 1. Install Dependencies

```bash
pip install faker google-generativeai pandas streamlit python-dotenv
```

### 2. Configure Environment Variables

Create a `.env` file in the `ticket_triage/` directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Note:** Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### 3. Directory Structure

```
ticket_triage/
├── faker_fake_tickets.py      # Synthetic ticket generation & triage
├── streamlit_feedback.py       # Feedback collection UI
├── README.md                   # This file
├── triage_results.csv          # Generated outputs (auto-created)
├── feedback.csv                # Generated outputs (auto-created)
└── .env                        # Environment variables (user-created)
```

---

## Running the Scripts

### Option 1: Generate & Triage Tickets

```bash
python faker_fake_tickets.py
```

**What it does:**
1. Generates 100 synthetic tickets using Faker
2. Sends each to Gemini for triage classification
3. Saves predictions to `triage_results.csv`
4. Displays override rate metrics in console

**Expected Output:**
```
Override Rate: 0.15
Triage Results saved to triage_results.csv
```

---

### Option 2: Launch Feedback UI

```bash
streamlit run streamlit_feedback.py
```

**What it does:**
1. Opens interactive web interface at `http://localhost:8501`
2. Displays tickets and AI predictions
3. Collects human corrections
4. Saves feedback to `feedback.csv`

**How to Use:**
1. View ticket subject and AI prediction
2. Click "Yes" if prediction was correct, or "No" if incorrect
3. If "No", select the actual category from dropdown
4. Click "Submit"
5. Feedback is saved; UI refreshes for next ticket

---

## Output Files

### `triage_results.csv`

Contains AI predictions for all tickets.

| Column | Description |
|--------|-------------|
| ticket_id | Unique identifier (UUID) |
| prediction | AI-predicted category (JSON from Gemini) |

**Sample:**
```
ticket_id,prediction
550e8400-e29b-41d4-a716-446655440000,"{""category"": ""Technical"", ""priority"": ""High""}"
```

---

### `feedback.csv`

Accumulates human corrections and feedback for model improvement.

| Column | Description |
|--------|-------------|
| subject | Ticket subject line |
| predicted_category | What AI predicted |
| actual_category | What human confirmed |
| correct | Boolean: was AI correct? |

**Sample:**
```
subject,predicted_category,actual_category,correct
"Unable to access account","Technical","Account Access","No"
"Invoice not received","Billing","Billing","Yes"
```

---

## Performance Metrics

### Override Rate

Defined as: **% of tickets where human disagreed with AI prediction**

```
Override Rate = (Number of Incorrect Predictions) / (Total Predictions)
```

**Interpretation:**
- **Low override rate (< 10%):** Model is reliable; requires minimal human review
- **Medium override rate (10-20%):** Model shows decent performance; some manual QA needed
- **High override rate (> 20%):** Model needs retraining or prompt refinement

---

## Calibration Analysis

To measure model confidence vs acceptance rates, analyze `feedback.csv`:

```python
import pandas as pd

# Load feedback
feedback = pd.read_csv("feedback.csv")

# Calculate metrics
accuracy = (feedback["correct"] == True).mean()
override_rate = 1 - accuracy

print(f"Accuracy: {accuracy:.2%}")
print(f"Override Rate: {override_rate:.2%}")
```

---

## Escalation Categories

Current system handles general ticket triage. Future enhancements can add escalation logic for:

- **VIP Customers:** Route to premium support tier
- **Cancellation Intent:** Escalate to retention team
- **Complaint Escalations:** Flag for manager review
- **Jurisdictional Issues:** Route to regional compliance
- **Legal/Refund Requests:** Escalate to legal team

---

## Common Issues & Troubleshooting

| Issue | Solution |
|-------|----------|
| `GEMINI_API_KEY not found` | Ensure `.env` file exists with valid key |
| `ModuleNotFoundError: No module named 'faker'` | Run `pip install faker` |
| `Streamlit port 8501 already in use` | Run `streamlit run --server.port=8502 streamlit_feedback.py` |
| Empty `feedback.csv` | Ensure streamlit app received submissions (check console) |
| `triage_results.csv` not created | Check Gemini API quota and network connectivity |

---

## Future Enhancements

1. **Batch Processing:** Process large ticket volumes in parallel
2. **Confidence Scoring:** Add model confidence percentages to predictions
3. **Causal Loop Diagram:** Visualize feedback → retraining → accuracy improvement cycle
4. **Database Integration:** Replace CSV with PostgreSQL for scalability
5. **A/B Testing:** Compare multiple triage strategies
6. **Fine-tuning:** Use collected feedback to fine-tune Gemini prompts
7. **Analytics Dashboard:** Real-time metrics on model performance

---

## License

MIT License - See LICENSE file for details

---

## Support

For issues or questions, contact: support@example.com

---

**Last Updated:** June 2, 2026
