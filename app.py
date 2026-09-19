import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

from rag import search_knowledge_base
from database import create_ticket, get_all_tickets


load_dotenv()

app = Flask(__name__)


# Gemini AI client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "response": "Please describe your IT problem."
        })

    # Search the AIONOS internal knowledge base
    knowledge = search_knowledge_base(message)

    prompt = f"""
You are the AIONOS AI IT Support Agent.

Help employees solve IT problems.

Use the following internal knowledge base:

{knowledge}

USER ISSUE:
{message}

Instructions:

1. Understand the employee's issue.
2. Use the knowledge base to provide relevant troubleshooting.
3. Give clear, practical steps.
4. If the employee clearly says they already tried
   the troubleshooting steps and the issue is still
   unresolved, escalate the issue.
5. If escalation is required, begin your response with:

CREATE_TICKET

6. Otherwise begin your response with:

NO_TICKET

Do not create a ticket unless the issue is clearly unresolved.
"""

    try:

        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        ai_response = response.output_text.strip()

        print("Gemini response:", ai_response)


        # ==========================================
        # AGENT DECISION: CREATE TICKET
        # ==========================================

        if ai_response.startswith("CREATE_TICKET"):

            ticket_id = create_ticket(
                issue=message,
                priority="Medium"
            )

            return jsonify({
                "response": f"""
<h3>🎫 IT Support Ticket Created</h3>

<p>
The AIONOS AI Support Agent determined that the
recommended troubleshooting steps have already been attempted.
</p>

<p><strong>Ticket ID:</strong> {ticket_id}</p>

<p><strong>Priority:</strong> Medium</p>

<p><strong>Status:</strong> Open</p>

<p>
Our IT support team can investigate the issue further.
</p>
"""
            })


        # ==========================================
        # NORMAL AI RESPONSE
        # ==========================================

        if ai_response.startswith("NO_TICKET"):

            ai_response = ai_response.replace(
                "NO_TICKET",
                "",
                1
            ).strip()

        return jsonify({
            "response": ai_response
        })


    except Exception as error:

        print("Gemini Error:", error)

        # Fallback response
        return jsonify({
            "response": f"""
<h3>🤖 AIONOS AI Support Agent</h3>

<p>
The AI service is temporarily unavailable, but I found
relevant information in the AIONOS knowledge base.
</p>

<div>
{knowledge}
</div>

<p>
<strong>Next step:</strong> Try these troubleshooting steps.
If the problem continues, tell me that the issue is still
not resolved and I can create an IT support ticket.
</p>
"""
        })


@app.route("/tickets")
def tickets():

    all_tickets = get_all_tickets()

    return render_template(
        "tickets.html",
        tickets=all_tickets
    )


if __name__ == "__main__":
    app.run(debug=True)