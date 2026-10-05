# Fix-Mate 🔧

> **Fix what you safely can. Connect you to someone when you can't.**

Fix-Mate is an AI-powered troubleshooting platform designed to help people diagnose problems with everyday devices and appliances.

The goal is to provide users with a conversational troubleshooting assistant that can understand a problem, ask relevant questions, identify likely causes, determine whether a repair is safe to attempt, and connect the user to a technician when professional assistance is required.

---

# Project Overview

When a device stops working, users often face two problems:

1. They don't know what is wrong.
2. They don't know whether they can safely fix it themselves.

Fix-Mate addresses both problems by combining conversational AI with a structured diagnostic system.

Instead of simply giving the user a list of possible causes, Fix-Mate follows a diagnostic workflow:

```text
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

       Core Objectives
Fix-Mate is designed to:

Understand natural-language descriptions of problems.

Identify the device involved.

Identify the user's main problem or symptom.

Ask targeted diagnostic questions.

Perform safety checks before troubleshooting.

Track diagnostic evidence.

Determine likely causes.

Assign a confidence level to the diagnosis.

Determine whether a repair is safe for the user.

Provide safe troubleshooting or repair guidance.

Escalate unsafe or complex problems to a technician.

Verify whether the proposed solution actually solved the problem.