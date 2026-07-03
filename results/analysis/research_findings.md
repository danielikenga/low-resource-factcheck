# Research Findings Log

## Dissertation Project

**Topic:** Retrieval-Augmented Misinformation Detection for Low-Resource Nigerian Languages

**Languages:** Hausa, Igbo, Yoruba

**Evaluation Test Set:** 492 examples

**Primary Labels:**
- supports
- refutes
- nei

---

# 1. Purpose of This Findings Log

This document records quantitative findings, qualitative observations, interpretation hypotheses, methodological caveats, and report-ready insights produced during the experimental evaluation.

The purpose is to preserve the analytical reasoning behind the dissertation results rather than relying only on final metric tables.

Interpretations recorded here should later be validated against the relevant experiment outputs before inclusion in the final dissertation.

---

# 2. Current Master Experimental Results

## 2.1 Encoder and LLM Results

| Experiment | Accuracy | Macro-F1 | Precision | Recall |
|---|---:|---:|---:|---:|
| XLM-R Claim Only | 0.346667 | 0.171617 | 0.115556 | 0.333333 |
| AfriBERTa Claim Only | 0.446154 | 0.418224 | 0.435362 | 0.436935 |
| AfriBERTa Custom Split | 0.497967 | 0.492296 | 0.491666 | 0.493279 |
| XLM-R Gold Evidence | 0.630081 | 0.589212 | 0.608706 | 0.617331 |
| AfriBERTa Gold Evidence | 0.571138 | 0.568683 | 0.576857 | 0.568618 |
| Qwen 1.5B Claim Only | 0.390244 | 0.380737 | 0.393998 | 0.389255 |
| Qwen 1.5B Gold Evidence | 0.459350 | 0.400397 | 0.525618 | 0.452344 |
| Qwen 1.5B Gold + Reasoning | 0.436992 | 0.425215 | 0.460196 | 0.433863 |
| Qwen 1.5B BM25 Evidence | 0.394309 | 0.318210 | 0.470052 | 0.392613 |
| Qwen 1.5B Adversarial Evidence | 0.333333 | 0.315591 | 0.349061 | 0.326094 |
| Qwen 14B Gold Evidence | 0.640244 | 0.600194 | 0.724721 | 0.624233 |
| Qwen 14B Few-shot (3) | 0.640244 | 0.595699 | 0.704338 | 0.625340 |
| Qwen 14B Few-shot (6) | 0.644309 | 0.592833 | 0.700043 | 0.629632 |
| Qwen 14B Few-shot (9) | 0.632114 | 0.582532 | 0.698087 | 0.618138 |
| Qwen 14B + Google Translate | 0.735772 | 0.733508 | 0.800859 | 0.729060 |
| Qwen 14B + Translate + Generic Examples | 0.621951 | 0.593794 | 0.795600 | 0.606069 |

---

# 3. Initial Cross-Experiment Findings

## 3.1 Evidence availability is a major performance factor

The encoder experiments show substantial improvements when gold evidence is available.

### XLM-R

Claim-only accuracy:

- 0.346667

Gold-evidence accuracy:

- 0.630081

Absolute improvement:

- +0.283414
- approximately +28.34 percentage points

Macro-F1 improves from:

- 0.171617
- to 0.589212

This is a very large increase.

### Interpretation

The result suggests that the verification task is strongly evidence-dependent. Claim-only classification provides insufficient information for reliable fact verification, whereas relevant evidence substantially improves classification.

This supports the dissertation's broader motivation for evidence-grounded and retrieval-augmented verification.

---

## 3.2 AfriBERTa also benefits from evidence

AfriBERTa Claim Only:

- Accuracy = 0.446154
- Macro-F1 = 0.418224

AfriBERTa Gold Evidence:

- Accuracy = 0.571138
- Macro-F1 = 0.568683

Absolute accuracy improvement:

- +0.124984
- approximately +12.50 percentage points

### Interpretation

Evidence improves both multilingual and African-focused encoder models.

However, the magnitude of improvement differs between architectures.

This may indicate differences in:
- pretrained multilingual representations,
- evidence utilisation,
- task adaptation,
- class decision boundaries.

Further interpretation should avoid claiming architectural causality without additional controlled experiments.

---

## 3.3 Custom splitting materially affects AfriBERTa performance

AfriBERTa Claim Only:

- Accuracy = 0.446154
- Macro-F1 = 0.418224

AfriBERTa Custom Split:

- Accuracy = 0.497967
- Macro-F1 = 0.492296

### Interpretation

The custom split improves performance relative to the initial claim-only baseline.

This indicates that evaluation design and dataset partitioning materially affect measured performance.

This is important for the methodology chapter because low-resource datasets can be particularly sensitive to:
- split composition,
- label distribution,
- language distribution,
- source overlap,
- topic distribution.

The exact mechanism should be interpreted only after confirming the construction of both splits.

---

# 4. Model Scale Findings

## 4.1 Qwen 14B substantially outperforms Qwen 1.5B with gold evidence

Qwen 1.5B Gold Evidence:

- Accuracy = 0.459350
- Macro-F1 = 0.400397

Qwen 14B Gold Evidence:

- Accuracy = 0.640244
- Macro-F1 = 0.600194

Absolute improvement:

- Accuracy: +0.180894
- Macro-F1: +0.199797

### Interpretation

The larger model demonstrates substantially stronger evidence-conditioned fact verification.

This suggests that model capacity is important for:
- multilingual semantic reasoning,
- claim-evidence alignment,
- contradiction detection,
- instruction following.

However, model size alone does not solve the task, as Qwen 14B still achieves only 64.02% accuracy on original-language gold evidence.

---

# 5. Few-Shot Prompting Findings

## 5.1 Few-shot prompting does not reliably improve Qwen 14B

Qwen 14B Gold Evidence baseline:

- Accuracy = 0.640244
- Macro-F1 = 0.600194

3-shot:

- Accuracy = 0.640244
- Macro-F1 = 0.595699

6-shot:

- Accuracy = 0.644309
- Macro-F1 = 0.592833

9-shot:

- Accuracy = 0.632114
- Macro-F1 = 0.582532

### Key observation

The highest few-shot accuracy is obtained with 6 examples:

- 0.644309

However, this is only a very small improvement over zero-shot gold evidence:

- 0.640244

At the same time, Macro-F1 declines.

The 9-shot configuration performs worse than the baseline.

### Interpretation

Increasing the number of demonstrations does not produce monotonic improvement.

Potential explanations include:
- prompt interference,
- demonstration mismatch,
- increased context complexity,
- label bias,
- poor transfer from examples to low-resource claim-evidence relations.

### Report-ready insight

More demonstrations are not automatically beneficial. In this experiment, additional few-shot examples produced diminishing and eventually negative returns.

---

# 6. Generic Prompt Examples After Translation

Translation-only Qwen 14B:

- Accuracy = 0.735772
- Macro-F1 = 0.733508

Translation + Generic Prompt Examples:

- Accuracy = 0.621951
- Macro-F1 = 0.593794

Absolute change:

- Accuracy = -0.113821
- Macro-F1 = -0.139714

