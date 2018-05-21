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


class TestTable:
    @pytest.fixture
    def simple_table(self):
        return Table([
            Record(a=1, b=4, c=7),
            Record(a=2, b=5, c=8),
            Record(a=3, b=6, c=9),
            ])

    def test_copy(self):
        t = Table([
            Record(a=1, b=4, c=7),
            Record(a=2, b=5, c=8),
            Record(a=3, b=6, c=9),
            ])
        s = t.copy()
        s[0]["a"] = 13
        assert t[0]["a"] == 1

    def test___getitem__(self):
        t = Table([
            Record(a=1, b=4, c=7),
            Record(a=2, b=5, c=8),
            Record(a=3, b=6, c=9),
            ])

        assert t[0] == Record(a=1, b=4, c=7)
        assert t[1] == Record(a=2, b=5, c=8)
        assert t[2] == Record(a=3, b=6, c=9)

        assert type(t[0:1]) is Table
        assert t[0:1] == Table([Record(a=1, b=4, c=7)])
        assert t[0:2] == Table([
            Record(a=1, b=4, c=7),
            Record(a=2, b=5, c=8),
        ])
        assert t[[0, 2]] == Table(
            [
                Record(a=1, b=4, c=7),
                Record(a=3, b=6, c=9),
            ]
        )

        assert t["a"] == [1, 2, 3]
        assert type(t["a"]) is list

        assert t[["a", "c"]] == Table([
            Record(a=1, c=7),
            Record(a=2, c=8),
            Record(a=3, c=9)])
        assert type(t[["a", "c"]]) is Table

    def test___setitem___index(self, simple_table):
        simple_table[0] = Record(a=0, b=2, c=4)
        assert simple_table[0] == Record(a=0, b=2, c=4)

    def test___setitem___indices(self, simple_table):
        simple_table[0:2] = Table([
            Record(a=7, b=3, c=9),
            Record(a=5, b=7, c=4),
            ])
        assert simple_table[0:2] == Table([
            Record(a=7, b=3, c=9),
            Record(a=5, b=7, c=4),
            ])

    def test___setitem___key(self, simple_table):
        simple_table["a"] = [10, 11, 12]
        r0 = simple_table[0]
        assert simple_table["a"] == [10, 11, 12]
        assert r0["a"] == 10

    def test___setitem___keys(self, simple_table):
        t = Table()
        t.append(Record(a=1, b=4, c=7))
        t.append(Record(a=2, b=5, c=8))
        t.append(Record(a=3, b=6, c=9))

        s = Table()
        s.append(Record(a=10, c=13))
        s.append(Record(a=11, c=14))
        s.append(Record(a=12, c=15))
        #t[["a", "c"]] = s

        r = Table()
        r.append(Record(a=10, b=4, c=13))
        r.append(Record(a=11, b=5, c=14))
        r.append(Record(a=12, b=6, c=15))

        # s = Table()
        # s.append(Record(a=13, d=16))
        # s.append(Record(a=14, d=17))
        # s.append(Record(a=15, d=18))
        # t[["a", "d"]] = s

        # r = Table()
        # r.append(Record(a=13, b=4, c=13, d=16))
        # r.append(Record(a=14, b=5, c=14, d=17))
        # r.append(Record(a=15, b=6, c=15, d=18))
        # assert t == r

    def test_get(self):
        t = Table([
            Record(x=1, y=2),
            Record(x=2, y=4, z=3)
        ])
        assert t.get(["z"]) == Table([
            Record(),
            Record(z=3),
        ])
        assert t.get(["z"], {"z": None}) == Table([
            Record(z=None),
            Record(z=3),
        ])


    def test_pop(self):
        r0 = Record(x=1, y=2, z=3)
        r1 = Record(x=2, y=2, z=3)
        t = Table([r0, r1])

        assert t.pop("x") == [1, 2]
        assert r0 == Record(y=2, z=3)
        assert r1 == Record(y=2, z=3)

    def test_keys(self):
        t = Table()
        t.append(Record(a=1, b=2, c=3))
        assert set(t.keys()) == set(["a", "b", "c"])

    def test___str__(self):
        pass

    def test___repr__(self):
        pass

    def test___add__(self):
        t = Table()
        t.append(Record(a=1, b=4, c=7))

        assert t + t == Table([
            Record(a=1, b=4, c=7),
            Record(a=1, b=4, c=7)])

        assert type(t + t) is Table

    def test_sorted(self):
        pass

    def test_filter(self):
        t = Table([
            Record(x=1, y=2, z=3),
            Record(x=2, y=2, z=3),
            Record(x=1, y=2, z=4),
            Record(x=2, y=1, z=3),
            Record(x=1, y=2, z=3),
            Record(x=3, y=3, z=4),
        ])

        assert t.filter(lambda r: r["z"] > 3) == Table([
            Record(x=1, y=2, z=4),
            Record(x=3, y=3, z=4),
        ])

    def test_partition(self):
        pass

    def test_key_index(self):
        t = Table([
            Record(a=1, b=4, c=7),
            Record(a=2, b=4, c=9),
            Record(a=1, b=6, c=9, d=4),
            ])
        assert t.key_index({"a": 1}) == 0
        assert t.key_index({"a": 1}, 1) == 2
        assert t.key_index({"d": 4}) == 2


    def test_key_count(self):
        t = Table([
            Record(x=1, y=2),
            Record(x=2, y=2),
            Record(x=1, y=2),
            Record(x=1, y=2, z=3),
            ])
        assert t.key_count({"x": 1}) == 3
        assert t.key_count({"y": 2}) == 4
        assert t.key_count({"x": 1, "y": 2}) == 3
        assert t.key_count({"z": 3}) == 1
        assert t.key_count({"w": 3}) == 0
        assert t.key_count({"z": 4}) == 0

    def test_key_sort(self):
        t = Table([
            Record(x=1, y=2, z=3),
            Record(x=1, y=2, z=4),
            Record(x=2, y=1, z=3),
            Record(x=3, y=3, z=4),
            Record(x=2, y=2, z=3),
            Record(x=1, y=2, z=3),
        ])

        t.key_sort(["x"])
        assert t == Table([
            Record(x=1, y=2, z=3),
            Record(x=1, y=2, z=4),
            Record(x=1, y=2, z=3),
            Record(x=2, y=1, z=3),
            Record(x=2, y=2, z=3),
            Record(x=3, y=3, z=4),
        ])
        assert type(t) is Table

    def test_key_sorted(self):
        t = Table([
            Record(x=1, y=2, z=3),
            Record(x=2, y=2, z=3),
            Record(x=1, y=2, z=4),
            Record(x=3, y=3, z=4),
            Record(x=1, y=2, z=3),
            Record(x=2, y=1, z=3),
        ])

        assert type(t.key_sorted(["x"])) is Table

        assert t.key_sorted(["y"]) == Table([
            Record(x=2, y=1, z=3),
            Record(x=1, y=2, z=3),
            Record(x=2, y=2, z=3),
            Record(x=1, y=2, z=4),
            Record(x=1, y=2, z=3),
            Record(x=3, y=3, z=4),
            ])

        assert t.key_sorted(["z", "y"]) == Table([
            Record(x=2, y=1, z=3),
            Record(x=1, y=2, z=3),
            Record(x=2, y=2, z=3),
            Record(x=1, y=2, z=3),
            Record(x=1, y=2, z=4),
            Record(x=3, y=3, z=4),
            ])

        assert t.key_sorted(["x", "y"]) == Table([
            Record(x=1, y=2, z=3),
            Record(x=1, y=2, z=4),
            Record(x=1, y=2, z=3),
            Record(x=2, y=1, z=3),
            Record(x=2, y=2, z=3),
            Record(x=3, y=3, z=4),
            ])

        assert t.key_sorted(["z", "x", "y"]) == Table([
            Record(x=1, y=2, z=3),
            Record(x=1, y=2, z=3),
            Record(x=2, y=1, z=3),
            Record(x=2, y=2, z=3),
            Record(x=1, y=2, z=4),
            Record(x=3, y=3, z=4),
            ])

    def test_key_filter(self):
        t = Table([
            Record(x=1, y=2, z=3),
            Record(x=2, y=2, z=3),
            Record(x=1, y=2, z=4),
            Record(x=2, y=1, z=3, w=6),
            Record(x=1, y=2, z=3, w=6),
            Record(x=3, y=3, z=4, w=7),
        ])

        assert t.key_filter({"x": 1, "z": 3}) == Table([
            Record(x=1, y=2, z=3),
            Record(x=1, y=2, z=3, w=6),
        ])
        assert t.key_filter({"w": 6}) == Table([
            Record(x=2, y=1, z=3, w=6),
            Record(x=1, y=2, z=3, w=6),
        ])

    def test_key_partition(self):
        pass

    def test_key_groupby(self):
        pass

    def test_key_sorted_groupby(self):
        pass
    #     t = Table()
    #     t.append(Record(x=1, y=2, z=3))
    #     t.append(Record(x=1, y=2, z=4))
    #     t.append(Record(x=2, y=1, z=3))
    #     t.append(Record(x=3, y=3, z=4))
    #     t.append(Record(x=2, y=2, z=3))
    #     t.append(Record(x=1, y=2, z=3))

    #     assert list(t.key_groupby(["x"])) == [
    #         (Record(x=1), Table([
    #             Record(x=1, y=2, z=3),
    #             Record(x=1, y=2, z=4),
    #         ])),
    #         (Record(x=2), Table([
    #             Record(x=2, y=1, z=3),
    #         ])),
    #         (Record(x=3), Table([
    #             Record(x=3, y=3, z=4),
    #         ])),
    #         (Record(x=2), Table([
    #             Record(x=2, y=2, z=3),
    #         ])),
    #         (Record(x=1), Table([
    #             Record(x=1, y=2, z=3),
    #         ])),
    #         ]

    #     # This causes an error because of the way groupby works.
    #     assert list(t.key_groupby("x")) == [
    #         (1, Table([
    #             Record(x=1, y=2, z=3),
    #             Record(x=1, y=2, z=4),
    #         ])),
    #         (2, Table([
    #             Record(x=2, y=1, z=3),
    #         ])),
    #         (3, Table([
    #             Record(x=3, y=3, z=4),
    #         ])),
    #         (2, Table([
    #             Record(x=2, y=2, z=3),
    #         ])),
    #         (1, Table([
    #             Record(x=1, y=2, z=3),
    #         ])),
    #         ]

    #     assert False

    #     for x, y in zip(t.groupby(["x"], invert=True), t.groupby(["y", "z"])):
    #         assert x == y

    #     t = Table()
    #     t.append(Record(x=1, y=2, z=3))
    #     t.append(Record(x=1, y=2, z=4))
    #     t.append(Record(x=2, y=1))
    #     t.append(Record(x=3, y=3))
    #     t.append(Record(x=2, y=2, z=3))
    #     t.append(Record(x=1, y=2, z=3))

    #     assert list(t.groupby(["x"])) == [
    #         (Record(x=1), Table([
    #             Record(x=1, y=2, z=3),
    #             Record(x=1, y=2, z=4),
    #             Record(x=1, y=2, z=3),
    #         ])),
    #         (Record(x=2), Table([
    #             Record(x=2, y=1),
    #             Record(x=2, y=2, z=3),
    #         ])),
    #         (Record(x=3), Table([
    #             Record(x=3, y=3),
    #         ])),
    #         ]

    #     assert list((rec, list(group)) for rec, group in t.groupby(["z"])) == [
    #         (Record(), Table([
    #             Record(x=2, y=1),
    #             Record(x=3, y=3),
    #         ])),
    #         (Record(z=3), Table([
    #             Record(x=1, y=2, z=3),
    #             Record(x=2, y=2, z=3),
    #             Record(x=1, y=2, z=3),
    #         ])),
    #         (Record(z=4), Table([
    #             Record(x=1, y=2, z=4),
    #         ])),
    #         ]

    def test_index(self):
        t = Table()
        t.append(Record(a=1, b=4, c=7))
        t.append(Record(a=2, b=5, c=8))
        t.append(Record(a=3, b=6, c=9))

        t.index(Record(a=1, b=4, c=7)) == 0

    def test_match(self):
        t = Table([
            Record(x=1, y=2, z=3),
            Record(x=1, y=6, z=3),
            Record(x=1, y=2, z=3),
            ])

        assert t.match({"x": 1, "y": 6}) == Record(x=1, y=6, z=3)
        with pytest.raises(ValueError):
            t.match({"x": 1, "y": 2})
        assert t.match({"x": 1, "y": 6, "w": 9}) == Record(x=1, y=6, z=3)
        with pytest.raises(ValueError):
            t.match({"a": 1})

        s = Table([
            Record(x=1, y=2, z=3),
            ])
        assert s.match({"a": 7}) == Record(x=1, y=2, z=3)

        s = Table([
            Record(x=1, y=2),
            Record(x=1, y=4, z=3),
        ])
        with pytest.raises(ValueError):
            s.match({"x": 1, "z": 3})
