import argparse, httpx
from pathlib import Path

ALLOWED = {".pdf", ".txt", ".docx"}

def seed(folder: str, api_url: str):
    files = [f for f in Path(folder).rglob("*") if f.suffix in ALLOWED]
    print(f"Found {len(files)} files")
    for f in files:
        with open(f, "rb") as fh:
            resp = httpx.post(
                f"{api_url}/api/upload",
                files={"file": (f.name, fh, "application/octet-stream")},
                timeout=30,
            )
        mark = "✓" if resp.status_code == 200 else "✗"
        print(f"  {mark} {f.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default="./sample_docs")
    parser.add_argument("--api",    default="http://localhost:8000")
    args = parser.parse_args()
    seed(args.folder, args.api)