import time
import traceback
from database import get_connection
from agent_engine import ask_ai


def run_worker(agent_id: int):
    print(f"🚀 Worker started for agent {agent_id}")

    while True:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, task FROM tasks WHERE agent_id=%s AND status='pending'",
            (agent_id,)
        )

        tasks = cursor.fetchall()

        if not tasks:
            conn.close()
            time.sleep(5)
            continue

        for task_id, task_text in tasks:

            try:
                print(f"⚙️ Running task {task_id}: {task_text}")

                result = ask_ai(agent_id, f"Execute this task: {task_text}")

                cursor.execute(
                    "INSERT INTO conversations (agent_id, user_message, ai_response) VALUES (%s, %s, %s)",
                    (agent_id, task_text, result)
                )

                cursor.execute(
                    "UPDATE tasks SET status='done' WHERE id=%s",
                    (task_id,)
                )

                conn.commit()

                print(f"✅ Task {task_id} done")

            except Exception:
                print("❌ ERROR OCCURRED")
                print(traceback.format_exc())

                cursor.execute(
                    "UPDATE tasks SET status='failed' WHERE id=%s",
                    (task_id,)
                )
                conn.commit()

        conn.close()
        time.sleep(5)


if __name__ == "__main__":
    run_worker(1)