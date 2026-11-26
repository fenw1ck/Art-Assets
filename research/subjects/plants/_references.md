---
id: botanical-references
title: Botanical research references and evidence policy
kind: reference
parent: plants
updated: 2026-11-26
used_by: [plant-art/infocards.json, research/subjects/plants/*.md, tools/plant-art.py]
---

# Botanical research references

## Taxonomy and accepted names

- [Plants of the World Online (POWO), Royal Botanic Gardens, Kew](https://powo.science.kew.org/) — accepted names, synonyms, taxonomy, distribution, traits, descriptions and image discovery. POWO uses the World Checklist of Vascular Plants backbone and updates regularly. It is advisory; compare regional or taxon-specific treatments where needed.
- [World Flora Online](https://www.worldfloraonline.org/) — global taxonomic backbone and flora-derived species information.
- [International Plant Names Index (IPNI)](https://www.ipni.org/) — nomenclatural publication data and author citations. It is not a source for plant architecture or horticultural performance.

## Specimens, distribution and images

- [Global Biodiversity Information Facility (GBIF)](https://www.gbif.org/) — specimen and occurrence records. Use records with determiner, institution, collection and voucher metadata; an occurrence point alone does not establish morphology.
- [USDA PLANTS](https://plants.usda.gov/) — North American plant profiles and distribution cross-checks.
- [Missouri Botanical Garden Tropicos](https://www.tropicos.org/) — names, specimens, images and linked botanical literature.
- [Biodiversity Heritage Library](https://www.biodiversitylibrary.org/) — digitized historical floras, monographs and original botanical illustrations. Check the date and taxonomic concept of historical works.

## Morphology and regional floras

- [Flora of North America / eFloras](http://www.efloras.org/) — detailed regional descriptions, keys and diagnostic morphology.
- Regional floras, herbarium specimen sheets, peer-reviewed monographs and botanical-garden collections should be preferred for detailed organ morphology and growth architecture.

## Cultivars and horticultural forms

- [Royal Horticultural Society plant profiles](https://www.rhs.org.uk/plants) — cultivar naming and horticultural descriptions.
- For named cultivars, prefer the breeder or cultivar registration authority, an accredited botanical garden, university extension publication or a horticultural trial report. Clearly distinguish cultivar-level evidence from species-level morphology.

## Evidence hierarchy for the renderer

1. Peer-reviewed taxonomic revision, monograph or regional flora for morphology.
2. Herbarium specimen with verified determination and collection metadata for organ arrangement and variation.
3. Botanical garden or university extension publication for cultivation, growth stages and named cultivars.
4. POWO/WFO/IPNI for taxonomic identity and synonymy.
5. GBIF occurrence data for distribution and specimen discovery, not as stand-alone proof of anatomy.
6. Commercial nursery descriptions only as a last resort, labelled as commercial claims.

## Citation rules

- Every plant research record must have a dedicated **References** section with exact species pages, publications or specimen links, not just a generic database homepage.
- Record the source's taxon name as written, access date where relevant, and the specific claim it supports.
- Do not cite a database landing page as if it supports a detailed leaf, branching or flower claim.
- Keep conflicting taxonomic treatments visible and explain which treatment the profile follows.
- Separate observed source facts, cultivar-dependent variation and renderer assumptions.
- When no cultivar is named, use a clearly labelled species-level or representative-cultivar baseline. Never silently invent a cultivar.

## Closing research gaps without fabricating details

- Missing sources: find and cite an exact taxon page, flora treatment, monograph, extension publication or verified specimen.
- Missing cultivar: retain as a user-selectable variant; do not pretend the species has one fixed fruit colour, leaf shape or growth habit.
- Missing growth-stage information: define a stage sequence from documented ontogeny and cite the source; do not use a mature form as a seedling.
- Missing photographs: use verified herbarium/botanical-garden imagery as comparison material. Photographs are evidence, not templates to trace.
- Missing exact dimensions: use a documented range where available; otherwise omit dimensions and retain the uncertainty.
- Missing decline/death states: model only documented senescence features and label any generic seasonal decay as an illustrative state, not a diagnostic botanical fact.

## Guide-driven catalogue intake

- Treat every newly consulted botanical, horticultural or plant-identification guide as a catalogue-expansion opportunity. Extract **all distinct plant entries** in that guide, not only entries already identified as gaps or members of a fixed cohort.
- Reconcile each extracted entry against the existing taxonomy index, research records and infocards. Update an existing record when it is the same plant/profile; add a new taxon or horticultural profile when it is genuinely distinct. Preserve multiple cultivar or growth-form infocards linked to one species taxon where appropriate.
- Repeat this reconciliation for each guide. Catalogue completeness is cumulative across guides; do not treat the current gap list as a closed or exhaustive target.
- Every factual infocard field must be populated from appropriate botanical or horticultural evidence. User-provided preferences, selections or descriptions may identify which cultivar, growth form or developmental stage to research, but they are **not evidence** for botanical traits and must not be used to fill factual fields.
- For every populated field, retain trait-level provenance identifying the exact source and the claim it supports. Prefer primary botanical sources, regional floras, peer-reviewed treatments, verified specimens, botanical gardens and university extension publications according to the evidence hierarchy above.
- Do not infer a missing value from taxonomy, family resemblance, a generic guide summary or another species' profile. If adequate evidence is not found, retain `unknown` and record the research gap. Use `not_applicable` only when the field genuinely does not apply.
- Distinguish species-level facts from cultivar-specific, growth-form-specific and developmental-stage variation. Record supported variants and their sources rather than collapsing them into a single unsupported default.
- Guide inclusion alone does not authorize artwork generation. Catalogue and research work may proceed while the protected rendering gate remains in force.

## Project scope and rendering gate

The 57 existing plant infocards are the protected first cohort. They remain research-only until their source records and user-supplied cultivar/stage choices are reviewed and the user explicitly authorizes rendering. New plant profiles may be researched and added beyond this cohort, but their artwork must not cause the protected 57 to be rendered prematurely.