### Interpretation

Generic examples substantially reduce performance.

This is a major negative result and should be reported rather than hidden.

The likely explanation is that generic demonstrations introduce a mismatch between:
- simplified demonstration patterns,
- real Afrifact examples,
- culturally specific entities,
- noisy evidence,
- complex multilingual relations.

### Report-ready insight

Prompt demonstrations can be harmful when they are not distributionally aligned with the target task.

This result complements the earlier few-shot experiments and suggests that prompt-example quality and task alignment are more important than simply increasing the number of demonstrations.

---

# 7. BM25 Retrieval Findings

## 7.1 Retrieval metrics

BM25 retrieval evaluation over 492 test queries produced:

- Recall@1 = 0.197154
- Recall@3 = 0.481707
- Recall@5 = 0.573171
- Recall@10 = 0.628049

### Interpretation

The correct evidence is retrieved at rank 1 for only approximately 19.72% of queries.

However, recall rises substantially as the retrieval depth increases:

- approximately 48.17% by top 3,
- approximately 57.32% by top 5,
- approximately 62.80% by top 10.

### Key retrieval insight

BM25 often retrieves the correct evidence somewhere in the candidate set but struggles to rank it first.

This suggests a potential distinction between:
- candidate generation,
- candidate ranking.

### Report-ready insight

The retrieval bottleneck is not simply total failure to retrieve relevant evidence. A substantial proportion of relevant evidence appears within deeper candidate sets, suggesting that reranking may be a promising future direction.

---

# 8. End-to-End BM25 Evidence Verification

Qwen 1.5B Gold Evidence:

- Accuracy = 0.459350
- Macro-F1 = 0.400397

Qwen 1.5B BM25 Evidence:

- Accuracy = 0.394309
- Macro-F1 = 0.318210

### Interpretation

Replacing oracle gold evidence with BM25-retrieved evidence reduces verification performance.

This demonstrates an oracle-to-retrieved evidence gap.

The result suggests that retrieval quality directly constrains downstream fact verification.

### Important dissertation interpretation

Gold-evidence experiments measure verification capability under oracle evidence access.

BM25 experiments measure a more realistic retrieval-augmented pipeline.

The performance difference quantifies part of the cost introduced by imperfect evidence retrieval.

---

# 9. Adversarial Evidence Findings

Qwen 1.5B Gold Evidence:

- Accuracy = 0.459350
- Macro-F1 = 0.400397

Qwen 1.5B Adversarial Evidence:

- Accuracy = 0.333333
- Macro-F1 = 0.315591

### Interpretation

Performance degrades under adversarial evidence.

Accuracy reaches approximately one-third, which is especially notable in a three-class task.

This indicates sensitivity to misleading or mismatched evidence.

### Report-ready insight

Evidence grounding is beneficial only when evidence quality is reliable. Supplying misleading evidence can substantially degrade model decisions.

This supports a broader argument that retrieval-augmented fact checking requires both:
- retrieval relevance,
- robustness to misleading context.

---

# 10. Translation Experiment

## 10.1 Overall result

Qwen 14B Original Gold Evidence:

- Accuracy = 0.640244
- Macro-F1 = 0.600194

Qwen 14B Translated Gold Evidence:

- Accuracy = 0.735772
- Macro-F1 = 0.733508

Absolute accuracy improvement:

- +0.095528
- approximately +9.55 percentage points

Absolute Macro-F1 improvement:

- +0.133314
- approximately +13.33 percentage points

### Interpretation

Translation into English produces the strongest overall result among the current experiments.

However, subsequent analysis shows that this gain is highly non-uniform.

Translation should therefore not be described as a universally beneficial preprocessing step.

---

# 11. Translation Effect by Language

| Language | Examples | Original Accuracy | Translated Accuracy | Absolute Change |
|---|---:|---:|---:|---:|
| Igbo | 163 | 0.607362 | 0.742331 | +0.134969 |
| Hausa | 166 | 0.650602 | 0.759036 | +0.108434 |
| Yoruba | 163 | 0.662577 | 0.705521 | +0.042945 |

## 11.1 Igbo

Improvement:

- +13.50 percentage points

This is the largest overall language-level gain.

## 11.2 Hausa

Improvement:

- +10.84 percentage points

## 11.3 Yoruba

Improvement:

- +4.29 percentage points

This is positive overall but substantially smaller than the improvements for Igbo and Hausa.

### Interpretation

Translation benefits are language-dependent.

The later language-label interaction analysis shows that Yoruba's smaller aggregate improvement masks a severe decline for supported claims.

---

# 12. Translation Effect by Gold Label

| Gold Label | Examples | Original Accuracy | Translated Accuracy | Absolute Change |
|---|---:|---:|---:|---:|
| supports | 166 | 0.668675 | 0.602410 | -0.066265 |
| refutes | 152 | 0.250000 | 0.625000 | +0.375000 |
| nei | 174 | 0.954023 | 0.959770 | +0.005747 |

## 12.1 Major result: contradiction detection improves dramatically

Refutes accuracy increases from:

- 25.00%
- to 62.50%

Absolute improvement:

- +37.50 percentage points

This is the dominant source of translation improvement.

## 12.2 Supports performance declines

Supports accuracy decreases from:

- 66.87%
- to 60.24%

Absolute decline:

- -6.63 percentage points

## 12.3 NEI remains extremely strong

NEI accuracy changes only slightly:

- 95.40%
- to 95.98%

### Central interpretation

Translation acts asymmetrically across fact-verification relations.

It strongly improves contradiction recognition while slightly damaging entailment recognition.

This is one of the strongest findings of the dissertation.

---

# 13. Translation Transition Analysis

Across 492 examples:

| Transition | Count | Percentage |
|---|---:|---:|
| correct_to_correct | 268 | 54.47% |
| wrong_to_correct | 94 | 19.11% |
| wrong_to_wrong | 83 | 16.87% |
| correct_to_wrong | 47 | 9.55% |

## Interpretation

Translation repairs:

- 94 previously incorrect examples

Translation damages:

- 47 previously correct examples

Net improvement:

- +47 correct predictions

This exactly corresponds to the overall accuracy increase:

- 47 / 492 = approximately 9.55 percentage points

### Report-ready insight

Translation is a net-positive but lossy transformation. It repairs twice as many decisions as it damages, yet the 47 regressions demonstrate that translation introduces meaningful semantic risk.

---

# 14. Translation Transitions by Language

## Hausa

- correct_to_correct = 100
- correct_to_wrong = 8
- wrong_to_correct = 26
- wrong_to_wrong = 32

Net repaired decisions:

- 26 - 8 = +18

## Igbo

- correct_to_correct = 81
- correct_to_wrong = 18
- wrong_to_correct = 40
- wrong_to_wrong = 24

Net repaired decisions:

- 40 - 18 = +22

## Yoruba

- correct_to_correct = 87
- correct_to_wrong = 21
- wrong_to_correct = 28
- wrong_to_wrong = 27

Net repaired decisions:

- 28 - 21 = +7

### Interpretation

Igbo receives the largest net benefit.

