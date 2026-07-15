from data.data import DataManager


def test_get_price():
    """Should return a non-empty dataframe with required columns."""

    dm = DataManager()

    df = dm.get_price("VOO")

    assert not df.empty

    assert "Open" in df.columns
    assert "High" in df.columns
    assert "Low" in df.columns
    assert "Close" in df.columns
    assert "Volume" in df.columns

    assert "Return" in df.columns
    assert "Drawdown" in df.columns


def test_get_prices():

    dm = DataManager()

    prices = dm.get_prices(
        [
            "VOO",
            "QQQM",
        ]
    )

    assert "VOO" in prices
    assert "QQQM" in prices

    assert not prices["VOO"].empty
    assert not prices["QQQM"].empty


def test_refresh():

    dm = DataManager()

    df = dm.refresh("VOO")

    assert not df.empty
