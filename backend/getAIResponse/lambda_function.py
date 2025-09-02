import json
import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    origin = event.get("headers", {}).get("origin", "")

    try:
        chatHistory = json.loads(event["body"])
        print(chatHistory)
        
    except (KeyError, json.JSONDecodeError):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid or missing JSON body"})
        }
    
    messages=[
        {
            "role": "system",
            "content": "You are a fitness assitant helping a user to build a workout programme who wants to gain muscle. "
                      "You are the final step for collecting information regarding the user's preferences and "
                      "requirements before generating the fitness programme. Your task is to ask questions one at a time "
                      "(and answer if necessary) in order to find out the following information: "
                      "1. Any muscle groups the user wants to exclude in their workout programme. "
                      "2. Any muscle groups that the user particularly wants to work on. "
                      "Once you have both of the above, confirm with the user that you are "
                      "ready to generate the programme and instruct them to press the 'Build Programme' button below."
                      "Here is some supplementary context for the fitness programme generator app you are part of just "
                      "in case the user asks some questions."
                      "The user has already entered some basic preferences like available days, "
                      "time per session, the equipment they have access to, etc. "
                      "So, this chat-based form will gather all of the user's preferences before generating "
                      "the programme. You do not have access to the user's other preferences as this is not necessary for your task. "
                      "And, after generation, the user will have the option to replace any exercises they wish. "
                      "If the user has any queries that you feel are unequipped to answer, then instruct them to go to the 'Contact' page "
                      "and send a query by email. "
                      "Keep your tone motivating, positive, and approachable but not too informal (no emojis). "
                      "And keep replies fairly brief where possible."
        }
    ] + chatHistory

    completion = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=messages,
        temperature=1
    )

    return {
        "statusCode": 200,
        "headers": { 
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "reply": completion.choices[0].message.content
        })
    }
