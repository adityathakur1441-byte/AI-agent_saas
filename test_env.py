from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r"C:\Ai agent\chatbot\.env")

print(os.getenv("DB_USER"))
print(os.getenv("DB_PASSWORD"))
print(os.getenv("DB_NAME"))