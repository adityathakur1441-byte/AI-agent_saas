from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from database import get_connection
from agent_engine import ask_ai

# ==================================================
# APP
# ==================================================

app = FastAPI(
    title="AI Agent SaaS Platform",
    version="1.0.0"
)

# ==================================================
# JWT CONFIG
# ==================================================

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================================
# FRONTEND
# ==================================================

app.mount(
    "/ui",
    StaticFiles(directory="frontend", html=True),
    name="ui"
)

# ==================================================
# MODELS
# ==================================================

class ChatRequest(BaseModel):
    user_id: int
    message: str


class AgentRequest(BaseModel):
    name: str
    role: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class OrderRequest(BaseModel):
    order_id: str

# ==================================================
# ROOT
# ==================================================

@app.get("/")
def home():
    return {
        "success": True,
        "message": "AI Agent SaaS Platform Running 🚀"
    }

# ==================================================
# REGISTER
# ==================================================

@app.post("/register")
def register(user: RegisterRequest):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM users WHERE email=%s",
            (user.email,)
        )

        if cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        hashed_password = pwd_context.hash(user.password)

        cursor.execute(
            """
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
            """,
            (user.username, user.email, hashed_password)
        )

        conn.commit()

        return {
            "success": True,
            "message": "User registered successfully"
        }

    finally:
        conn.close()

# ==================================================
# LOGIN
# ==================================================

@app.post("/login")
def login(user: LoginRequest):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, password FROM users WHERE email=%s",
            (user.email,)
        )

        db_user = cursor.fetchone()

        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid email")

        user_id = db_user[0]
        hashed_password = db_user[1]

        if not pwd_context.verify(user.password, hashed_password):
            raise HTTPException(status_code=401, detail="Invalid password")

        token = jwt.encode(
            {
                "user_id": user_id,
                "exp": datetime.utcnow() + timedelta(days=1)
            },
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {
            "success": True,
            "token": token,
            "user_id": user_id
        }

    finally:
        conn.close()

# ==================================================
# AGENTS
# ==================================================

@app.get("/agents")
def get_agents():

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, name, role FROM agents")
        rows = cursor.fetchall()

        return {
            "success": True,
            "agents": [
                {"id": r[0], "name": r[1], "role": r[2]}
                for r in rows
            ]
        }

    finally:
        conn.close()


@app.post("/agents")
def create_agent(agent: AgentRequest):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO agents (name, role) VALUES (%s, %s)",
            (agent.name, agent.role)
        )
        conn.commit()

        return {
            "success": True,
            "message": "Agent created"
        }

    finally:
        conn.close()

# ==================================================
# CHAT
# ==================================================

@app.post("/chat")
def chat(req: ChatRequest):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM agents WHERE id=%s",
            (req.user_id,)
        )

        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Agent not found")

        response = ask_ai(req.user_id, req.message)

        return {
            "success": True,
            "response": response
        }

    finally:
        conn.close()

# ==================================================
# ORDER TRACKING (FIXED - IMPORTANT)
# ==================================================

@app.post("/track-order")
def track_order(req: OrderRequest):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT order_id, status FROM orders WHERE order_id=%s",
            (req.order_id,)
        )

        order = cursor.fetchone()

        if not order:
            return {
                "success": False,
                "response": "Order not found"
            }

        return {
            "success": True,
            "response": f"Order {order[0]} is {order[1]}"
        }

    finally:
        conn.close()