from science.mutation import annotate_substitution


def test_missense_annotation() -> None:
    result = annotate_substitution("ATGGCC", 4, "T")
    assert result["reference_codon"] == "GCC"
    assert result["alternate_codon"] == "TCC"
    assert result["classification"] == "missense"


def test_nonsense_annotation() -> None:
    result = annotate_substitution("CAG", 1, "T")
    assert result["classification"] == "nonsense"


def test_synonymous_annotation() -> None:
    result = annotate_substitution("GCT", 3, "C")
    assert result["classification"] == "synonymous"
