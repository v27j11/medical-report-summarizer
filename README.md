<<<<<<< HEAD
# Medical Report Summarization using Mistral SDK

This project extracts and summarizes information from scanned PET/CT reports using Mistral's OCR and chat APIs.

## Features

- ✅ Extracts text using OCR from scanned medical PDF reports.
- 🧠 Summarizes and extracts structured information like:
  - Patient Name
  - Age
  - Sex
  - Medical Summary
- 📝 Saves structured data as JSON.

## Project Structure

```
Medical reports Summarization/
│
├── Medical_reports.py         # Main script
├── pet_ct_2.pdf               # Sample input PDF
├── pet_ct_2_structured.json   # Output structured summary
├── README.md                  # This file
└── requirements.txt           # Dependencies
```

## Setup Instructions

1. **Clone this private repository**:
```bash
git clone https://github.com/yourusername/your-private-repo.git
cd your-private-repo
```

2. **Create and activate a virtual environment** (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Add your Mistral API key** to a `.env` file:
```
MISTRAL_API_KEY=your_actual_key_here
```

5. **Run the script**:
```bash
python Medical_reports.py
```

## Notes

- Requires Python 3.10 or newer.
- Make sure your `.env` is included in `.gitignore`.

---

© 2025 Medical AI Research | Private and Confidential
=======
# medical-report-summarizer
Medical report OCR + summarizer using Mistral SDK
>>>>>>> c12abca03e012f21b9096d89e855dcafb2d8f60f
