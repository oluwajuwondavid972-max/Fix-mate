Fix-Mate 🔧
Fix what you safely can. Connect you to someone when you can't.

Fix-Mate is an AI-powered troubleshooting platform designed to help people diagnose problems with everyday devices and appliances.

The goal is to provide users with a conversational troubleshooting assistant that can understand a problem, ask relevant questions, identify likely causes, determine whether a repair is safe to attempt, and connect the user to a technician when professional assistance is required.

The current MVP demonstrates this workflow using a standing fan that does not turn on, while the architecture is designed to support multiple devices and appliance types.

Project Overview
When a device stops working, users often face two problems:

They don't know what is wrong.

They don't know whether they can safely fix it themselves.

Fix-Mate addresses both problems by combining conversational AI with a structured diagnostic system.

Instead of simply giving the user a list of possible causes, Fix-Mate follows a diagnostic workflow:

User describes problem
        ↓
Identify device and problem
        ↓
Perform safety check
        ↓
Ask diagnostic questions
        ↓
Collect evidence
        ↓
Determine likely cause
        ↓
Estimate confidence
        ↓
Determine repairability
        ↓
      ┌───────────────┐
      │               │
   Safe DIY       Technician
      │               │
      └───────┬───────┘
              ↓
          Verification
              ↓
       Solved / Continue
System Architecture
Fix-Mate uses a layered architecture:

                         USER
                           │
                           ▼
                    FRONTEND / CHAT
                           │
                           ▼
                      FASTAPI API
                           │
                           ▼
                    SAFETY ENGINE
                           │
                           ▼
                    AI / LLM LAYER
                           │
                           ▼
                 SYMPTOM EXTRACTION
                           │
                           ▼
                 DIAGNOSTIC ENGINE
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
              KNOWLEDGE BASE    RULES
                    │             │
                    └──────┬──────┘
                           ▼
                      CONFIDENCE
                           │
                           ▼
                     REPAIRABILITY
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
             SAFE DIY          TECHNICIAN
                 │                   │
                 └─────────┬─────────┘
                           ▼
                       VERIFICATION
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
               SOLVED            RE-DIAGNOSE
The important design principle is that the LLM is not the entire diagnostic engine.

The AI layer is responsible for understanding and communicating natural language, while structured components control diagnostic logic, safety, and the troubleshooting workflow.

Architecture Components
1. Frontend
The frontend is the user-facing chat interface.

Its responsibilities include:

Displaying the conversation.

Sending user messages to the backend.

Displaying diagnostic questions.

Displaying troubleshooting instructions.

Displaying diagnosis results.

Displaying technician recommendations when required.

The frontend communicates with the FastAPI backend through the API.

2. FastAPI API
FastAPI acts as the main backend interface between the frontend and the Fix-Mate system.

The main endpoint is:

POST /api/chat
The endpoint receives a user's message and returns information such as:

Assistant response.

Diagnostic state.

Identified device.

Identified problem.

Likely cause.

Confidence level.

Current action.

Session ID.

Example request:

{
    "message": "My standing fan is not working",
    "session_id": "string"
}
The backend then processes the message through the diagnostic workflow.

3. Safety Engine
Safety is one of the first layers in the system.

The safety engine checks user messages for potentially dangerous situations before allowing normal troubleshooting to continue.

Examples of safety indicators include:

Sparks

Smoke

Burning smell

Electric shock

Exposed wires

Damaged cables

Burnt plugs

Burnt sockets

Melting

Severe overheating

Example:

User:
"My fan isn't working and there are sparks."

                ↓

Safety Engine

                ↓

Potential danger detected

                ↓

STOP
The system responds with a safety warning and recommends professional inspection instead of continuing with DIY troubleshooting.

4. AI / LLM Layer
The AI layer is responsible primarily for understanding and communicating natural language.

Potential responsibilities include:

Understanding user descriptions.

Extracting symptoms.

Identifying device types.

Normalizing user responses.

