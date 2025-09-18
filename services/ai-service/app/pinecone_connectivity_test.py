# Simple connectivity test for Pinecone DNS and HTTPS
import socket
import requests
import os
from dotenv import load_dotenv

load_dotenv()

pinecone_env = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
controller_host = f"controller.{pinecone_env}.pinecone.io"

print(f"Testing DNS for: {controller_host}")
try:
    ip = socket.gethostbyname(controller_host)
    print(f"DNS resolved: {controller_host} -> {ip}")
except Exception as e:
    print(f"DNS resolution failed: {e}")

print(f"Testing HTTPS connectivity to: https://{controller_host}/databases")
try:
    resp = requests.get(f"https://{controller_host}/databases", timeout=5)
    print(f"HTTPS response: {resp.status_code}")
except Exception as e:
    print(f"HTTPS connectivity failed: {e}")
