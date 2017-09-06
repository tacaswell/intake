import pytest

from intake.plugins import base


def test_plugin_base():
    p = base.Plugin(version='0.1.0', container='dataframe', partition_access=False)

    assert p.version == '0.1.0'
    assert p.container == 'dataframe'
    assert p.partition_access == False
    with pytest.raises(Exception) as except_info:
        p.open()

    assert 'open' in str(except_info.value)


def test_datasource_base_method_exceptions():
    # Unimplemented methods should raise exceptions
    d = base.DataSource(container='dataframe')

    for method_name in ['discover', 'read', 'read_chunked', 'read_partition', 'to_dask', 'close']:
        method = getattr(d, method_name)
        with pytest.raises(Exception) as except_info:
            method()
        assert method_name in str(except_info.value)


def test_datasource_base_context_manager():
    # Base data source should raise a "need to implement" exception when it
    # leaves the context manager

    with pytest.raises(Exception) as except_info:
        with base.DataSource(container='dataframe') as d:
            pass
    assert 'close' in str(except_info.value)