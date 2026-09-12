                 USER MESSAGE
                      │
                      ▼
              ┌───────────────┐
              │      LLM      │
              └───────┬───────┘
                      │
                      ▼
             NORMALIZED SYMPTOM
                      │
                      ▼
             ┌────────────────┐
             │   DIAGNOSTIC   │
             │     ENGINE     │
             └───────┬────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       POSSIBLE   EVIDENCE   QUESTIONS
        CAUSES
          │          │          │
          └──────────┼──────────┘
                     ▼
               CAUSE SCORING
                     │
                     ▼
                CONFIDENCE
                     │
                     ▼
             REPAIRABILITY
                     │
              ┌──────┴──────┐
              ▼             ▼
          SAFE DIY      TECHNICIAN
              │
              ▼
          LLM EXPLAINS
          NEXT ACTION