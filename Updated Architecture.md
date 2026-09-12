                         FIX-MATE
                            │
                            ▼
                         USER
                            │
                            ▼
                    ┌───────────────┐
                    │  CHAT FRONTEND │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    FASTAPI    │
                    │    BACKEND   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ SAFETY ENGINE │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  AI / LLM     │
                    │    LAYER      │
                    └───────┬───────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ SYMPTOM EXTRACTION  │
                 │    & NORMALIZATION  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ DIAGNOSTIC ENGINE   │
                 └──────────┬──────────┘
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
        ┌────────────────┐    ┌─────────────────┐
        │ KNOWLEDGE BASE │    │ DIAGNOSTIC RULES│
        └───────┬────────┘    └────────┬────────┘
                └──────────┬───────────┘
                           ▼
                  ┌─────────────────┐
                  │    CONFIDENCE   │
                  │     ENGINE      │
                  └────────┬────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ REPAIRABILITY      │
                 │      ENGINE        │
                 └─────────┬──────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       SAFE DIY REPAIR            TECHNICIAN
              │                    REFERRAL
              ▼
       VERIFY THE FIX
              │
        ┌─────┴─────┐
        ▼           ▼
      FIXED       NOT FIXED
        │           │
        ▼           ▼
      SOLVED     RE-DIAGNOSE