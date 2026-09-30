"""Small deterministic coding-sequence substitution annotator."""
from __future__ import annotations

from Bio.Seq import Seq


def annotate_substitution(sequence: str, position: int, alternate: str) -> dict[str, object]:
    sequence = sequence.upper().replace(" ", "")
    alternate = alternate.upper()
    if any(base not in "ACGT" for base in sequence) or alternate not in "ACGT":
        raise ValueError("Sequence and alternate must use A, C, G, or T only.")
    if position > len(sequence):
        raise ValueError("Position is outside the supplied sequence.")
    reference = sequence[position - 1]
    mutated = sequence[: position - 1] + alternate + sequence[position:]
    codon_start = ((position - 1) // 3) * 3
    if codon_start + 3 > len(sequence):
        raise ValueError("Position must fall inside a complete coding codon.")
    reference_codon = sequence[codon_start : codon_start + 3]
    alternate_codon = mutated[codon_start : codon_start + 3]
    reference_aa = str(Seq(reference_codon).translate())
    alternate_aa = str(Seq(alternate_codon).translate())
    if reference == alternate:
        classification = "no change"
    elif alternate_aa == reference_aa:
        classification = "synonymous"
    elif alternate_aa == "*":
        classification = "nonsense"
    else:
        classification = "missense"
    return {"position": position, "nucleotide_change": f"{reference}>{alternate}", "reference_codon": reference_codon, "alternate_codon": alternate_codon, "codon_number": codon_start // 3 + 1, "reference_amino_acid": reference_aa, "alternate_amino_acid": alternate_aa, "classification": classification, "mutated_sequence": mutated}
