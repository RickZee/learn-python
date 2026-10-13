from triage.classify import Ticket, confusion_matrix, precision_recall


def test_confusion_matrix():
    got = [Ticket(text="a", label="billing"), Ticket(text="b", label="other")]
    matrix = confusion_matrix(got, ["billing", "other"], ["billing", "other"])
    assert matrix["billing"]["billing"] == 1
    assert matrix["other"]["other"] == 1


def test_precision_recall():
    matrix = {"billing": {"billing": 1, "other": 0}, "other": {"billing": 1, "other": 1}}
    precision, recall = precision_recall(matrix, "billing")
    assert precision == 0.5
    assert recall == 1.0
