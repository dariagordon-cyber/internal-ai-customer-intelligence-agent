import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


def load_csv(filename: str) -> list[dict[str, str]]:
    file_path = DATA_DIR / filename

    with file_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def load_customers() -> list[dict[str, str]]:
    return load_csv("crm_customers.csv")


def load_sales_pipeline() -> list[dict[str, str]]:
    return load_csv("sales_pipeline.csv")


def load_text_file(relative_path: str) -> str:
    file_path = DATA_DIR / relative_path

    with file_path.open("r", encoding="utf-8") as file:
        return file.read()


def load_meeting_transcripts() -> dict[str, str]:
    transcripts_dir = DATA_DIR / "meeting_transcripts"
    transcripts = {}

    for file_path in transcripts_dir.glob("*.txt"):
        transcripts[file_path.name] = file_path.read_text(encoding="utf-8")

    return transcripts


def load_internal_policies() -> dict[str, str]:
    policies_dir = DATA_DIR / "internal_policies"
    policies = {}

    for file_path in policies_dir.glob("*.md"):
        policies[file_path.name] = file_path.read_text(encoding="utf-8")

    return policies


def find_customer_by_id(customer_id: str) -> dict[str, str] | None:
    customers = load_customers()

    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer

    return None


def find_deals_by_customer_id(customer_id: str) -> list[dict[str, str]]:
    deals = load_sales_pipeline()

    return [deal for deal in deals if deal["customer_id"] == customer_id]


def find_meeting_transcripts_by_customer_id(customer_id: str) -> dict[str, str]:
    transcripts = load_meeting_transcripts()

    return {
        filename: content
        for filename, content in transcripts.items()
        if f"Customer ID: {customer_id}" in content
    }