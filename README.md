# 🤖 AIONOS AI Support Agent

An agentic AI-powered IT support system designed to help employees
resolve common technical issues and automatically escalate unresolved
problems by creating IT support tickets.

## 🎯 Problem Statement

Employees frequently face IT problems such as:

- VPN connectivity issues
- Wi-Fi/network problems
- Laptop performance issues
- Software-related problems

Traditional IT support requires employees to manually contact the
support team and wait for assistance.

The AIONOS AI Support Agent provides an automated first level of
support and escalates unresolved issues automatically.

---

## 💡 Solution

The system combines an AI support agent, a knowledge base, and an
automated ticketing system.

The agent:

1. Understands the employee's IT problem.
2. Searches the internal knowledge base.
3. Provides relevant troubleshooting steps.
4. Determines whether the issue remains unresolved.
5. Automatically creates an IT support ticket when escalation is
   required.
6. Stores the ticket in a SQLite database.
7. Displays tickets through an IT support dashboard.

---

## 🧠 Agentic Workflow

```text
Employee
   ↓
AIONOS AI Support Agent
   ↓
Understand Issue
   ↓
Search Knowledge Base
   ↓
Analyze Troubleshooting Steps
   ↓
Issue Resolved?
   ├── YES → Provide Solution
   │
   └── NO
        ↓
   Create IT Ticket
        ↓
   SQLite Database
        ↓
   Ticket Dashboard

   ## How to Test the Live Demo

### Scenario 1: IT Troubleshooting

Enter an issue such as:

> My VPN is not working

The AI Support Agent analyzes the issue, searches the internal AIONOS knowledge base, and provides relevant troubleshooting steps.

### Scenario 2: Automatic Ticket Escalation

After receiving the troubleshooting steps, enter:

> I tried all these troubleshooting steps and my VPN is still not working.

The AI Agent detects that the issue remains unresolved and automatically creates an IT support ticket.

The response will display:

- Ticket ID
- Priority
- Status

### Scenario 3: View Support Tickets

Click **View Support Tickets** on the homepage.

The ticket dashboard displays:

- Ticket ID
- Issue
- Priority
- Status
- Creation time

### Example Workflow

Employee Issue  
↓  
AI understands the issue  
↓  
Knowledge Base Search  
↓  
AI troubleshooting  
↓  
Issue resolved → End  
↓  
Issue still unresolved → Create IT Ticket  
↓  
Ticket appears in Support Dashboard