import random
from datetime import datetime

levels:list[str] = [
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR"]
services:list[str] = [
    "auth-service",
    "db-service",
    "io-service",
    "dns-service"
]
messages:dict[str, list[str]] = {
    "DEBUG": ["Started", "Stopped", "Hello World"],
    "INFO": ["Running smoothly", "Connected", "Disconnected"],
    "WARNING": ["Resources low", "getting late", "no responses"],
    "ERROR": ["Unexpected error", "invalid value", "division by zero"]
}

def create_message():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level = random.choices(levels, k=1, weights=[0.1, 0.6, 0.2, 0.1])[0]
    service = random.choice(services)
    message = random.choice(messages[level])
    return f"[{timestamp}] [{level}] [{service}] {message}\n"


def generate_log(n = 1000):
    log:list[str] = []
    for i in range(n):
        msg = create_message()
        log.append(msg)
    with open("sample.log", "w") as f:
        f.writelines(log)
    print("log file created")


if __name__ == "__main__":
    generate_log()
