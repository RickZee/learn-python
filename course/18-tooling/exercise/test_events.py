from pylearn import load_exercise


def test_log_event_records_info(caplog):
    events = load_exercise("events")
    with caplog.at_level("INFO", logger="tooling"):
        events.log_event("ready")
    assert "ready" in caplog.text