Yoruba has the weakest net gain because translation repairs 28 errors but introduces 21 new errors.

This explains why Yoruba's aggregate improvement is substantially smaller.

---

# 15. Translation Transitions by Label

## NEI

- correct_to_correct = 162
- correct_to_wrong = 4
- wrong_to_correct = 5
- wrong_to_wrong = 3

Net change:

- +1

## Refutes

- correct_to_correct = 31
- correct_to_wrong = 7
- wrong_to_correct = 64
- wrong_to_wrong = 50

Net change:

- +57

## Supports

- correct_to_correct = 75
- correct_to_wrong = 36
- wrong_to_correct = 25
- wrong_to_wrong = 30

Net change:

- -11

### Central finding

Almost the entire net translation improvement is driven by refutes examples.

Translation creates:

- +57 net correct refutes decisions

but:

- -11 net supports decisions

and:

- +1 net NEI decision

Total:

- +47 net correct predictions

### Report-ready interpretation

The overall translation gain should not be interpreted as uniform multilingual improvement. It is primarily a contradiction-detection effect.

---

# 16. Language × Label Interaction

| Language | Label | Examples | Original Accuracy | Translated Accuracy | Absolute Change |
|---|---|---:|---:|---:|---:|
| Hausa | NEI | 67 | 0.970149 | 0.940299 | -0.029851 |
| Hausa | Refutes | 43 | 0.255814 | 0.627907 | +0.372093 |
| Hausa | Supports | 56 | 0.571429 | 0.642857 | +0.071429 |
| Igbo | NEI | 53 | 0.962264 | 0.962264 | 0.000000 |
| Igbo | Refutes | 55 | 0.290909 | 0.690909 | +0.400000 |
| Igbo | Supports | 55 | 0.581818 | 0.581818 | 0.000000 |
| Yoruba | NEI | 54 | 0.925926 | 0.981481 | +0.055556 |
| Yoruba | Refutes | 54 | 0.203704 | 0.555556 | +0.351852 |
| Yoruba | Supports | 55 | 0.854545 | 0.581818 | -0.272727 |

## Major interaction finding

Translation improves refutes accuracy for every language:

- Hausa: +37.21 percentage points
- Igbo: +40.00 percentage points
- Yoruba: +35.19 percentage points

This is a highly consistent cross-language pattern.

## Major anomaly

Yoruba supports accuracy decreases from:

- 85.45%
- to 58.18%

Absolute decline:

- -27.27 percentage points

### Interpretation

The weak overall Yoruba translation gain is not because translation fails uniformly on Yoruba.

Instead:
- Yoruba refutes improves strongly,
- Yoruba NEI improves,
- Yoruba supports collapses.

This interaction is substantially more informative than aggregate language accuracy alone.

---

# 17. Confusion Matrix Findings

## 17.1 Original-language Qwen 14B

| Gold Label | Pred Supports | Pred Refutes | Pred NEI |
|---|---:|---:|---:|
| Supports | 111 | 2 | 53 |
| Refutes | 27 | 38 | 87 |
| NEI | 3 | 5 | 166 |

### Key observation

The major original-language weakness is refutes detection.

Among 152 refutes examples:

- only 38 are correctly classified as refutes,
- 87 are incorrectly classified as NEI,
- 27 are incorrectly classified as supports.

The dominant error is therefore:

- refutes → NEI

## 17.2 Translated Qwen 14B

| Gold Label | Pred Supports | Pred Refutes | Pred NEI |
|---|---:|---:|---:|
| Supports | 100 | 13 | 53 |
| Refutes | 3 | 95 | 54 |
| NEI | 2 | 5 | 167 |

### Key observation

After translation:

- correct refutes predictions increase from 38 to 95,
- refutes → supports errors fall from 27 to 3,
- refutes → NEI errors fall from 87 to 54.

However:

- supports → refutes errors increase from 2 to 13.

### Interpretation

Translation substantially improves contradiction recognition but also shifts some supported claims toward false contradiction decisions.

---

# 18. Qualitative Translation Case Analysis

## 18.1 Method

Representative cases were selected systematically rather than manually cherry-picked.

Target groups:

1. Refutes examples changing from wrong to correct.
2. Yoruba supports examples changing from correct to wrong.

Representative examples were selected using fixed text-length quantiles.

This selection strategy provides examples across a range of input lengths and reduces subjective case selection.

The cases should be described as illustrative error patterns rather than proof that every transition has the same cause.

---

# 19. Translation Repair Mechanisms

## 19.1 Ordinal contradiction exposure

### Example ID

`afrifact_data_culture_igbo_013`

### Transition

- Original prediction: NEI
- Translated prediction: refutes

### Claim relation

Claim:

- Bianca Ojukwu was the second female head of the Nigerian Stock Exchange.

Evidence:

- She was the first woman to hold the position.

### Interpretation

Translation exposes an explicit ordinal contradiction:

- second
- versus first

### Hypothesised mechanism

Improved accessibility of ordinal semantics enables the model to recognise contradiction.

---

## 19.2 Event-role and predicate contradiction exposure

### Example ID

`afrifact_data_culture_hausa_169`

### Transition

- Original prediction: supports
- Translated prediction: refutes

### Claim relation

Claim:

- Governor Shema received an honour award from EFCC.

Evidence:

- EFCC prosecuted Governor Shema over alleged corruption involving approximately ₦11 billion.

### Interpretation

The translated text makes the event-role contradiction explicit:

- honoured by institution
- versus prosecuted by institution

### Hypothesised mechanism

Translation improves access to event predicates and institutional role relations.

---

## 19.3 Entity mismatch exposure

### Example ID

`afrifact_data_culture_yoruba_149`

### Transition

- Original prediction: NEI
- Translated prediction: refutes

### Claim relation

Claim attributes a promise to:

- Dauda / David

Evidence concerns:

- Ibrahim

### Interpretation

Translation makes the entity mismatch easier to detect.

### Hypothesised mechanism

Improved entity-role discrimination after translation.

---

## 19.4 Explicit detention contradiction

### Example ID

`afrifact_data_culture_yoruba_200`

### Transition

- Original prediction: NEI
- Translated prediction: refutes

### Claim relation

Claim states that no EndSARS protesters were arrested.

Evidence discusses detainees and individuals in police custody.

### Interpretation

Translation exposes lexical relations around:

- arrested,
- detainees,
- police custody.

### Hypothesised mechanism

Improved recognition of semantically related detention concepts.

### Caveat

The translated numerical wording is visibly noisy and should not be treated as a clean translation example.

---

# 20. Translation Damage Mechanisms

## 20.1 Numerical and ranking corruption

### Example ID

`afrifact_data_culture_yoruba_624`

### Transition

- Original prediction: supports
- Translated prediction: NEI

### Original relation

The claim describes Ondo State as the 19th most populous state.

The original evidence supports the ranking relation.

### Translation problem

The translated evidence states:

- 11th largest state

instead of preserving the original population ranking.

### Interpretation

Translation changes:
- the numerical rank,
- and potentially the measured property.

### Mechanism

Numerical/ranking semantic corruption.

### Significance

This demonstrates that translation can alter factual content rather than merely surface form.

