def test_basic_count():
    data = [{"district": "1"}, {"district": "1"}, {"district": "2"}]

    count = sum(1 for d in data if d["district"] == "1")

    assert count == 2