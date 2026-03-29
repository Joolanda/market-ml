import re
from pathlib import Path

# Determine project root based on script location
ROOT = Path(__file__).resolve().parents[1]

ROADMAP = ROOT / "docs" / "ROADMAP.md"
KANBAN = ROOT / "docs" / "KANBAN.md"




# Mapping between roadmap phases and kanban steps
PHASE_TO_STEP = {
    "Phase 1": "Step 1",
    "Phase 2": "Step 3",
    "Phase 3": "Step 4",
    "Phase 4": "Step 4",
    "Phase 5": "Step 5"
}

def extract_phase_status():
    """Extracts the status of each phase from ROADMAP.md."""
    text = ROADMAP.read_text()

    statuses = {}
    pattern = r"## (Phase \d+) — .*?\n\n(.*?)\n\n"
    matches = re.findall(pattern, text, flags=re.DOTALL)

    for phase, content in matches:
        if "Completed" in content:
            statuses[phase] = "Done"
        elif "In Progress" in content:
            statuses[phase] = "In Progress"
        else:
            statuses[phase] = "To Do"

    return statuses


def update_kanban(phase_status):
    """Updates KANBAN.md based on roadmap phase status."""
    kanban = KANBAN.read_text()

    for phase, status in phase_status.items():
        step = PHASE_TO_STEP.get(phase)
        if not step:
            continue

        # Replace the status marker in the Kanban table
        kanban = re.sub(
            rf"(\*\*{step}.*?\|\s*)(To Do|In Progress|✔️|x)(\s*\|)",
            rf"\1{status}\3",
            kanban
        )

    KANBAN.write_text(kanban)
    print("KANBAN.md updated successfully.")


if __name__ == "__main__":
    phase_status = extract_phase_status()
    update_kanban(phase_status)
