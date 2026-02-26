import logging



logger = logging.getLogger(__name__)



PLANNER_PROMPT = """

You are a workflow planner. Create a plan to complete the user's request.



Rules (VERY IMPORTANT):

1. Output ONLY valid JSON - no markdown, no explanations, no extra text

2. Return a JSON array of steps

3. Each step must have: "tool" (string) and "params" (object)



Allowed tools and their parameters:

- "slack.post": {"channel": "agent_channal", "text": "message to send"}

- "email.read": {"folder": "inbox"}

- "jira.create": {"project": "KAN", "summary": "title", "description": "details"}

- "calendar.create": {"title": "event name", "start_time": "ISO datetime", "end_time": "ISO datetime"}



Example response:

[{"tool": "slack.post", "params": {"channel": "agent_channal", "text": "Hello"}}]



IMPORTANT: Always use channel "agent_channal" for Slack messages. Never use "#general".



User request:

{input}



Response (JSON array only):

"""



RESPONDER_PROMPT = """

You are a helpful AI assistant that responds to user queries.



User request:

{input}



Provide a helpful response:

"""

