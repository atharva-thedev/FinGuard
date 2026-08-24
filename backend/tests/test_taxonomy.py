from app.domain.taxonomy import DEFAULT_CATEGORIES, guess_category


def test_default_categories():
    assert "Travel" in DEFAULT_CATEGORIES
    assert "Software" in DEFAULT_CATEGORIES
    assert "Office Supplies" in DEFAULT_CATEGORIES
    assert "Other" in DEFAULT_CATEGORIES


def test_guess_category():
    assert guess_category("Uber Trip 123") == "Travel"
    assert guess_category("AWS Cloud Services") == "Software"
    assert guess_category("Staples Office Depot") == "Office Supplies"
    assert guess_category("Unknown Random Corp") == "Other"
