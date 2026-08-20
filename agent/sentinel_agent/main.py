from .client import send_event

if __name__ == "__main__":
    event = {
        "event_type": "agent_status",
        "severity": 1,
        "source": "sentinel-agent",
        "summary": "SentinelCore agent started",
        "payload": {"agent_version": "1.0.0"},
    }
    print(send_event(event))
