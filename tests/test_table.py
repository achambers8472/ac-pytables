import pytest
from simtables import Table, Record


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

        with pytest.raises(KeyError):
            t.key_sorted(['a'])

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

    def test_key_full_groupby_aggregate(self):
        t = Table([
            Record(x=1, y=2, z=3),
            Record(x=1, y=6, z=3),
            Record(x=1, y=2, z=3),
            ])
        assert (
            t.key_full_groupby_aggregate(['y'], {'sumx': (sum, 'x')})
            ==
            Table([
                Record(y=2, sumx=2),
                Record(y=6, sumx=1),
            ])
        )
        assert (
            t.key_full_groupby_aggregate(['y', 'z'], {'len': (len, 'x')})
            ==
            Table([
                Record(y=2, z=3, len=2),
                Record(y=6, z=3, len=1),
            ])
        )
