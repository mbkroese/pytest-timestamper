import freezegun
import pytest

pytest_plugins = ["pytester"]


@pytest.fixture
def example_suite(testdir):
    testdir.makepyfile(
        """
    def test_1(): pass
    def test_2(): pass
    def test_3(): pass
    """
    )
    yield testdir


@pytest.fixture
def slow_suite(testdir):
    testdir.makepyfile(
        """
    import time
    def test_1():
        time.sleep(1.1)
    """
    )
    yield testdir


class TestTimestamperFormatArguments:
    @freezegun.freeze_time("2021-01-01")
    def test_accepts_date_format_argument(self, example_suite, capsys):
        result = example_suite.inline_run("-v", "--datefmt", "%Y-%m-%d")

        assert result.ret == 0
        result.assertoutcome(passed=3)

        outerr = capsys.readouterr()
        assert "[2021-01-01] test_accepts_date_format_argument.py::test_1" in outerr.out

    @freezegun.freeze_time("2021-01-01 12:00:00")
    def test_accepts_prefix_format_argument(self, example_suite, capsys):
        result = example_suite.inline_run("-v", "--prefixfmt", "xxx {formatted_datetime} xxx ")

        assert result.ret == 0
        result.assertoutcome(passed=3)

        outerr = capsys.readouterr()
        assert "xxx 2021-01-01 12:00:00 xxx test_accepts_prefix_format_argument.py::test_1" in outerr.out

    @freezegun.freeze_time("2021-01-01 12:00:00")
    def test_accepts_prefix_and_date_format_argument(self, example_suite, capsys):
        result = example_suite.inline_run("-v", "--datefmt", "%Y", "--prefixfmt", "xxx {formatted_datetime} xxx ")

        assert result.ret == 0
        result.assertoutcome(passed=3)

        outerr = capsys.readouterr()
        assert "xxx 2021 xxx test_accepts_prefix_and_date_format_argument.py::test_1" in outerr.out


class TestTimestamperTimestampsInVerboseMode:
    @freezegun.freeze_time("2021-01-01 12:00:00")
    def test_has_expected_output(self, example_suite, capsys):
        result = example_suite.inline_run("-v")

        assert result.ret == 0
        result.assertoutcome(passed=3)

        outerr = capsys.readouterr()
        assert "[2021-01-01 12:00:00] test_has_expected_output.py::test_1" in outerr.out
        assert "[2021-01-01 12:00:00] test_has_expected_output.py::test_2" in outerr.out
        assert "[2021-01-01 12:00:00] test_has_expected_output.py::test_3" in outerr.out

    def test_prints_only_one_line_per_test(self, slow_suite, capsys):
        result = slow_suite.inline_run("-v")

        assert result.ret == 0
        result.assertoutcome(passed=1)

        outerr = capsys.readouterr()
        lines = outerr.out.split("\n")

        counter = 0
        for line in lines:
            counter += int("test_prints_only_one_line_per_test.py::test_1" in line)
        assert counter == 1
