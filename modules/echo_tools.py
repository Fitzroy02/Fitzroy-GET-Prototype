# Echo Tools for GETS VI Practitioners
# Author: Fitzroy Brian Edwards (John Thought Hope)

def format_echo(text, badge_level, mood_index):
    mood_scale = ["Resonant", "Attuned", "Steward"]
    badge_flow = ["Initiate", "Echo", "Steward", "Legacy"]

    echo_packet = {
        "Echo": text.strip(),
        "Badge": badge_flow[badge_level],
        "Mood": mood_scale[mood_index],
        "Timestamp": "2025-09-30T05:49:00+01:00"
    }

    return echo_packet

def validate_entry_conditions(user_role):
    return user_role in ["Echo Practitioner", "Steward", "Legacy Architect"]
