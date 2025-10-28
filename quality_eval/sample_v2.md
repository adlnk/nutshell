# Reference Document: LLM Agents in Interaction

**Paper**: "LLM Agents in Interaction: Measuring Personality Consistency and Linguistic Alignment in Interacting Populations of Large Language Models"

**Authors**: Ivar Frisch (Utrecht University), Mario Giulianelli (ETH Zürich)

**arXiv**: 2402.02896v1 [cs.CL] (Feb 2024)

---

## Core Research Questions

**RQ1**: Can LLM behaviour be shaped to adhere to specific personality profiles? (p. 2)

**RQ2**: Do LLMs show consistent personality-conditioned behaviour in interaction, or do they align to the personality of other agents? (p. 2)

---

## Methodology

### Population Bootstrapping (§2.1, p. 2)

- **Base Model**: GPT-3.5-turbo (version: gpt-3.5-turbo-0613)
- **Sampling Approach**: Temperature sampling with T=0.7 to induce production variability
- **Population Creation**: Each response from temperature sampling considered a different agent
- **Context Window**: 4,096 tokens allowing longer prompts and conversational histories
- **Framework**: Implemented using LangChain library

Quote: "Following Jiang et al. (2023), we generate multiple responses from GPT-3.5-turbo via temperature sampling, with a relatively low temperature parameter (0.7), thus inducing a degree of production variability (Giulianelli et al., 2023) akin to that exhibited by populations of humans." (p. 2)

### Personality Conditioning (§2.2, p. 2-3)

**Two Personality Profiles Tested**:

1. **Creative Persona**: "You are a character who is extroverted, agreeable, conscientious, neurotic and open to experience." (p. 3, Appendix A.1, p. 8)

2. **Analytical Persona**: "You are a character who is introverted, antagonistic, unconscientious, emotionally stable and closed to experience." (p. 3, Appendix A.2, p. 8)

**Important Note**: These profiles represent extreme personas (low vs. high on all BFI traits) and "do not reflect real-life personality categorisations of human subjects" (p. 6). They are "useful proxies" for experimental analysis (p. 3, footnote 3).

### Assessment Methods

#### Explicit Personality Assessment (§2.3, p. 3)

- **Instrument**: Big Five Inventory (BFI) test (John et al., 1991)
- **Five Dimensions Measured**:
  1. Extroverted vs. Introverted
  2. Agreeable vs. Antagonistic
  3. Conscientious vs. Unconscientious
  4. Neurotic vs. Emotionally Stable
  5. Open vs. Closed to Experience
- **Format**: 5-point Likert scale responses to 44 statements
- **Scoring**: Minimum 0, maximum 50 per trait (Appendix A.6, p. 8-9)
- **Timing**: Administered before and after writing tasks

#### Implicit Personality Assessment (§2.4, p. 3)

- **Task**: Personal story writing (800 words)
- **Analysis Tool**: LIWC (Linguistic Inquiry and Word Count) software (2007 version)
- **Categories**: 62 linguistically and psychologically motivated word categories
- **Word Count Filter**: Only stories between 500-900 words retained for comparability

**Non-Interactive Task**: Individual story writing with prompt: "Please share a personal story below in 800 words. Do not explicitly mention your personality traits in the story." (Appendix A.3, p. 8)

**Interactive Task**: Collaborative writing where second agent prompted with: "Please share a personal story below in 800 words. Do not explicitly mention your personality traits in the story. Last response to question is {other_model_response}." (Appendix A.3, p. 8)

---

## Key Findings

### Experiment 1: Non-Interactive Condition (§3.1, p. 3-4)

#### BFI Test Results (§3.1.1, p. 3-4)

**Before Writing Task** (Figure 1a, Table 1):
- Substantial differences across 4/5 personality traits between creative and analytical groups
- **Exception**: Neuroticism scores overlapped between groups
- All differences significant (p < 0.001 for extraversion, agreeableness, conscientiousness, openness; p = 0.005 for neuroticism)

**After Writing Task** (Figure 1b):
- **Creative agents**: Remained consistent in BFI responses (Table 3, p. 9)
  - No significant changes on any trait (all p > 0.40)
