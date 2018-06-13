import simtables
import pytest
import pkg_resources


def test_load_csv():
    filename = pkg_resources.resource_filename('simtables', 'data/test.csv')
    with open(filename) as fh:
        assert (
            simtables.load_csv(fh)
            ==
            simtables.Table([
                simtables.Record({'a': '1', 'b': '2', 'c': '3'}),
                simtables.Record({'a': '4', 'b': '5', 'c': '6'}),
            ])
        )
