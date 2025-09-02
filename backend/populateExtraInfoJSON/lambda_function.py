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
        context = json.loads(event["body"])
        
    except (KeyError, json.JSONDecodeError):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid or missing JSON body"})
        }
    
    # All of the values below are values in the database apart from 'back' which is separated into 'middle back', 'lats'
    # and 'shoulders' which is separated into 'front delt', 'lateral delt', 'rear delt'
    possible_muscle_groups = ["abdominals", "abductors", "adductors", "biceps", "back", "calves", "chest", "forearms", "glutes", "hamstrings", "quadriceps", "shoulders", "traps", "triceps"]

    example_json = {
        "excludedMuscleGroups": [],
        "preferredMuscleGroups": []
    }
    
    messages=[
        {
            "role": "system",
            "content":
                "Your job is to complete a JSON file that summarises some of the user's preferences "
                "for their fitness programme. "
                "From the following chat history, extract a list for each of the following categories: "
                "1. excludedMuscleGroups: muscle groups the user wants to avoid working. "
                "2. preferredMuscleGroups: muscle groups the user wants to focus on. "
                "The ONLY allowed values are the following: "
                + ", ".join(possible_muscle_groups) + ". "
                "If the user has no preferences for a category, or does not mention anything for a category, "
                "use an empty array for that category. "
                "Use only the information EXPLICITLY stated in the chat history. Do not guess or add extra information. "
                "If the user mentions a broader term, you may infer the appropriate muscle group(s) "
                "from the list above. For example: "
                "'legs' → ['quadriceps', 'hamstrings', 'calves'], "
                "'arms' → ['biceps', 'triceps']. "
                "Do not add any fields other than 'excludedMuscleGroups' and 'preferredMuscleGroups'. "
                "Return ONLY a valid JSON object in this exact format: "
                + json.dumps(example_json, indent=2) + "\n\n"
                "Here is the chat history to analyse:\n"
                + json.dumps(context, indent=2)
        }

    ] 

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.2
    )

    json_response = json.loads(completion.choices[0].message.content)

    return {
        "statusCode": 200,
        "headers": { 
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Content-Type": "application/json"
        },
        "body": json.dumps(json_response)
    }