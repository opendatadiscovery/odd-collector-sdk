from odd_collector_sdk.domain.filter import Filter


def test_default_filter():
    filter = Filter()
    assert filter.is_allowed("test_table")
    assert filter.is_allowed("test_column")
    assert filter.is_allowed("test_schema")


def test_default_filter_with_excluded():
    filter = Filter(exclude=[".*_pii"])
    assert filter.is_allowed("table_one")
    assert not filter.is_allowed("table_one_pii")


def test_case_sensitive_include_filter():
    filter = Filter(include=["dev_table"])
    assert filter.is_allowed("dev_table")
    assert not filter.is_allowed("prod_table")


def test_case_sensitive_exclude_filter():
    filter = Filter(include=["test_table_.*"], exclude=[".*_pii"])
    assert filter.is_allowed("test_table_one")
    assert not filter.is_allowed("test_table_pii")


def test_case_insensitive_include_filter():
    filter = Filter(include=["table_", "column_"], ignore_case=True)
    assert filter.is_allowed("Table_one")
    assert filter.is_allowed("COLumn_X")
    assert not filter.is_allowed("column")


def test_case_insensitive_exclude_filter():
    filter = Filter(include=["table_"], exclude=[".*_pii"], ignore_case=True)
    assert filter.is_allowed("table_one")
    assert not filter.is_allowed("table_one_PII")
