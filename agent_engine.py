import requests
from database import get_connection

def ask_ai(user_id: int, message: str):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT memory_text FROM memory WHERE agent_id=%s ORDER BY id DESC LIMIT 5",
            (user_id,)
        )

        memory_rows = cursor.fetchall()
        memory = "\n".join([m[0] for m in memory_rows]) or "No memory"

        prompt = f"""
You are an AI assistant.

Memory:
{memory}

User: {message}
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()
        return data.get("response", "No response")

    except Exception as e:
        return f"AI Error: {str(e)}"

    finally:
        conn.close()