from odd_collector_sdk.domain.filter import Filter


def test_default_filter():
    filter = Filter()
    assert filter.validate("test_table")
    assert filter.validate("test_column")
    assert filter.validate("test_schema")


def test_default_filter_with_excluded():
    filter = Filter(exclude=[".*_pii"])
    assert filter.validate("table_one")
    assert not filter.validate("table_one_pii")


def test_case_sensitive_include_filter():
    filter = Filter(include=["dev_table"])
    assert filter.validate("dev_table")
    assert not filter.validate("prod_table")


def test_case_sensitive_exclude_filter():
    filter = Filter(include=["test_table_.*"], exclude=[".*_pii"])
    assert filter.validate("test_table_one")
    assert not filter.validate("test_table_pii")


def test_case_insensitive_include_filter():
    filter = Filter(include=["table_", "column_"], ignore_case=True)
    assert filter.validate("Table_one")
    assert filter.validate("COLumn_X")
    assert not filter.validate("column")


def test_case_insensitive_exclude_filter():
    filter = Filter(include=["table_"], exclude=[".*_pii"], ignore_case=True)
    assert filter.validate("table_one")
    assert not filter.validate("table_one_PII")