---

## 20.2 Culturally specific lexical mistranslation

### Example ID

`afrifact_data_culture_yoruba_555`

### Transition

- Original prediction: supports
- Translated prediction: NEI

### Original concept

- gaàrí

### Translation problem

The translated claim renders gaàrí as:

- sugar

This changes the entity from a culturally specific cassava food product into an unrelated English concept.

### Mechanism

Culturally grounded lexical ambiguity and mistranslation.

### Significance

This is particularly important for low-resource African-language NLP because culturally specific vocabulary may not map reliably into generic English lexical categories.

---

## 20.3 Predicate-level proposition corruption

### Example ID

`afrifact_data_culture_yoruba_358`

### Transition

- Original prediction: supports
- Translated prediction: refutes

### Original meaning

The claim concerns global breastfeeding and the number of lives that could be saved.

### Translation problem

The translated claim states:

- "if the entire world community donates a child"

This corrupts the central predicate.

### Mechanism

Proposition-level predicate mistranslation.

### Significance

The model is no longer verifying the same proposition after translation.

This is a direct example of translation-induced label instability.

---

## 20.4 Domain-specific semantic distortion

### Example ID

`afrifact_data_culture_yoruba_168`

### Transition

- Original prediction: supports
- Translated prediction: NEI

### Translation problem

A football positional description becomes:

- "back-handed footballer"

### Mechanism

Domain-specific terminology is translated into semantically malformed English.

### Caveat

The provided evidence excerpt may itself be incomplete for the full claim.

Therefore, this case should be treated as suggestive rather than definitive proof that translation alone caused the failure.

---

## 20.5 Possible translation-amplified claim mismatch

### Example ID

`afrifact_data_culture_yoruba_528`

### Transition

- Original prediction: supports
- Translated prediction: NEI

### Observation

The translated claim states that Wizkid is:

- "one of the best Afro Beat musicians"

The translated evidence discusses:
- Afro Beats,
- Wizkid,
- his early musical career.

However, the evidence does not clearly establish the stronger evaluative phrase:

- "one of the best"

### Interpretation

Translation may strengthen or alter the proposition in a way that reduces direct entailment.

### Caveat

The original example may also contain annotation noise or imperfect evidence alignment.

This case should therefore be described as a possible translation-amplified mismatch rather than definitive translation corruption.

---

# 21. Integrated Translation Interpretation

## Central finding

Translation is not a uniformly beneficial preprocessing operation.

Instead, it behaves as a task-dependent semantic intervention.

### Benefits

Translation substantially improves:
- contradiction recognition,
- ordinal mismatch detection,
- entity mismatch detection,
- event-role contradiction recognition.

### Risks

Translation can introduce:
- culturally specific lexical mistranslation,
- numerical corruption,
- ranking corruption,
- predicate corruption,
- domain-specific terminology distortion,
- proposition strengthening or semantic drift.

### Strong report-ready statement

Translation substantially improved overall Qwen 14B verification performance, but the gain was highly asymmetric. The improvement was driven primarily by refuted claims, whose accuracy increased from 25.0% to 62.5% across consistent gains in Hausa, Igbo, and Yoruba. Conversely, supported claims declined overall, with Yoruba supports falling by 27.27 percentage points. Qualitative inspection linked successful repairs to clearer ordinal, entity, and event-role contradictions, while regressions were associated with mistranslated culturally specific terms, altered numerical semantics, and proposition-level predicate corruption.

---

# 22. Methodological Caveats for Translation Analysis

The following caveats must be retained in the final dissertation.

## 22.1 Translation cases are illustrative

Representative cases demonstrate plausible mechanisms but do not prove that all transitions share the same cause.

## 22.2 Translation quality was not manually annotated for all 492 examples

Therefore, causal claims about translation errors should remain appropriately qualified.

Recommended language:

- "qualitative inspection suggests"
- "illustrative cases indicate"
- "errors were consistent with"
- "a plausible mechanism is"

Avoid:

- "translation caused every error"
- "all Yoruba failures resulted from mistranslation"

## 22.3 Dataset noise may interact with translation

Some examples may contain:
- imperfect evidence spans,
- annotation noise,
- malformed source text,
- incomplete context.

Therefore, translation and dataset quality may jointly influence outcomes.

## 22.4 Free translation tooling

The translation experiment uses a free translation-library route rather than a paid enterprise translation API.

The exact translation implementation, library, access method, and reproducibility limitations must be documented accurately in the methodology chapter.

---

# 23. Current Strongest Dissertation Findings

At the current stage, the strongest findings are:

1. Gold evidence dramatically improves encoder verification, particularly for XLM-R.

2. Larger model scale substantially improves evidence-conditioned verification.

3. Few-shot prompting does not produce monotonic gains and can reduce Macro-F1.

4. Generic prompt demonstrations substantially damage translated Qwen 14B performance.

5. BM25 retrieval recall rises strongly with retrieval depth but top-1 recall remains low.

6. Retrieved evidence underperforms oracle gold evidence, demonstrating an oracle-to-retrieved evidence gap.

7. Adversarial evidence reduces performance to approximately one-third accuracy.

8. Translation produces the strongest current overall result.

9. Translation improvement is primarily a contradiction-detection effect rather than uniform multilingual improvement.

10. Translation improves refutes accuracy consistently across Hausa, Igbo, and Yoruba.

11. Yoruba supported claims experience a severe translation-related degradation.

12. Qualitative analysis identifies plausible semantic repair and corruption mechanisms.

---

# 24. Future Analysis Queue

The following analyses remain to be completed.

## 24.1 Cross-experiment error analysis

Planned:
- encoder error analysis,
- Qwen 1.5B error analysis,
- Qwen 14B error analysis,
- few-shot error analysis,
- BM25 pipeline error analysis,
- adversarial evidence error analysis,
- generic prompt example error analysis.

## 24.2 Retrieval analysis

Planned:
- retrieval success versus downstream correctness,
- top-k retrieval depth analysis,
- cases where correct evidence is retrieved but verification fails,
- cases where retrieval fails but prediction is correct,
- potential language differences in retrieval.

## 24.3 Model comparison analysis

Planned:
- agreement/disagreement across models,
- examples solved only by larger models,
- examples solved by encoders but not LLMs,
- examples consistently difficult across architectures.

## 24.4 Statistical testing

Consider:
- paired significance testing for original versus translated predictions,
- bootstrap confidence intervals,
- McNemar's test for paired classification outcomes.

These should be implemented where methodologically appropriate.

---

# 25. Reporting Principle

The final dissertation should not present experiments as isolated leaderboard rows.

The analysis should connect:

- evidence availability,
- retrieval quality,
- model scale,
- prompting strategy,
- translation,
- adversarial robustness,
- language-specific effects,
- label-specific effects,
- qualitative error mechanisms.

The central research narrative should explain not only:

- which system performs best,

but also:

- why performance changes,
- where systems fail,
- which components create bottlenecks,
- how low-resource multilingual conditions affect evidence-grounded fact verification.
---

# Cross-Experiment Error Analysis and Final Synthesis

## Purpose of the analysis