Generating natural conversational responses.

Explaining diagnostic results.

For example:

"The fan is completely dead when I switch it on."
can be interpreted as:

Device: standing_fan

Problem:
fan_not_turning_on
The structured diagnostic engine can then take over the diagnostic process.

This separation prevents the LLM from being solely responsible for deciding the diagnostic path.

5. Answer Normalizer
Users should not have to answer diagnostic questions using exact keywords.

For example, the diagnostic engine may expect:

yes_fan_works
A user could instead say:

"Yeah, I tried another socket and the fan works there."
The answer normalizer converts natural-language responses into the structured values expected by the diagnostic engine.

User response
      │
      ▼
Answer Normalizer
      │
      ▼
Structured answer
      │
      ▼
Diagnostic Engine
Example:

"Yes, I tried another socket and the fan works there."
                         ↓
                  "yes_fan_works"
This allows the diagnostic engine to remain predictable while the user experience remains conversational.

6. Diagnostic Engine
The diagnostic engine controls the actual troubleshooting workflow.

It determines:

Which question should be asked next.

How an answer affects the diagnosis.

Which cause is supported by the evidence.

Whether the system should continue diagnosing.

Whether the problem should be escalated.

Whether a possible solution has been identified.

The diagnostic logic is stored separately from the API layer.

This makes the diagnostic engine reusable across different devices.

7. Knowledge Base
Device-specific diagnostic information is stored in the knowledge base.

Current location:

backend/
└── knowledge/
    └── diagnostics.json
The knowledge base contains information such as:

Device
   ↓
Problem
   ↓
Safety Check
   ↓
Diagnostic Steps
   ↓
Possible Answers
   ↓
Possible Causes
   ↓
Confidence
   ↓
Action
For example:

Standing Fan
     │
     └── Fan does not turn on
             │
             ├── Safety check
             ├── Check power source
             ├── Try another socket
             ├── Check plug/cable
             ├── Check fan response
             ├── Check speed settings
             └── Internal fault
The same diagnostic engine can therefore work with different device knowledge.

8. Confidence
Fix-Mate should not treat every diagnosis as equally certain.

A diagnosis can have different confidence levels:

HIGH
MODERATE
LOW
For example:

Fan does not work in Socket A
        +
Fan works in Socket B
        ↓
Original socket is likely the problem
        ↓
Confidence: HIGH
Whereas:

Socket has power
        +
Cable looks fine
        +
Fan still does not respond
        ↓
Possible internal fault
        ↓
Confidence: LOW
Confidence helps the system determine how strongly it should present a diagnosis and whether escalation may be appropriate.

9. Repairability
Diagnosis alone is not enough.

Fix-Mate must also determine whether the problem is safe for the user to address.

The system should distinguish between:

Diagnosed + Safe
        ↓
Possible DIY guidance
and:

Diagnosed + Unsafe/Complex
        ↓
Technician referral
Examples of situations that may require escalation include:

Internal electrical faults.

Exposed electrical wiring.

Damaged power cables.

Components requiring the appliance to be opened.

Problems requiring electrical measurements.

Dangerous or uncertain conditions.

The system should prioritize user safety over attempting to complete a repair.

10. Diagnostic Sessions
Fix-Mate maintains a diagnostic session for each troubleshooting conversation.

A session stores information such as:

Session
│
├── Device
├── Problem
├── Safety state
├── Current diagnostic step
├── Verification state
└── Pending diagnostic result
The session ID allows the backend to know which diagnostic conversation a user's response belongs to.

Example:

User message
     +
Session ID
     ↓
Existing diagnostic session
     ↓
Current diagnostic step
     ↓
Process answer
     ↓
Next diagnostic step
End-to-End Workflow
Consider the following example.

Step 1 — User Reports a Problem
The user says:

"My standing fan is not working."
Fix-Mate identifies:

Device:
Standing Fan

Problem:
Fan does not turn on
A diagnostic session is created.

