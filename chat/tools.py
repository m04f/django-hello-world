from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
import json

from rest_framework.reverse import reverse

from workout.models import Workout, WorkoutExercise
from workout.serializers import WorkoutSerializer


async def create_workout(data: dict) -> str:
    serializer = WorkoutSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return 'Workout created: ' + serializer.url


async def call_tool(tool: ChatCompletionMessageToolCall):
    """
    Helper function to call a tool with the provided arguments.

    Args:
        tool (dict): The tool definition containing function metadata.

    Returns:
        dict: The result of the tool's function execution.
    """
    if tool.function.name == 'create_workout':
        args = json.loads(tool.function.arguments)
        return await create_workout(args)


create_workout_tool = {
    "type": "function",
    "function": {
        "name": "create_workout",
        "description": "Create a new workout with exercises",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the workout"
                },
                "description": {
                    "type": "string",
                    "description": "Description of the workout"
                },
                "exercises": {
                    "type": "array",
                    "description": "List of exercises in the workout",
                    "items": {
                        "type": "object",
                        "properties": {
                            "exercise": {
                                "type": "string",
                                "description": "Name of the exercise"
                            },
                            "reps": {
                                "type": "integer",
                                "description": "Number of repetitions (required if duration not provided)"
                            },
                            "duration": {
                                "type": "integer",
                                "description": "Duration in seconds (required if reps not provided)"
                            },
                            "sets": {
                                "type": "integer",
                                "description": "Number of sets",
                                "default": 1
                            },
                            "weight": {
                                "type": "integer",
                                "description": "Weight in appropriate units"
                            },
                            "rest": {
                                "type": "integer",
                                "description": "Rest time between sets in seconds",
                                "default": 120
                            }
                        },
                        "required": ["exercise"]
                    }
                },
                "notes": {
                    "type": "string",
                    "description": "Additional notes for the workout"
                },
                "public": {
                    "type": "boolean",
                    "description": "Whether the workout is public",
                    "default": True
                }
            },
            "required": ["name", "exercises"]
        }
    }
}

availableTools = [
    create_workout_tool
]