A cross-experiment error analysis was conducted to move beyond aggregate performance metrics and determine how different interventions changed model behaviour at the individual-example level. The analysis compared six principal systems:

- Qwen 1.5B Claim Only
- Qwen 1.5B Gold Evidence
- Qwen 1.5B BM25 Evidence
- Qwen 1.5B Adversarial Evidence
- Qwen 14B Gold Evidence
- Qwen 14B Translated Gold Evidence

All six systems were compared over the same 492-example evaluation set, enabling matched example-level transition analysis.

The analysis addressed four main questions:

1. How much does access to evidence improve over claim-only classification?
2. Does automatically retrieved BM25 evidence reproduce the benefit of oracle gold evidence?
3. How vulnerable is fact verification to misleading or adversarial evidence?
4. How do model scale and translation affect the correction and introduction of errors?

---

## 1. Overall performance hierarchy

The six principal systems ranked as follows by accuracy:

| Rank | Experiment | Accuracy |
|---|---|---:|
| 1 | Qwen 14B Translated Gold Evidence | 0.735772 |
| 2 | Qwen 14B Gold Evidence | 0.640244 |
| 3 | Qwen 1.5B Gold Evidence | 0.459350 |
| 4 | Qwen 1.5B BM25 Evidence | 0.394309 |
| 5 | Qwen 1.5B Claim Only | 0.390244 |
| 6 | Qwen 1.5B Adversarial Evidence | 0.333333 |

### Interpretation

The ranking indicates that performance is governed by more than the mere presence of evidence. Three factors emerge as particularly important:

- model capacity;
- evidence quality;
- linguistic accessibility of the input.

The strongest result was obtained by translating low-resource-language claims and evidence before classification with Qwen 14B. This suggests that a capable multilingual LLM may still possess substantially stronger verification competence when semantically equivalent content is presented in a higher-resource language representation.

The weak BM25 and adversarial results demonstrate that evidence-conditioned fact verification is highly sensitive to the relevance and reliability of the supplied context. Retrieval is therefore not automatically beneficial.

---

## 2. Evidence access: claim-only to gold evidence

Transition from Qwen 1.5B Claim Only to Qwen 1.5B Gold Evidence produced:

- correct to correct: 74
- wrong to correct: 152
- correct to wrong: 118
- wrong to wrong: 148
- net correct gain: +34

Accuracy increased from 0.390244 to 0.459350.

### Interpretation

Gold evidence improved aggregate accuracy, but the matched transition analysis reveals substantial instability. Although 152 previously incorrect examples were repaired, 118 previously correct examples became incorrect after evidence was introduced.

This is important because aggregate accuracy alone hides the fact that evidence can both repair and damage predictions. The 1.5B model appears unable to exploit evidence consistently. It may be influenced by lexical overlap, partial semantic cues, or misleading details within longer contexts.

Therefore, the finding is not simply that evidence improves performance. A more accurate conclusion is:

> Relevant evidence provides useful verification signal, but smaller language models may lack sufficient reasoning capacity to use that signal reliably.

---

## 3. Gold evidence versus BM25 retrieval

Transition from Qwen 1.5B Gold Evidence to Qwen 1.5B BM25 Evidence produced:

- correct to correct: 171
- wrong to correct: 23
- correct to wrong: 55
- wrong to wrong: 243
- net correct gain: -32

Accuracy fell from 0.459350 with gold evidence to 0.394309 with BM25 evidence.

### Interpretation

Replacing oracle gold evidence with top-ranked BM25 retrieval caused a net loss of 32 correct predictions.

Only 23 previously wrong examples were repaired by BM25 retrieval, whereas 55 previously correct examples were damaged. This indicates a clear retrieval bottleneck.

The result demonstrates that a retrieval-augmented fact-checking pipeline can underperform an oracle-evidence system because retrieval quality constrains downstream classification. Even when the classifier is unchanged, substituting imperfect retrieved evidence for gold evidence materially changes the prediction outcome.

This supports a central dissertation argument:

> Retrieval-augmented misinformation detection is constrained not only by classifier capability but by whether the retriever supplies evidence that is genuinely discriminative for verification.

---

## 4. BM25 support bias

The Qwen 1.5B BM25 system displayed a strong prediction bias:

- supports: 394 predictions (80.08%)
- refutes: 69 predictions (14.02%)
- NEI: 29 predictions (5.89%)

A dedicated case analysis identified 245 BM25 support-bias failures:

- 126 gold NEI examples
- 119 gold refutes examples

By language:

- Igbo: 87
- Yoruba: 83
- Hausa: 75

### Interpretation

This is one of the strongest behavioural findings in the dissertation.

The BM25 system did not merely perform poorly in a random manner. It overwhelmingly predicted `supports`, assigning this label to more than four-fifths of the evaluation set.

A plausible mechanism is lexical-overlap bias. BM25 retrieves passages using term overlap rather than contradiction-aware semantic reasoning. Consequently, retrieved passages may share entities, topics, or surface vocabulary with a claim without actually supporting it.

When such topically related evidence is passed to the LLM, the classifier may interpret relevance as entailment.

This suggests the following failure chain:

1. BM25 rewards lexical similarity.
2. Lexically similar evidence is retrieved.
3. The evidence appears topically relevant.
4. The LLM over-interprets relevance as support.
5. Refuted and insufficient-information claims are incorrectly classified as `supports`.

The result provides an important distinction between:

- retrieval relevance;
- verification usefulness.

A passage can be relevant to a claim while still being insufficient for determining whether the claim is true or false.

---

## 5. Adversarial evidence damage

Transition from Qwen 1.5B Gold Evidence to Qwen 1.5B Adversarial Evidence produced:

- correct to correct: 89
- wrong to correct: 75
- correct to wrong: 137
- wrong to wrong: 191
- net correct gain: -62

Accuracy fell from 0.459350 to 0.333333.

A total of 137 examples that were correct under gold evidence became wrong under adversarial evidence.

### Interpretation

The adversarial condition produced the largest negative net transition among the analysed interventions.

The result demonstrates that evidence-conditioned fact verification systems can be highly vulnerable to misleading context. A model that produces a correct decision when given appropriate evidence may reverse that decision when exposed to plausible but unsuitable evidence.

This has direct implications for real-world RAG systems. Retrieval pipelines operating over noisy web corpora may encounter:

- irrelevant passages;
- outdated information;
- misleading context;
- contradictory sources;
- semantically related but non-verifying evidence.

Therefore, retrieval quality should be considered a reliability and robustness problem rather than merely a search-performance problem.

A key dissertation interpretation is:

> In retrieval-augmented fact verification, poor evidence can be worse than no evidence.

This conclusion is supported by the adversarial system's accuracy of 0.333333, which was below the claim-only system's 0.390244.

---

## 6. Effect of model scaling

Transition from Qwen 1.5B Gold Evidence to Qwen 14B Gold Evidence produced:

- correct to correct: 169
- wrong to correct: 146
- correct to wrong: 57
- wrong to wrong: 120
- net correct gain: +89

Accuracy increased from 0.459350 to 0.640244.

### Interpretation

