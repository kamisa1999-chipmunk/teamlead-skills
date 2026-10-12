#!/usr/bin/env python3
"""Scan meeting transcripts in Downloads for a person's group-meeting contributions."""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

TEAMLEAD = "Саидова Камилла"


def parse_date(text: str, filename: str) -> Optional[str]:
    m = re.search(r"Встреча проходила (\d{2})\.(\d{2})\.(\d{4})", text)
    if m:
        return f"{m.group(1)}.{m.group(2)}.{m.group(3)}"
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", filename)
    if m:
        return f"{m.group(3)}.{m.group(2)}.{m.group(1)}"
    return None


def parse_meeting_time(text: str) -> Optional[str]:
    m = re.search(r"Встреча проходила \d{2}\.\d{2}\.\d{4} с (\d{2}:\d{2})", text)
    return m.group(1) if m else None


def date_ge(d: str, since: str) -> bool:
    def key(s):
        parts = s.split(".")
        return (int(parts[2]), int(parts[1]), int(parts[0]))

    return key(d) >= key(since)


def get_speakers(text: str) -> set:
    speakers = set()
    for line in text.splitlines():
        m = re.match(r"^(.+?)(?: \(голос \d+\))?:\s*$", line.strip())
        if m:
            name = m.group(1).strip()
            if not name.startswith("[") and "Встреча проходила" not in name:
                speakers.add(name)
    return speakers


def is_one_on_one(speakers: set, person_substr: str) -> bool:
    non_lead = [s for s in speakers if TEAMLEAD not in s]
    if len(non_lead) != 1:
        return False
    return person_substr in non_lead[0]


def extract_meeting_topic(text: str, max_lines: int = 40) -> str:
    """Pull early meeting context from non-person lines (usually agenda)."""
    lines = text.splitlines()
    snippets = []
    for line in lines[1:max_lines]:
        m = re.match(r"\[\d{2}:\d{2}:\d{2}\]\s*(.+)", line.strip())
        if m and len(m.group(1)) > 30:
            snippets.append(m.group(1))
        if len(snippets) >= 5:
            break
    return " ".join(snippets)[:800]


def extract_person_segments(text: str, person_substr: str) -> List[dict]:
    lines = text.splitlines()
    segments: List[dict] = []
    current: Optional[str] = None
    start_time: Optional[str] = None
    buf: List[str] = []

    def flush():
        if current and person_substr in current and buf:
            segments.append(
                {
                    "time": start_time or "?",
                    "text": " ".join(buf).strip(),
                }
            )

    for line in lines:
        m = re.match(r"^(.+?)(?: \(голос \d+\))?:\s*$", line.strip())
        if m:
            flush()
            current = m.group(1).strip()
            start_time = None
            buf = []
        elif current and person_substr in current:
            m2 = re.match(r"\[(\d{2}:\d{2}:\d{2})\]\s*(.*)", line.strip())
            if m2:
                if start_time is None:
                    start_time = m2.group(1)
                if m2.group(2):
                    buf.append(m2.group(2))
    flush()
    return segments


def scan(downloads: Path, person: str, since: Optional[str]) -> List[dict]:
    results = []
    for path in sorted(downloads.glob("*.txt")):
        if not re.match(r"\d{4}-\d{2}-\d{2}", path.name):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if person not in text:
            continue
        speakers = get_speakers(text)
        if is_one_on_one(speakers, person):
            continue
        date = parse_date(text, path.name)
        if not date:
            continue
        if since and not date_ge(date, since):
            continue
        segments = extract_person_segments(text, person)
        if not segments:
            continue
        results.append(
            {
                "date": date,
                "meeting_time": parse_meeting_time(text),
                "file": path.name,
                "file_path": str(path),
                "speakers_count": len(speakers),
                "speakers": sorted(speakers),
                "topic_hint": extract_meeting_topic(text),
                "segments": segments,
            }
        )
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--person", required=True, help="Substring of person name, e.g. Гуминиченко")
    parser.add_argument("--since", help="DD.MM.YYYY — only meetings on or after this date")
    parser.add_argument("--downloads", default=str(Path.home() / "Downloads"))
    args = parser.parse_args()

    meetings = scan(Path(args.downloads), args.person, args.since)
    json.dump(meetings, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
