import logging
import os

#directory creation
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

#path
LOG_FILE = os.path.join(LOG_DIR, "chatbot.log")

#configure
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # Optional: also logs to console
    ]
)

#global
logger = logging.getLogger("chatbot")
