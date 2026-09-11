--This is a simple architecture of how i want to build this project, doesn't replace the main architecture,it is just a simple put together raw idea

                         ┌──────────────────┐
                         │       USER       │
                         │                  │
                         │ "Fan is humming  │
                         │ but not spinning"│
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    FRONTEND      │
                         │                  │
                         │ Chat Interface   │
                         └────────┬─────────┘
                                  │ HTTP/API
                                  ▼
                  ┌────────────────────────────┐
                  │       FASTAPI BACKEND      │
                  │                            │
                  │  Chat / Session Manager    │
                  └─────────────┬──────────────┘
                                │
                ┌───────────────┼────────────────┐
                ▼               ▼                ▼
       ┌────────────────┐ ┌──────────────┐ ┌──────────────┐
       │ SAFETY ENGINE  │ │     LLM      │ │ DIAGNOSTIC   │
       │                │ │              │ │    ENGINE    │
       │ danger rules   │ │ understands  │ │              │
       │ stop rules     │ │ user message │ │ symptoms     │
       └───────┬────────┘ │ asks naturally│ │ causes       │
               │          └──────┬───────┘ │ questions    │
               │                 │         └──────┬───────┘
               │                 │                │
               └─────────────────┼────────────────┘
                                 ▼
                       ┌──────────────────┐
                       │   KNOWLEDGE DB   │
                       │                  │
                       │ Devices          │
                       │ Symptoms         │
                       │ Causes           │
                       │ Questions        │
                       │ Safe actions     │
                       └──────────────────┘