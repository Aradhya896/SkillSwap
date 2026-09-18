import os

dirs = [
    "src/main/java/com/skillswap/config",
    "src/main/java/com/skillswap/controller",
    "src/main/java/com/skillswap/dto",
    "src/main/java/com/skillswap/entity",
    "src/main/java/com/skillswap/exception",
    "src/main/java/com/skillswap/repository",
    "src/main/java/com/skillswap/security",
    "src/main/java/com/skillswap/service",
    "src/main/resources"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