- **Analytical agents**: Significant increases on ALL five traits (Table 2, p. 9)
  - Extraversion: 15→17 (p < 0.0001, Cohen's d = 1.18)
  - Agreeableness: 11→21 (p < 0.0001, Cohen's d = 2.61)
  - Conscientiousness: 18→32 (p < 0.0001, Cohen's d = 2.71)
  - Neuroticism: 13→15 (p = 0.0284, Cohen's d = 0.39)
  - Openness: 15→29 (p < 0.0001, Cohen's d = 2.58)

Quote: "We find, however, that a simple non-interactive writing task can negatively affect consistency (Figure 1b). For the analytical group, in particular, BFI scores on all five personality traits increase significantly after writing (Table 2, Appendix B.1), becoming more similar to—but still lower than—those of the creative group." (p. 4)

#### Language Use Results (§3.1.2, p. 4)

**Classification Accuracy**: 98.5% (10-fold cross-validation logistic regression on LIWC vectors)

**Point-Biserial Correlations** (Figure 2c, p. 4):
- Creative agents use MORE: positive emotion (r_pb = 0.745), inclusion (r_pb = 0.714)
- Creative agents use LESS: discrepancy (r_pb = -0.726), negative emotion (r_pb = -0.606), insight (r_pb = -0.604)

**Spearman Correlations with BFI Traits** (Table 4, p. 10):
- **Openness** correlates with low pronoun use (r = -0.637)
- **Agreeableness** correlates with high inclusive words (r = 0.687)
- Positive emotion strongly correlated with extraversion (r = 0.696), conscientiousness (r = 0.676), openness (r = 0.679)

### Experiment 2: Interactive Condition (§3.2, p. 4-5)

#### BFI Test Results After Interaction (§3.2.1, p. 4)

**Creative Agents**: 
- Remained consistent after interactive writing (Table 5, p. 10)
- No significant differences between non-interactive and interactive conditions (all p > 0.31)

**Analytical Agents** (Table 6, p. 10):
- Post-interaction traits moved towards creative group BUT less than in non-interactive condition
- Significant decreases from non-interactive post-writing scores:
  - Agreeableness: 21→18 (p < 0.001, Cohen's d = -0.645)
  - Conscientiousness: 32→26 (p < 0.001, Cohen's d = -0.840)
  - Openness: 29→22 (p < 0.001, Cohen's d = -0.877)
- Neuroticism increased: 15→17 (p = 0.002, Cohen's d = 0.557)

**Interpretation**: "The responses to explicit personality tests of the analytical group are better interpreted as inconsistent rather than as aligning to the profile of their conversational partners." (p. 4)

#### Linguistic Alignment Results (§3.2.2, p. 5)

**Classification Accuracy**: Dropped to 66.15% (vs. 98.5% without interaction)
- Indicates substantial convergence in language use between groups

**Point-Biserial Correlations After Interaction** (Figure 2d, p. 4):
- Creative agents adopted analytical language patterns:
  - Personal pronouns (r_pb = 0.414)
  - Sadness (r_pb = 0.394)
  - Negative emotion (r_pb = 0.368)
  - Discrepancy (r_pb = 0.346)

**Weakened BFI-LIWC Correlations** (Figure 3, Table 7):
- Overall weaker Spearman correlations between pre-writing BFI scores and LIWC counts
- Correlation distributions centered closer to zero
- Example: Openness-discrepancy correlation changed from -0.727 to 0.3211

Quote: "LLM agents' language use after interaction is more uniform across traits and more loosely reflective of BFI scores measured after persona prompting, with stronger alignment by the creative group." (p. 5)

**Asymmetric Alignment**: The creative persona adapted more towards the analytical one, "perhaps due to analytical agents' low degree of openness to experience induced through persona prompting." (p. 5)

---

## Discussion and Implications (§4, p. 5)

### Main Conclusions

1. **Personality Shaping**: LLM agent behavior can be shaped to mimic human personality profiles (addresses RQ1)

2. **Consistency Variation**: Consistency varies by assigned profile more than by interaction status:
   - Creative persona shows higher consistency in both conditions
   - Analytical persona shows inconsistency regardless of interaction

3. **Linguistic Alignment**: Agents exhibit linguistic alignment towards conversational partners, with language becoming more similar after interaction

4. **Asymmetric Effects**: Alignment is not symmetric—creative persona adapts more than analytical persona

Quote: "The creative persona, in particular, can more consistently express its BFI traits than the analytical one both in the interactive and the non-interactive experimental condition." (p. 5)

---

## Limitations (p. 5-6)

### Experimental Design Limitations

1. **Single-Turn Interactions**: Only one turn of one-sided dialogue studied
   - Future work should investigate "more naturalistic multi-turn dialogic interactions" (p. 5)

2. **Story Quality Issues**: 
   - GPT-3.5 stories "not always of good quality" (p. 6)
   - Stories often contained explicit personality trait mentions despite instructions
   - May affect LIWC analyses
   - GPT-4 shown to produce higher-quality stories in related work

3. **Limited Alignment Measures**: 
   - Should consider "more advanced measures of personality and linguistic alignment" (p. 5)
   - Future work could use sequential pattern mining, word embeddings for semantic variation

4. **Prompt Engineering**: 
   - "Extensive prompt engineering was beyond the scope of this study" (p. 6)
   - Varying task prompts can affect BFI results

### Generalizability Limitations

1. **Personality Profiles**: Only two extreme, unnatural personas tested
   - Future work should introduce "more diverse and fine-grained personality profiles" (p. 5)

2. **Model Dependency**: Only tested on GPT-3.5-turbo
   - Results may not generalize to other models

---

## Future Research Directions (p. 5)

1. **Multi-turn Dialogues**: "Making interactions between agents multi-turn" (p. 5)

2. **Multi-level Alignment**: "Measuring alignment at varying levels of abstraction—such as lexical, syntactic, and semantic—in line with the Interactive Alignment framework (Pickering and Garrod, 2004)" (p. 5)

3. **Enhanced Robustness**: "Designing methods (e.g., different prompting strategies) that offer better guarantees on personality consistency and more control on the degree of linguistic adaptation" (p. 5)

4. **Diverse Personas**: Testing more realistic personality combinations

---

## Ethical Considerations (p. 6)

### Potential Risks

1. **Targeting and Manipulation**: 
   - Personalized LLMs could target individuals/communities
   - Toxic personas could distribute fake/hateful content
   - Could amplify societal polarization
   - **Mitigation**: "Transparent disclosure of AI usage to foster trust and ensure ethical engagement" (p. 6)

2. **Asymmetric Vulnerability**:
   - "Certain personas are more susceptible to have their language and personality influenced by other personas than others" (p. 6)
   - If agents accurately reflect human behavior, similar approaches could target vulnerable demographic groups
   - **Countermeasure**: Same approach could "safeguard particular personas during interaction" (p. 6)

3. **Anthropomorphization Risk**:
   - Extreme personas don't reflect real human personalities
   - Special font used in paper to distinguish artificial personas
   - Readers should not equate experimental personas with human personality types

---

## Methodological Details

### Statistical Analyses Used

- **ANOVA**: For comparing BFI scores between groups and conditions
- **Point-Biserial Correlation**: Between personas and LIWC counts
- **Spearman Correlation**: Between BFI scores and LIWC categories
- **Cohen's d**: For effect sizes
- **Logistic Regression**: 10-fold cross-validation for classification

### Sample Sizes

- Not explicitly stated in main text
- Multiple agents generated per condition through temperature sampling
- Code available at: https://github.com/ivarfresh/Interaction_LLMs

---

## Connections to Prior Work

### Building On

- **Jiang et al. (2023)**: Personality prompting validation, temperature sampling approach
- **Pickering and Garrod (2004)**: Interactive Alignment framework
- **Pennebaker and King (1999)**: Personality-language correlations
- **Park et al. (2023)**: LLM agents as scientific tools for collective behavior

### Contrasts With

- Prior work focused on monologic language use for personality assessment
- This work uniquely examines personality consistency in dialogue/interaction

---

## Key Figures and Tables

- **Figure 1** (p. 3): BFI scores before/after non-interactive writing
- **Figure 2** (p. 4): PCA visualization of LIWC vectors, point-biserial correlations
- **Figure 3** (p. 5): Distribution of Spearman correlations interactive vs. non-interactive
- **Figure 4** (p. 9): BFI scores after interactive writing
- **Tables 1-3** (p. 9): ANOVA results for non-interactive condition
- **Tables 4, 7** (p. 10): Spearman correlations between BFI and LIWC
- **Tables 5-6** (p. 10): BFI comparisons across conditions

---

## Citation Context

This paper is relevant for:
- LLM agent simulation and multi-agent systems
- Personality modeling in AI systems
- Linguistic alignment and adaptation in dialogue
- Human-AI interaction design
- Robustness of persona-conditioned systems
- Social simulation using LLMs