import time
from database import get_connection
from agent_engine import ask_ai


def run_worker(agent_id: int):
    print(f"Worker running for agent {agent_id}")

    while True:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, task 
            FROM tasks 
            WHERE agent_id=%s AND status='pending'
        """, (agent_id,))

        tasks = cursor.fetchall()

        for task_id, task in tasks:
            try:
                cursor.execute("UPDATE tasks SET status='running' WHERE id=%s", (task_id,))
                conn.commit()

                result = ask_ai(agent_id, f"Execute task: {task}")

                cursor.execute("""
                    INSERT INTO conversations (agent_id, user_message, ai_response)
                    VALUES (%s, %s, %s)
                """, (agent_id, task, result))

                cursor.execute("UPDATE tasks SET status='done' WHERE id=%s", (task_id,))
                conn.commit()

            except Exception as e:
                cursor.execute("UPDATE tasks SET status='failed' WHERE id=%s", (task_id,))
                conn.commit()

                print("Error:", e)

        conn.close()
        time.sleep(5)


if __name__ == "__main__":
    run_worker(1)