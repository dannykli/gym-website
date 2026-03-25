import json

from get_extra_preferences import get_extra_preferences
from generate_programme import generate_programme

def lambda_handler(event, context):
    try:
        payload = json.loads(event["body"])
        user_preferences = payload["preferences"]
        chat_history = payload["chatHistory"]
        
    except (KeyError, json.JSONDecodeError):
        return {
            "statusCode": 400,
            "headers": { 
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Invalid or missing JSON body"})
        }
    
    try:
        extra_preferences = get_extra_preferences(chat_history)
    except Exception as e:
        print(f"Error fetching extra preferences from LLM: {str(e)}")
        print("Falling back to empty extra preferences.")
        extra_preferences = {
            "excludedMuscleGroups": [],
            "preferredMuscleGroups": []
        }

    preferences = user_preferences | extra_preferences
    
    result = generate_programme(preferences)

    return result