Model scaling produced the largest positive net gain among the matched pairwise interventions.

The 14B model repaired 146 errors made by the 1.5B model while introducing only 57 regressions, yielding a net gain of 89 correct examples.

This provides strong evidence that model capacity materially affects low-resource fact verification even when the evidence condition remains constant.

The larger model may benefit from:

- stronger multilingual representations;
- improved contextual reasoning;
- better entity and relation tracking;
- stronger contradiction recognition;
- more robust instruction following.

However, 120 examples remained wrong under both 1.5B and 14B gold-evidence conditions. Scaling therefore substantially improves performance but does not eliminate systematic failure.

---

## 7. Translation as a model-access intervention

Transition from Qwen 14B Gold Evidence to Qwen 14B Translated Gold Evidence produced:

- correct to correct: 268
- wrong to correct: 94
- correct to wrong: 47
- wrong to wrong: 83
- net correct gain: +47

Accuracy increased from:

- original low-resource input: 0.640244
- translated English input: 0.735772

Absolute accuracy gain:

- +0.095528
- approximately +9.55 percentage points

Macro F1 increased from:

- 0.600194
- to 0.733508

### Interpretation

Translation produced a substantial improvement even though the underlying factual task remained unchanged.

The same model was used before and after translation. Therefore, the improvement cannot be attributed to increased model size. Instead, the result indicates that the language in which information is presented materially affects the model's ability to reason over evidence.

A central interpretation is:

> Translation functions as a model-access intervention, mapping low-resource-language content into a linguistic representation in which the LLM can use its reasoning capabilities more effectively.

This does not imply that translation universally improves every example. The transition analysis showed 47 correct-to-wrong regressions. Translation is therefore beneficial overall but non-uniform.

---

## 8. Translation effect by language

Per-language accuracy changed as follows:

| Language | Examples | Original Accuracy | Translated Accuracy | Absolute Change |
|---|---:|---:|---:|---:|
| Igbo | 163 | 0.607362 | 0.742331 | +0.134969 |
| Hausa | 166 | 0.650602 | 0.759036 | +0.108434 |
| Yoruba | 163 | 0.662577 | 0.705521 | +0.042945 |

### Interpretation

Translation improved overall performance in all three languages, but the magnitude varied substantially.

The largest gain occurred for Igbo:

- +13.50 percentage points

Hausa improved by:

- +10.84 percentage points

Yoruba improved by only:

- +4.29 percentage points

This demonstrates that translation should not be treated as a uniform preprocessing intervention. Its effect is language-dependent.

The smaller Yoruba gain later proved especially important because class-specific analysis revealed substantial damage to Yoruba `supports` examples.

---

## 9. Translation effect by verification label

Per-label accuracy changed as follows:

| Gold Label | Examples | Original Accuracy | Translated Accuracy | Absolute Change |
|---|---:|---:|---:|---:|
| supports | 166 | 0.668675 | 0.602410 | -0.066265 |
| refutes | 152 | 0.250000 | 0.625000 | +0.375000 |
| NEI | 174 | 0.954023 | 0.959770 | +0.005747 |

### Interpretation

The overall translation gain was driven primarily by contradiction recognition.

For `refutes`, accuracy increased from 25.00% to 62.50%:

- +37.50 percentage points

By contrast:

- `supports` declined by 6.63 percentage points;
- `NEI` remained almost unchanged.

This is a major result because it shows that the 9.55-point overall gain was not a uniform improvement across classes.

The translated representation appears particularly effective at exposing contradictions that the model previously failed to recognise.

---

## 10. Translation and the refutes class

Translation repaired 64 `refutes` examples that were previously wrong.

Per-language `refutes` changes were:

| Language | Original Accuracy | Translated Accuracy | Change |
|---|---:|---:|---:|
| Hausa | 0.255814 | 0.627907 | +0.372094 |
| Igbo | 0.290909 | 0.690909 | +0.400000 |
| Yoruba | 0.203704 | 0.555556 | +0.351852 |

### Interpretation

The improvement in contradiction recognition was not isolated to one language.

Refutes accuracy increased by:

- +40.00 percentage points for Igbo;
- +37.21 percentage points for Hausa;
- +35.19 percentage points for Yoruba.

This cross-language consistency strengthens the interpretation that translation improves the model's access to contradiction cues.

The original model frequently mapped refuted claims to NEI, suggesting that it failed to recognise the semantic relationship required for contradiction. Translation often converted these uncertain decisions into correct refutations.

---

## 11. Representative translation repair cases

### Igbo: first versus second

Claim:

> Bianca Ojukwu is the second female CEO of the Nigerian Stock Exchange.

Evidence:

> She is the first woman to hold a position as the head of the Nigerian Stock Exchange.

Prediction changed:

- original: NEI
- translated: refutes

### Interpretation

Translation exposed a direct ordinal contradiction between `second` and `first`.

---

### Hausa: award versus prosecution

Claim:

> Governor Shema received an award of honor from the EFCC.

Evidence:

> The EFCC prosecuted Governor Shema on corruption charges involving approximately N11 billion.

Prediction changed:

- original: supports
- translated: refutes

### Interpretation

The translated representation made the relation between the entity and the EFCC clearer. The evidence described prosecution rather than an honour or award.

---

### Yoruba: Dauda versus Ibrahim

Claim:

> God made a promise to Dauda that if she had a child, she would worship him.

Evidence referred to Ibrahim and the dedication of a child to God.

Prediction changed:

- original: NEI
- translated: refutes

### Interpretation

Translation exposed an entity mismatch between Dauda and Ibrahim.

---

## 12. Translation damage and Yoruba supports examples

Despite the overall translation improvement, Yoruba `supports` accuracy fell from:

- 0.854545
- to 0.581818

Absolute change:

- -0.272727
- approximately -27.27 percentage points

A dedicated case extraction identified 20 Yoruba `supports` examples that changed from correct to incorrect after translation.

### Interpretation

This is a critical counter-result.

Translation is not a universally safe preprocessing step. In some cases it introduces semantic distortion severe enough to reverse correct predictions.

The Yoruba result prevents an overly simplistic conclusion that English translation always improves low-resource verification.

A more defensible conclusion is:

> Translation provides a strong average benefit but can introduce language-specific semantic corruption.

---

## 13. Representative translation damage cases

### Ondo State ranking distortion

Original claim stated that Ondo was the 19th most populous state.

Translated claim preserved:

> 19th most populous state

However, translated evidence changed the relevant statement to:

> 11th largest state

The model changed:

- supports
- to NEI

### Interpretation

A numerical/ranking translation error destroyed the original entailment relation.

---

### Gaari mistranslated as sugar

Original claim concerned:

- white gaari
- yellow gaari

Translated claim became:

> White sugar and brown sugar are two types of sugar found in western Nigeria.

### Interpretation

The culturally specific food term `gaari` was incorrectly translated into `sugar`, changing the subject of the claim.

---

### Breastfeeding semantic corruption

The Yoruba statement concerning breastfeeding and lives saved was translated into language resembling:

> if the entire world community donates a child...

### Interpretation

A major semantic translation error corrupted the core proposition and damaged verification.

