# Sources and Evidence

## Three corpora

Keep three bodies of material distinct:

1. **Discovery corpus:** broad reading used to find anomalies, actors, periods, and possible mechanisms.
2. **Test corpus:** materials selected by an explicit protocol to evaluate focal and rival explanations.
3. **Context corpus:** background material used for chronology, institutions, and terminology but not treated as direct causal evidence.

The same item may move from discovery to testing only after its evidentiary role and independence are audited. Do not present evidence that generated a hypothesis as if it were a fully independent confirmation.

Before confirmation, freeze the coding rules, inclusion rules, outcome threshold, main claim, and rival predictions. Prefer a held-out subset, a new source family, a new archive, or new cases. Adding more examples from the same searched corpus is not independent confirmation. If no holdout or independent material is feasible, label the result exploratory and lower the claim.

## Source criticism record

Literature anchors: METH-SOURCE-001, METH-SOURCE-002, and METH-SOURCE-003; read their roles and limits in [Method-Evidence Map](method-evidence-map.md) before using the label.

For every material source, record:

- source ID, date, author or producing body, genre, and repository;
- public, restricted, missing, destroyed, translated, excerpted, or secondary-only access state;
- production context, intended audience, incentives, and censorship constraints;
- proximity to the event and whether the source is contemporaneous or retrospective;
- what the source directly observes, what it reports second-hand, and what the researcher infers;
- source family and likely dependence on other items;
- credibility concerns and corroboration status.

Use `source-register.csv` for individual records and `source-dependence-matrix.csv` for relationships.

## Source families and dependence

Ten documents repeating one communiqué may be one observation, not ten. Group items by shared origin, wire service, archive file, institutional reporting chain, interview network, or later citation lineage.

Corroboration is strongest when accounts differ in institutional origin, incentive, information path, and genre. Agreement inside one source family increases detail but not necessarily independence.

Trace possible common upstream origins even when items initially appear to belong to different families. Independence remains `unknown` until the relevant reporting, citation, translation, or briefing chain is checked.

Assess independence at the proposition level. A group of reports may independently establish that an event occurred while remaining dependent or non-diagnostic for its cause. Split compound claims such as `protest occurred`, `food prices rose`, and `participants acted because of food prices`; assign separate proposition IDs and source-family judgments to each.

## Observation, interpretation, and inference

Write each evidence entry in three layers:

- **Observation:** what the item explicitly contains or what was directly observed;
- **Interpretation:** the source meaning after contextual and linguistic analysis;
- **Inference:** how that interpretation bears on a claim or rival.

Do not silently convert a memoir's self-description, an official formula, or an interviewee's retrospective rationale into a fact about motives or causal effects.

## Evidence types are not fixed strengths

Documents, interviews, statistics, speeches, institutional rules, meeting records, budgets, personnel changes, media reports, material traces, and silence can all matter. Their strength depends on the hypothesis and the evidence-generating process.

Classify process evidence by what it tests:

- **Straw-in-the-wind:** modestly shifts plausibility but is neither necessary nor sufficient.
- **Hoop test:** absence seriously weakens a hypothesis; passage does not strongly confirm it.
- **Smoking-gun test:** presence strongly supports a hypothesis; absence may be unsurprising.
- **Doubly decisive test:** strongly supports one explanation while excluding major rivals; rare and must be defended.

Never assign a test label from vividness alone. State why the mechanism would generate the evidence and why rivals would not.

## Silence and missingness

Literature anchors: METH-SOURCE-001; read its role and limits in [Method-Evidence Map](method-evidence-map.md) before using the label.

An archive's silence is evidence only if the record-generating process made the item likely to be created, preserved, accessible, and found. Before using absence, ask:

1. Would the actor or institution normally create a record?
2. Would incentives favor recording the relevant fact honestly?
3. Would the record likely survive and be catalogued?
4. Did the search cover the correct collection, period, language, and aliases?
5. Could secrecy, destruction, informal action, or classification explain the silence?

If any link is unknown, record “not observed” rather than “did not occur.”

For every consequential silence claim, name at least two alternative source routes that would have different production incentives—for example private correspondence, diaries, personnel records, budget traces, local records, foreign reporting, oral history, or later investigations—and state what finding would raise or lower the silence's diagnostic value.

## Claim testing state and inferential strength

Every substantive claim receives a stable claim ID. Keep testing state separate from strength:

- testing state: `UNTESTED`, `PARTIALLY_TESTED`, `TESTED`, `CONTESTED`, or `OUT_OF_SCOPE`;
- inferential strength: `UNSUPPORTED`, `WEAK`, `NECESSARY_STEP_PASSED`, `STRONG_DIAGNOSTIC`, or `UNRESOLVED`.

One relevant observation can justify `WEAK` at most unless its diagnostic value is independently established. A central mechanism claim is aggregated through `observation -> proposition -> step -> mechanism -> bounded claim`; it cannot exceed its weakest necessary step. Record evidence IDs, rival implications, source ceilings, and the next discriminating search in `claim-register.csv` and `evidence-register.csv`.

## Fabrication and citation rules

- Never invent a quotation, page number, archive call number, interview, dataset value, DOI, author, or publication detail.
- Do not cite a source not inspected as though it were inspected.
- Label metadata-only records, abstracts, snippets, OCR, translations, and secondary quotations.
- Preserve conflicting dates or versions until the underlying record is resolved.
- If access fails, state the access failure and lower the conclusion ceiling.
- For current or unstable facts, verify against a primary or authoritative source before use.

When asked to fabricate or “temporarily” invent a citation, refuse the fabricated locator and provide a safe replacement package:

1. a visibly non-citable placeholder such as `[SOURCE NOT YET VERIFIED — DO NOT SUBMIT]`;
2. a search plan containing institutions, collection fields, date windows, actor aliases, and keywords without invented call numbers;
3. a verification checklist for full text, provenance, quotation, page or folio, translation, and claim relevance;
4. provisional wording that preserves uncertainty and stays below the evidence ceiling.

For a claim based only on a secondary abstract, snippet, or lost citation, the minimum verification set is: identify the original source, inspect the relevant full passage and context, verify the locator and translation, establish who made the statement and when, and test at least one alternative source route. If this cannot be completed, keep the claim `PENDING` or `UNSUPPORTED` and use it only as a hypothesis.
