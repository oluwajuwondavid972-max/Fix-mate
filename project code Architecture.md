fix-mate/
│
├── backend/
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   ├── chat.py
│   │   └── diagnosis.py
│   │
│   ├── ai/
│   │   ├── llm.py
│   │   ├── symptom_extractor.py
│   │   └── response_generator.py
│   │
│   ├── diagnosis/
│   │   ├── engine.py
│   │   ├── confidence.py
│   │   └── repairability.py
│   │
│   ├── safety/
│   │   └── safety_engine.py
│   │
│   ├── knowledge/
│   │   └── diagnostics.json
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   └── services/
│       └── technician_service.py
│
├── frontend/
│
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md