---

## 14. Generic prompt examples after translation

The translated Qwen 14B baseline achieved:

- accuracy: 0.735772
- macro F1: 0.733508

Adding generic prompt examples reduced performance to:

- accuracy: 0.621951
- macro F1: 0.593794

### Interpretation

Generic examples were actively harmful.

This is an important negative result. Prompt examples are not automatically beneficial, even when they appear logically clear and task-relevant.

A plausible explanation is that generic demonstrations introduced an artificial decision pattern that did not align with the distributional characteristics of the Afrifact evaluation data.

The demonstrations may have:

- shifted the model's decision boundary;
- encouraged superficial analogy;
- interfered with dataset-specific evidence interpretation;
- imposed generic verification patterns that did not transfer to culturally and linguistically specific claims.

The finding supports the conclusion that:

> Few-shot or demonstration-based prompting should be evaluated empirically rather than assumed to improve performance.

---

# Cross-System Behavioural Analysis

## 15. Prediction distributions reveal distinct system biases

Prediction distributions were:

### Qwen 1.5B Claim Only

- supports: 95 (19.31%)
- refutes: 183 (37.20%)
- NEI: 214 (43.50%)

### Qwen 1.5B Gold Evidence

- supports: 373 (75.81%)
- refutes: 51 (10.37%)
- NEI: 68 (13.82%)

### Qwen 1.5B BM25 Evidence

- supports: 394 (80.08%)
- refutes: 69 (14.02%)
- NEI: 29 (5.89%)

### Qwen 1.5B Adversarial Evidence

- supports: 155 (31.50%)
- refutes: 66 (13.41%)
- NEI: 271 (55.08%)

### Qwen 14B Gold Evidence

- supports: 141 (28.66%)
- refutes: 45 (9.15%)
- NEI: 306 (62.20%)

### Qwen 14B Translated Gold Evidence

- supports: 105 (21.34%)
- refutes: 113 (22.97%)
- NEI: 274 (55.69%)

### Interpretation

The systems do not simply differ in accuracy. They exhibit qualitatively different label preferences.

The 1.5B gold and BM25 systems are strongly support-biased.

The 14B gold model is strongly NEI-biased.

Translation substantially increases the model's willingness to predict `refutes`, consistent with the large improvement in contradiction recognition.

This suggests that interventions such as retrieval, scaling, and translation reshape the classifier's decision behaviour rather than uniformly improving all classes.

---

## 16. Best system differs by label

Best observed system by class:

| Label | Best System | Accuracy |
|---|---|---:|
| NEI | Qwen 14B Translated | 0.959770 |
| refutes | Qwen 14B Translated | 0.625000 |
| supports | Qwen 1.5B Gold | 0.921687 |

### Interpretation

No single model configuration dominates every verification class.

The translated 14B model is strongest for:

- contradiction recognition;
- insufficient-information recognition.

However, Qwen 1.5B Gold Evidence achieves the highest `supports` accuracy at 92.17%.

This reinforces the finding that system improvements are class-dependent and may involve trade-offs.

The smaller model's very high supports accuracy must also be interpreted alongside its strong support prediction bias. High class-specific accuracy does not necessarily imply balanced verification competence.

---

## 17. Best model by language

The translated Qwen 14B model was best for all three languages:

| Language | Accuracy |
|---|---:|
| Hausa | 0.759036 |
| Igbo | 0.742331 |
| Yoruba | 0.705521 |

### Interpretation

The translated 14B system provides the strongest overall performance across all three target languages.

However, the lower Yoruba result remains consistent with the observed translation-induced damage to Yoruba supports examples.

Thus, the model is best across all languages while still exhibiting meaningful language-specific weaknesses.

---

# Universally Hard Examples

## 18. Universal error concentration

Across all six principal systems:

- 29 examples were wrong for every system;
- only 12 examples were correct for every system.

Among the 29 universally hard examples:

### By language

- Yoruba: 13
- Hausa: 10
- Igbo: 6

### By gold label

- refutes: 25
- supports: 4

### Interpretation

The most striking result is the overwhelming concentration of universal failures in the `refutes` class.

25 of 29 universally hard examples were refutations.

This demonstrates that contradiction recognition is the dominant persistent failure mode across:

- model scales;
- claim-only classification;
- gold evidence;
- BM25 retrieval;
- adversarial evidence;
- translation.

The problem is therefore deeper than one specific architecture or prompt configuration.

---

## 19. Persistent hard refutes by language

The 25 persistent hard refutes were distributed as:

- Yoruba: 13
- Hausa: 8
- Igbo: 4

### Interpretation

Yoruba accounts for more than half of persistent hard refutes.

This aligns with other evidence that Yoruba presents distinctive challenges in the current pipeline, including the substantial supports-class degradation after translation.

However, because the hard-error subset is small, these findings should be interpreted diagnostically rather than as population-wide statistical estimates.

---

# Manual Hard-Refute Taxonomy

## 20. Purpose and methodological status

The 25 persistent hard refutes were manually reviewed and assigned a primary error category.

This analysis is exploratory and diagnostic.

It should not be presented as a statistically representative taxonomy of all dataset errors. Instead, it identifies recurring mechanisms among the most persistent failures.

---

## 21. Primary error categories

| Primary Error Type | Count | Percentage |
|---|---:|---:|
| evidence insufficient | 6 | 24% |
| entity-attribute mismatch | 5 | 20% |
| negation | 3 | 12% |
| role-relation mismatch | 3 | 12% |
| temporal mismatch | 2 | 8% |
| boundary condition | 2 | 8% |
| causal mismatch | 1 | 4% |
| implicit contradiction | 1 | 4% |
| possible annotation issue | 1 | 4% |
| numerical mismatch | 1 | 4% |

### Interpretation

The largest category was `evidence_insufficient`, accounting for 24% of persistent hard refutes.

This suggests that some examples labelled `refutes` may not contain evidence that clearly establishes contradiction.

The second-largest category was `entity_attribute_mismatch` at 20%, showing that systems struggle when contradiction depends on assigning the wrong property, profession, identity, origin, or characteristic to an entity.

Negation and role-relation mismatches each accounted for 12%.

Overall, persistent contradiction errors are heterogeneous. They cannot be explained by a single weakness such as negation failure.

---

## 22. Contradiction explicitness

Among the 25 persistent hard refutes:

- explicit: 11 (44%)
- implicit: 7 (28%)
- ambiguous: 7 (28%)

### Interpretation

Only 44% of persistent hard refutes contained explicit contradictions.

A combined 56% were either implicit or ambiguous.

This is a crucial explanation for the difficulty of the `refutes` class. Many examples require more than surface-level contradiction detection.

The model may need to reason over:

- entity attributes;
- roles;
- temporal relations;
- causal relations;
- category membership;
- boundary conditions;
- unstated implications.

This supports the argument that low-resource fact verification requires relational and inferential reasoning, not merely lexical comparison.

---

## 23. Annotation suspicion

Manual review produced:

- no annotation issue suspected: 14 (56%)
- annotation issue suspected: 7 (28%)
- uncertain: 4 (16%)