Step 2 — Safety Check
Fix-Mate asks:

"Before we continue, do you notice any sparks,
smoke, burning smell, electric shock, exposed
or damaged wires, or a melted/burnt plug or socket?"
If the user answers:

"No, everything looks fine."
the system continues.

If the user reports a dangerous condition:

"There are sparks."
the safety engine stops the diagnostic process.

Step 3 — Check the Power Source
Fix-Mate asks:

"Does the socket you're using currently provide
power to another appliance?"
Suppose the user responds:

"No, there is no power in the socket."
The diagnostic engine determines that the next step should be testing another socket.

Step 4 — Test Another Socket
Fix-Mate asks:

"Can you try the fan in another socket that
you know is working?"
The user responds:

"Yes, I tried another socket and the fan works there."
The answer normalizer converts this into:

yes_fan_works
The diagnostic engine determines:

Likely Cause:
Original socket problem

Confidence:
High
Step 5 — Verification
Fix-Mate does not immediately declare success.

Instead, it asks:

"Does the fan work normally now?"
The user confirms:

"Yes, it works normally now."
The system then returns:

Status:
SOLVED
If the user instead says:

"No, it still doesn't work."
the system continues the diagnostic process rather than incorrectly declaring the problem solved.

Technician Escalation Workflow
If the diagnostic process determines that the problem is unsafe or requires professional intervention:

User
  ↓
Safety / Diagnosis
  ↓
Complex or unsafe problem
  ↓
Technician Referral
For example:

Fan has power
      +
Plug and cable appear fine
      +
Fan still does not respond
      ↓
Possible internal electrical fault
      ↓
Technician referral
The long-term platform will allow users to find and connect with suitable technicians.

Project Structure
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
│   │   ├── response_generator.py
│   │   └── answer_normalizer.py
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
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
Design Philosophy
1. Safety Before Diagnosis
Safety
  ↓
Diagnosis
The system should not continue with potentially dangerous troubleshooting.

2. Evidence Before Conclusion
The system should gather information before deciding on a cause.

Symptoms
   ↓
Evidence
   ↓
Diagnosis
3. Structured Logic Behind Conversational AI
The user should experience a natural conversation, but the underlying diagnostic process should remain structured and predictable.

Natural Language
      ↓
AI Understanding
      ↓
Structured Data
      ↓
Diagnostic Engine
4. Verify the Solution
A diagnosis should not automatically be considered successful.

Possible Solution
      ↓
User Verification
      ↓
Solved / Continue
5. Escalate When Necessary
When the system cannot safely solve the problem, the correct action is not to guess.

Unsafe / Complex / Uncertain
            ↓
       Technician
Future Device Support
Although the current MVP demonstrates a standing fan, the architecture is intended to support additional device categories.

Potential device categories include:

Phones

Standing fans

Electric kettles

Refrigerators

Dishwashers

Laptops

Generators

Each device can have its own diagnostic knowledge while sharing the same underlying diagnostic architecture.

                    DIAGNOSTIC ENGINE
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   Standing Fan        Refrigerator        Laptop
   Knowledge           Knowledge           Knowledge
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                        Fix-Mate
Summary
Fix-Mate combines conversational AI with structured troubleshooting logic to create an intelligent diagnostic assistant.

The system separates:

AI
│
├── Understand language
├── Extract symptoms
└── Communicate naturally

Diagnostic Engine
│
├── Control diagnostic flow
├── Evaluate evidence
└── Determine next step

Safety Engine
│
└── Prevent unsafe troubleshooting

Knowledge Base
│
└── Store device-specific diagnostic knowledge

Repairability
│
└── Determine DIY vs technician

Verification
│
└── Confirm whether the problem was actually solved
The ultimate goal is to build a platform where users can describe a problem naturally, receive safe and intelligent troubleshooting guidance, and seamlessly connect with a technician when the problem is beyond safe DIY repair.

Fix what you safely can. Connect you to someone when you can't.
