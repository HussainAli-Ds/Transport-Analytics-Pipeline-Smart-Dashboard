import os

BASE_DIR = "C:/Pipeline-Transportor"

INPUT_DIR = os.path.join(BASE_DIR, "input_files")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed_files")
FAILED_DIR = os.path.join(BASE_DIR, "failed_files")
LOG_DIR = os.path.join(BASE_DIR, "logs")

DB_URL = "postgresql+psycopg2://hussainali:hussain12@localhost:5432/supplier"

FUZZ_THRESHOLD = 80

KNOWN_TRANSPORTERS = [
    "Shah Faisal",
    "Sanaullah",
    "Shahid",
    "Mustafa"
]

TRANSPORTER_ALIASES = {
    "shah fasal": "Shah Faisal",
    "shah faisl": "Shah Faisal",
    "sana ullah": "Sanaullah",
    "sanaula": "Sanaullah",
    "mustfa": "Mustafa"
}

KNOWN_MATERIALS = [
    "Subbase",
    "38MM",
    "10MM",
    "Khaka",
    "05MM",
    "20MM",
    "25MM",
    "Over subbase",
    "Rejected Subbase"
]

MATERIAL_ALIASES = {
    "sub base": "Subbase",
    "reject subbase": "Rejected Subbase",
    "over sub base": "Over subbase",
    "38 mm": "38MM",
    "10 mm": "10MM"
}