### Interpretation

Only 56% of persistent hard refutes were judged clearly free from annotation suspicion.

For 28%, an annotation issue was suspected, while another 16% remained uncertain.

This means 44% of the persistent hard-refute subset had some degree of annotation concern.

This should be interpreted cautiously. It does not establish that 44% of the full dataset is incorrectly annotated.

Instead, it suggests that the most persistent model failures are disproportionately associated with examples where the evidence-label relationship may be unclear or debatable.

A defensible conclusion is:

> The observed performance ceiling may partly reflect dataset and evidence-quality limitations in addition to model limitations.

---

## 24. Hard-error taxonomy by language

Observed category counts were:

### Hausa

- boundary condition: 1
- causal mismatch: 1
- entity-attribute mismatch: 2
- evidence insufficient: 2
- implicit contradiction: 1
- temporal mismatch: 1

### Igbo

- evidence insufficient: 1
- negation: 1
- role-relation mismatch: 2

### Yoruba

- boundary condition: 1
- entity-attribute mismatch: 3
- evidence insufficient: 3
- negation: 2
- numerical mismatch: 1
- possible annotation issue: 1
- role-relation mismatch: 1
- temporal mismatch: 1

### Interpretation

The error mechanisms vary by language.

Yoruba displays the broadest spread of persistent error types and contains the largest number of persistent hard refutes.

Igbo persistent failures are fewer and concentrated mainly in role-relation mismatch, negation, and insufficient evidence.

Hausa errors span entity, causal, temporal, boundary, and implicit contradiction mechanisms.

Given the small subset sizes, these patterns should be described as qualitative tendencies rather than definitive language-wide distributions.

---

# Integrated Dissertation-Level Interpretation

## 25. Evidence quality matters more than evidence presence

Across experiments, merely supplying context does not guarantee improvement.

Observed pattern:

- claim only: 39.02%
- gold evidence: 45.94%
- BM25 evidence: 39.43%
- adversarial evidence: 33.33%

### Interpretation

Gold evidence improves performance, BM25 nearly collapses back to claim-only performance, and adversarial evidence performs worse than claim-only classification.

Therefore:

> The value of evidence is conditional on evidence quality.

This is a central finding for retrieval-augmented misinformation detection.

---

## 26. Retrieval is a major bottleneck

The BM25 system showed:

- only 23 wrong-to-correct repairs relative to gold evidence;
- 55 correct-to-wrong regressions;
- net loss of 32;
- 80.08% supports prediction rate;
- 245 identified support-bias failures.

### Interpretation

The retriever can fundamentally reshape downstream classifier behaviour.

The results suggest that lexical retrieval may be inadequate when verification requires:

- contradiction-aware matching;
- semantic distinction;
- entity relation reasoning;
- temporal reasoning;
- recognition that relevant evidence is not necessarily supporting evidence.

A future system should consider:

- dense multilingual retrieval;
- hybrid sparse-dense retrieval;
- cross-encoder reranking;
- contradiction-aware reranking;
- retrieval confidence thresholds;
- abstention when evidence quality is weak.

---

## 27. Scaling and translation solve different problems

Scaling from 1.5B to 14B produced:

- +89 net correct examples

Translation at 14B produced:

- +47 net correct examples

### Interpretation

These interventions are complementary.

Scaling improves the model's general capacity to interpret evidence and reason over claims.

Translation improves linguistic accessibility, allowing the larger model to use its existing reasoning capabilities more effectively.

This suggests a two-stage explanation:

1. sufficient model capacity is needed for evidence reasoning;
2. accessible linguistic representation is needed for that capacity to be fully expressed.

---

## 28. Translation is powerful but asymmetric

Translation:

- improved overall accuracy by approximately 9.55 points;
- improved Igbo by approximately 13.50 points;
- improved Hausa by approximately 10.84 points;
- improved Yoruba by approximately 4.29 points;
- improved refutes by 37.50 points;
- reduced supports by 6.63 points;
- reduced Yoruba supports by approximately 27.27 points.

### Interpretation

Translation should be understood as a high-impact but asymmetric intervention.

It repairs many contradiction failures but can damage entailment when culturally specific terms, numerical relations, or semantic details are mistranslated.

This motivates language-aware translation quality controls rather than universal blind translation.

---

## 29. Contradiction recognition is the central unresolved challenge

Evidence:

- 25 of 29 universally hard examples were refutes;
- original Qwen 14B refutes accuracy was only 25%;
- translation improved it to 62.5%, but substantial errors remained;
- 56% of persistent hard contradictions were implicit or ambiguous;
- persistent errors included entity, role, temporal, numerical, causal, and boundary mismatches.

### Interpretation

The dissertation's strongest overarching error-analysis conclusion is:

> Contradiction recognition is the principal unresolved challenge in low-resource evidence-based fact verification.

The difficulty arises not only from language representation but from the inferential structure of contradiction itself.

---

## 30. Dataset quality contributes to the observed ceiling

Among 25 persistent hard refutes:

- 28% had suspected annotation issues;
- 16% were uncertain;
- 24% were primarily categorised as evidence insufficient.

### Interpretation

Some apparent model failures may be partly attributable to weak evidence-label alignment.

This is particularly important for evaluation. If the supplied evidence does not clearly refute the claim, a model predicting NEI may be semantically defensible even when scored as incorrect against the dataset label.

Therefore, model performance should be interpreted alongside dataset quality rather than as a pure measure of reasoning ability.

---

# Final Research Narrative

The complete experimental evidence supports the following research narrative:

1. Low-resource claim verification is difficult under claim-only conditions.
2. Gold evidence improves performance, but small models use evidence inconsistently.
3. BM25 retrieval fails to reproduce oracle-evidence gains and induces severe support bias.
4. Misleading evidence can reduce performance below claim-only classification.
5. Increasing model scale substantially improves evidence reasoning.
6. Translating low-resource content into English produces the strongest overall system.
7. Translation gains are driven primarily by improved contradiction recognition.
8. Translation can also corrupt culturally specific and language-specific semantics, especially for Yoruba supports examples.
9. Generic prompt demonstrations can reduce performance rather than improve it.
10. Persistent failures concentrate overwhelmingly in the refutes class.
11. Hard contradictions frequently require implicit relational reasoning rather than explicit negation.
12. A meaningful proportion of persistent failures involve questionable evidence-label alignment.
13. The main bottlenecks are therefore not reducible to model size alone: retrieval quality, linguistic accessibility, contradiction reasoning, and dataset quality all contribute.

## Core dissertation contribution emerging from the experiments

The experiments collectively suggest that successful low-resource retrieval-augmented misinformation detection requires alignment across four components:

- linguistic representation;
- retrieval quality;
- model reasoning capacity;
- evidence-label validity.

Failure in any one component can dominate end-to-end performance.

The strongest observed system used translation and a larger LLM, but the error analysis demonstrates that even this configuration remains constrained by contradiction complexity and evidence quality.

This provides a richer conclusion than simply identifying the highest-performing model. The dissertation demonstrates how and why performance changes across retrieval, scaling, translation, prompting, and adversarial evidence conditions.

