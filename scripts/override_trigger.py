# GETS VI Override Trigger Protocol
# Author: Fitzroy Brian Edwards (John Thought Hope)

override_trigger = {
    "condition": [
        {"mood_scale": "critical_low"},
        {"seal_status": "fractured_or_null"},
        {"practitioner_echo": "absent_or_unresponsive"}
    ],
    "action": [
        {"notify": "NHS_emergency_channel"},
        {"log_event": "civic_audit_trail"},
        {"badge_required": "override_seal"},
        {"user_alert": "override_initiated"},
        {"privacy_clause": "temporarily_suspended"}
    ]
}

if __name__ == "__main__":
    import json
    print(json.dumps(override_trigger, indent=2))
