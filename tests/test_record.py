import pytest
from simtables import Table, Record

class TestRecord:
    def test___getitem__(self):
        record = Record({"x": 1, "y": 2})
        with pytest.raises(KeyError):
            record["z"]
        assert record["x"] == 1
        assert record["y"] == 2
        assert record[["x", "y"]] == {"x": 1, "y": 2}
        assert type(record["x"]) is int
        assert type(record[["x", "y"]]) is Record

    def test___setitem__(self):
        record = Record({"x": 1, "y": 2})
        record["x"] = 3
        assert record == {"x": 3, "y": 2}
        record["y"] = 7
        assert record == {"x": 3, "y": 7}
        record[["x", "y"]] = {"x": 10, "y": 11}
        assert record == {"x": 10, "y": 11}
        record[["x", "a", "b"]] = {"x": 3, "a": 4, "b": 5}
        assert record == {"x": 3, "y": 11, "a": 4, "b": 5}

    def test_get(self):
        record = Record({"x": 1, "y": 2})
        assert record.get("x") == 1
        assert record.get(["x", "y"]) == {"x": 1, "y": 2}
        assert record.get("z") is None
        with pytest.raises(Exception):
            record.get(["x", "y", "z"], 17)
        assert record.get(["x", "y", "z"]) == {"x": 1, "y": 2}
        record.get(["x", "y", "z"], {"u": 16}) == {"x": 1, "y": 2}
        assert record.get(["x", "y", "z"], {"z": 16}) == (
            {"x": 1, "y": 2, "z":16})

    def test_pop(self):
        record = Record(x=1, y=2, z=3)
        assert record.pop("x") == 1
        assert record == {"y": 2, "z": 3}

        record = Record(x=1, y=2, z=3)
        with pytest.raises(KeyError):
            record.pop("a")
        assert record == {"x": 1, "y": 2, "z": 3}

        record = Record(x=1, y=2, z=3)
        assert record.pop("a", 6) == 6
        assert record == {"x": 1, "y": 2, "z": 3}

        record = Record(x=1, y=2, z=3)
        assert record.pop(["x", "z"]) == Record(x=1, z=3)
        assert record == Record(y=2)

        record = Record(x=1, y=2, z=3)
        with pytest.raises(KeyError):
            record.pop(["x", "a"])
        assert record == Record(x=1, y=2, z=3)

        record = Record(x=1, y=2, z=3)
        with pytest.raises(Exception):
            record.pop(["x", "a"], 2)
        assert record == Record(x=1, y=2, z=3)

        record = Record(x=1, y=2, z=3)
        assert record.pop(["x", "a"], {"a": 16}) == {"x": 1, "a": 16}
        assert record == Record(y=2, z=3)

        r = Record(x=1, y=2, z=3)
        assert r.pop(["x", "y", "w"], default={"w": 2}) == Record(x=1, y=2, w=2)

    def test_popitem(self):
        pass

    def test_copy(self):
        record = Record()
        assert type(record.copy()) is Record
        record["x"] = 1
        new_record = record.copy()
        new_record["x"] = 4
        assert record["x"] == 1

    def test___str__(self):
        pass

    def test___repr__(self):
        pass

    def test_merge(self):
        r = Record(x=1, y=2, z=3)
        s = Record(u=4, v=5)
        assert Record.merge([r, s]) == Record(x=1, y=2, z=3, u=4, v=5)
        assert r == Record(x=1, y=2, z=3)
        assert s == Record(u=4, v=5)

        r = Record(x=1, y=2, z=3)
        s = Record(y=2, v=5)
        assert Record.merge([r, s]) == Record(x=1, y=2, z=3, v=5)

        r = Record(x=1, y=2, z=3)
        s = Record(y=3, v=5)
        with pytest.raises(ValueError):
            Record.merge([r, s])

        r = Record(x=1, y=2, z=3)
        s = Record(y=2, v=5)
        t = Record(v=5, w=4)
        assert Record.merge([r, s, t]) == Record(x=1, y=2, z=3, v=5, w=4)

    def test_without(self):
        r = Record(a=1, b=2, c=3)
        assert r.without(["a"]) == {"b": 2, "c": 3}
        assert r.without(["a", "c"]) == {"b": 2}
        assert r.without(["d", "c"]) == {"a": 1, "b": 2}

    def test_merge_conflicts(self):
        assert Record.merge_conflicts(
            [Record(a=1, b=2, c=3),
             Record(a=1, b=3, c=3),
             ]
        ) == ["b"]
