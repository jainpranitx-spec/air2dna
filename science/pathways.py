"""Structured pathway content, deliberately separated from presentation code."""
from __future__ import annotations

from typing import TypedDict


class Reference(TypedDict):
    label: str
    url: str
    summary: str


class PathwayNode(TypedDict):
    id: str
    title: str
    description: str
    evidence_level: str
    uncertainty: str
    references: list[Reference]
    next_nodes: list[str]


OXIDATIVE_NODES: list[PathwayNode] = [
    {"id": "pm25", "title": "PM2.5 exposure", "description": "Fine particulate matter can carry reactive constituents and is associated with oxidative stress pathways.", "evidence_level": "established", "uncertainty": "Composition and deposited dose vary substantially by source and person.", "references": [{"label": "WHO Global Air Quality Guidelines (2021)", "url": "https://www.who.int/publications/i/item/9789240034228", "summary": "Authoritative health guidance and evidence review for particulate matter."}], "next_nodes": ["oxidative-stress"]},
    {"id": "oxidative-stress", "title": "Oxidative stress", "description": "Particle-associated components can contribute to an imbalance between oxidants and antioxidant defenses.", "evidence_level": "established", "uncertainty": "This is a biological mechanism, not a measured response for this individual scenario.", "references": [{"label": "Valavanidis et al., Part Fibre Toxicol. (2008)", "url": "https://pubmed.ncbi.nlm.nih.gov/18325195/", "summary": "Review of particulate matter, oxidative stress, and DNA damage mechanisms."}], "next_nodes": ["ros"]},
    {"id": "ros", "title": "Reactive oxygen species", "description": "Reactive oxygen species can modify DNA bases when cellular defenses and repair do not fully compensate.", "evidence_level": "established", "uncertainty": "ROS are short-lived and their local cellular effects are context-dependent.", "references": [{"label": "Cooke et al., FASEB J. (2003)", "url": "https://pubmed.ncbi.nlm.nih.gov/12709404/", "summary": "Oxidative DNA damage mechanisms and biomarkers."}], "next_nodes": ["8-oxo-dg"]},
    {"id": "8-oxo-dg", "title": "8-oxo-dG lesion", "description": "8-oxo-7,8-dihydroguanine is a widely used biomarker of oxidative DNA damage and can mispair during replication.", "evidence_level": "established", "uncertainty": "A pathway diagram cannot infer lesion abundance in a person or tissue.", "references": [{"label": "Nakabeppu, Mutagenesis (2014)", "url": "https://pubmed.ncbi.nlm.nih.gov/24368813/", "summary": "Mechanisms for 8-oxoguanine formation, mutagenesis, and repair."}], "next_nodes": ["base-excision-repair"]},
    {"id": "base-excision-repair", "title": "Base-excision repair", "description": "Enzymes including OGG1 help recognize and remove oxidized bases, preserving genome integrity.", "evidence_level": "established", "uncertainty": "Repair capacity varies by cell state, genetics, and exposure context.", "references": [{"label": "David et al., Nat Rev Mol Cell Biol. (2007)", "url": "https://pubmed.ncbi.nlm.nih.gov/18007677/", "summary": "Review of base excision repair and genome stability."}], "next_nodes": ["potential-mutation"]},
    {"id": "potential-mutation", "title": "Potential replication / repair error", "description": "If a lesion persists into replication or repair is imperfect, a sequence change is a possible downstream consequence.", "evidence_level": "model-based", "uncertainty": "This is a conditional modeled consequence, not a predicted mutation or disease outcome.", "references": [{"label": "Nakabeppu, Mutagenesis (2014)", "url": "https://pubmed.ncbi.nlm.nih.gov/24368813/", "summary": "Describes the mutagenic potential of unrepaired oxidized guanine."}], "next_nodes": ["protein-consequence"]},
    {"id": "protein-consequence", "title": "Potential protein consequence", "description": "A coding sequence change may be synonymous, alter one amino acid, or truncate a protein depending on its genomic context.", "evidence_level": "hypothetical", "uncertainty": "Most details require a specific validated variant and transcript; use the Mutation Explorer to inspect a hypothetical coding example.", "references": [], "next_nodes": []},
]

PAH_NODES: list[PathwayNode] = [
    {"id": "pah", "title": "Combustion-associated PAHs", "description": "Some combustion particles contain polycyclic aromatic hydrocarbons (PAHs).", "evidence_level": "established", "uncertainty": "PM2.5 mass alone cannot determine which PAHs are present or their dose.", "references": [{"label": "IARC Monographs: Outdoor air pollution (2016)", "url": "https://publications.iarc.who.int/538", "summary": "IARC evaluation of outdoor air pollution and particulate matter."}], "next_nodes": ["metabolic-activation"]},
    {"id": "metabolic-activation", "title": "Metabolic activation", "description": "Enzymatic metabolism can convert some PAHs into reactive intermediates.", "evidence_level": "established", "uncertainty": "Activation differs across compounds, tissues, and enzyme activity.", "references": [{"label": "Xue & Warshawsky, Toxicol Appl Pharmacol. (2005)", "url": "https://pubmed.ncbi.nlm.nih.gov/15694476/", "summary": "Review of PAH metabolism and DNA adduct formation."}], "next_nodes": ["dna-adduct"]},
    {"id": "dna-adduct", "title": "DNA adduct", "description": "Reactive PAH metabolites can bind DNA, forming bulky adducts that can distort the helix.", "evidence_level": "established", "uncertainty": "This model does not infer adduct formation in an individual.", "references": [{"label": "Xue & Warshawsky, Toxicol Appl Pharmacol. (2005)", "url": "https://pubmed.ncbi.nlm.nih.gov/15694476/", "summary": "Review of PAH metabolism and DNA adduct formation."}], "next_nodes": ["nucleotide-excision-repair"]},
    {"id": "nucleotide-excision-repair", "title": "Nucleotide-excision repair", "description": "Nucleotide-excision repair can remove many bulky DNA lesions.", "evidence_level": "established", "uncertainty": "Repair efficiency depends on lesion type and cellular context.", "references": [{"label": "Sancar, Annu Rev Biochem. (1996)", "url": "https://pubmed.ncbi.nlm.nih.gov/8811189/", "summary": "Foundational review of DNA excision repair."}], "next_nodes": ["pah-potential-mutation"]},
    {"id": "pah-potential-mutation", "title": "Potential replication interference", "description": "Persistent adducts can interfere with replication; inaccurate lesion bypass or repair can contribute to sequence changes.", "evidence_level": "model-based", "uncertainty": "A possible mechanism, not a predicted mutation or outcome.", "references": [], "next_nodes": []},
]


def build_trace(pathway: str = "oxidative") -> list[PathwayNode]:
    if pathway == "oxidative":
        return OXIDATIVE_NODES
    if pathway == "pah":
        return PAH_NODES
    raise ValueError("Unknown pathway.")
