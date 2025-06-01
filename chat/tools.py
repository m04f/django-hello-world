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
    'type': 'function',
    'function': {
        'name': 'create_workout',
        'description': 'Create a workout with specified exercises',
        'parameters': {
            'type': 'object',
            'required': ['name', 'description', 'exercises'],
            'properties': {
                'name': {'type': 'string', 'description': 'The name of the workout'},
                'description': {'type': 'string', 'description': 'A description of the workout'},
                'exercises': {
                    'type': 'array',
                    'description': 'A list of exercise names with details',
                    'items': {
                        'type': 'object',
                        'required': ['exercise_id', 'order'],
                        'properties': {
                            'exercise': {'type': 'string', 'description': 'Exercise name'},
                            'reps': {'type': 'integer', 'description': 'The number of repetitions', 'nullable': True},
                            'duration': {'type': 'integer', 'description': 'The duration in seconds', 'nullable': True},
                            'weight': {'type': 'integer', 'description': 'The weight in kilograms', 'nullable': True},
                            'sets': {'type': 'integer', 'description': 'The number of sets', 'default': 1},
                            'rest': {'type': 'integer', 'description': 'The rest time in seconds', 'default': 120},
                            'notes': {'type': 'string', 'description': 'Additional notes', 'nullable': True},
                        }
                    }
                }
            }
        }
    }
}

availableTools = [
    create_workout_tool
]
