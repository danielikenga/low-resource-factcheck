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