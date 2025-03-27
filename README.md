# AgentArenaModular
This is the first prototype for an "end-to-end" cycle of agent arena.

This includes: (1) data curation, (2) hacky API to call data, (3) fully independent "agent" doing the job, (4) "submitting" the job, and (5) grading via LLM.  This demo is meant to show the full flow of Agent Arena, and should not be taken as any work actually done on the implementation of Agent Arena.  To be clear: THIS DEMO IS ONLY MEANT TO BE A COMMUNICATION TOOL.

## Setup Instructions

### Prerequisites
- Python 3.12.9
- pip (Python package installer)

### Virtual Environment Setup

1. Create a virtual environment:
```bash
python3.12 -m venv venv
```

2. Activate the virtual environment:
- On macOS/Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
.\venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. To deactivate the virtual environment when you're done:
```bash
deactivate
```

Note: Make sure to activate the virtual environment before running any Python scripts or notebooks in this project.

### Data and Output
Create directories data and output.  Move `df_randomized.csv` into data as that is a requirement of everything else.

