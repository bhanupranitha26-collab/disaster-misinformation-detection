# AI-Based Fake Disaster News Filter  
## Real-Time Disaster Misinformation Detection

## Overview
When disasters such as floods, earthquakes, cyclones, fires, or industrial accidents occur, false information spreads rapidly on social media. Fake casualty counts, edited images, false evacuation orders, and misleading posts can create panic and put lives at risk.

This project is an AI-powered system designed to detect, flag, and reduce disaster-related misinformation in real time. It analyzes text and images, compares claims with trusted sources, and provides verified updates for the public and authorities.

---

## Problem Statement
Manual fact-checking is too slow during emergencies. By the time misinformation is corrected, it may already have spread widely.

This system helps solve:

- Rapid spread of false information during active disasters  
- Lack of trusted real-time information for the public  
- Difficulty for authorities to track fake narratives  
- Need for automated large-scale verification  
- Regional language misinformation going undetected  

---

## Key Features

### Text Misinformation Detection
- Detects fake or suspicious disaster-related text posts  
- NLP-based classification model  
- Instant credibility scoring  

### Image Verification
- Identifies misleading or suspicious disaster images  
- Supports image-based misinformation checks  

### Official Source Validation
- Cross-checks claims using trusted sources  
- Government and emergency information support  

### Public Dashboard
- Verified updates during emergencies  
- Evacuation routes  
- Shelter details  
- Emergency helplines  

### Authority Dashboard
- Monitor misinformation trends  
- Detect top false narratives  
- Improve response actions  

### Multi-Language Support
- Designed to support regional languages and dialects  

---

## Tech Stack

### Frontend
- React.js  
- HTML  
- CSS  
- JavaScript  

### Backend
- Python  
- FastAPI  

### Database
- SQLite  

### AI / ML
- Scikit-learn  
- NLP  
- Computer Vision  

---

## Project Structure

```text
disaster-misinformation-detection/
│
├── backend/
│   ├── main.py
│   ├── model.py
│   ├── image_model.py
│   ├── database.py
│   ├── official_sources.json
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── package-lock.json
│
├── README.md
└── .gitignore
