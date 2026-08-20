from openai import OpenAI # type: ignore
import json
import os

def generate_assignment_content(assignment_name, assignment_statement, code):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set the OPENAI_API_KEY environment variable before running this script.")

    client = OpenAI(api_key=api_key)
    prompt = f"""
You are helping prepare a college Design and Analysis of Algorithms
(DAA) practical assignment.

Generate content for the following assignment.

Assignment:
{assignment_name}

Assignment Statement:
{assignment_statement}

C++ Code:
{code}

Generate the following:

1. theory
2. analysis of time_complexity & space_complexity

Requirements:

- Keep the theory concise and suitable for a B.Tech CSE practical file.
- Explain the algorithm actually represented by the provided code.
- Give best-case, average-case, and worst-case time complexity where applicable.
- Give space complexity.
- Do NOT invent experimental timing results.
- Do NOT modify or rewrite the C++ code.
- Return ONLY valid JSON.

JSON format:

{{
    "theory": "...",
    "pseudocode": "...",
    "time_complexity": "...",
    "space_complexity": "...",
    "analysis": "..."
}}
"""
    chat_completion = client.chat.completions.create(
        messages = [
            {
                "role" : "user",
                "content": prompt
            }
        ],
        model = "gpt-3.5-turbo",
        response_format={"type": "json_object"}
    )
    response = chat_completion.choices[0].message.content
    if not response:
        raise RuntimeError("The model returned an empty response.")

    return json.loads(response)

if __name__ == "__main__":

    result = generate_assignment_content(
        "Linear Search",
        "Implement Linear Search on an array and analyze its performance.",
        """
        int linearSearch(int arr[], int n, int key)
        {
            for(int i = 0; i < n; i++)
            {
                if(arr[i] == key)
                    return i;
            }

            return -1;
        }
        """
    )

    print(json.dumps(result, indent=4))