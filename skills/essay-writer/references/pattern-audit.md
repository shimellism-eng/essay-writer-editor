# Pattern audit and repair

Use this reference when the user asks whether prose contains statistical, structural, repetitive, or mechanically regular patterns, or asks for those patterns to be repaired.

## Boundary

AI-assisted writing can contain regular patterns. Human, translated, collaborative, edited, technical, and formulaic writing can contain them as well. A pattern audit describes the text and its reader effects; it does not identify an author, model, or percentage of AI contribution.

Do not:

- promise that a repair will evade a detector or produce a human score;
- add random errors, slang, fragments, or unusual punctuation merely to create variation;
- invent exact counts, statistical significance, corpus comparisons, or probabilities;
- rewrite a passage solely because a pattern is associated with AI writing;
- change a quotation, citation, number, factual claim, uncertainty, or meaningful voice marker without disclosure.

## Choose the task

Separate these requests:

1. **Pattern audit:** describe recurring features and their likely effect on reading.
2. **Pattern repair:** revise the prose where a recurring feature harms clarity, pace, specificity, or voice.
3. **Authorship analysis:** use Detect mode and [ai-writing-signals.md](ai-writing-signals.md). Do not silently turn a pattern audit into an authorship judgement.

If the user asks for both, return the repair and the audit as clearly labelled parts. The audit must not be used to claim that the repair makes the text human-written.

## Inspect the text

Use enough text to support the observation. Short passages can show an obvious local repetition, but they cannot support a reliable distributional claim. State when the sample is too short, too edited, translated, collaborative, technical, or genre-bound for a strong conclusion.

Look for clusters rather than isolated quirks:

| Pattern family | Questions to ask |
|---|---|
| Sentence shape | Do many sentences begin the same way or use the same clause sequence? |
| Rhythm | Are sentence lengths and paragraph sizes unusually uniform for the argument? |
| Transitions | Do the same signposts announce every move, even when the logic is already clear? |
| Rhetorical lists | Do repeated triads, mirrored contrasts, or serial conclusions add meaning or merely fill space? |
| Specificity | Does the prose repeat abstract benefits while avoiding the concrete detail that would test the claim? |
| Stance | Are hedges, certainty markers, praise, or moral conclusions repeated without a change in evidence? |
| Vocabulary | Are key terms usefully repeated, or are near-synonyms being rotated mechanically? |
| Paragraph function | Does every paragraph follow the same claim-evidence-explanation-summary template when the reasoning needs a different shape? |

## Count carefully

When tools are available, simple descriptive measures can support an observation: word count, sentence count, sentence-length range, repeated opening phrases, transition frequency, and paragraph-length range. Report what was measured and the text scope.

Do not present a descriptive count as a statistical test. Avoid claims such as “this proves AI,” “this is outside the human distribution,” or “the text has a 78% AI probability.” If no calculation was performed, use wording such as “many paragraphs begin with the same transition” rather than a made-up percentage.

## Formula habits worth checking

Some habits recur in heavily templated prose, including much model-generated writing. Check for them in every pattern repair and before returning a public-facing draft such as a personal statement. Repair them because they read as formula and weaken the writer's voice, not to evade a detector. Keep any instance the writer clearly chose.

| Habit | Example | Usual repair |
|---|---|---|
| Repeated reflective verbs | "showed me", "taught me", "made me realise" several times in one piece | Keep the writer's own instances; recast the rest as what the writer did or concluded |
| Stacked insight openers | "I came to see", "I now see", "I believe", "I expect" in close succession | Keep one or two; state the remaining points directly |
| Motto sentences | "A figure is only as reliable as the evidence behind it." | Restate as a plain claim tied to the writer's own experience |
| Short dramatic set-up sentences | "It also showed me a limit." "Carbon is the clearest test of that idea." | Merge into the sentence that carries the content |
| Colon reveals | "kept bringing me back to one principle: ..." | Say the point without the build-up |
| Stock vocabulary | "passion", "delve", "pivotal", "invaluable", "perfectly aligns", "moreover", "furthermore", "tapestry", "in today's world" | Use the plainer word, or cut the phrase if it adds nothing |
| Promotional superlatives about organisations | "China's No.1 firm", "a globally leading group" | Name the organisation and what the writer did there; keep a ranking only if it is verified and relevant |
| Triad stacking | several three-item lists in one paragraph | Keep the lists that carry information; split or shorten the rest |
| Punctuation the writer does not use | em dashes in a writer's prose that otherwise has none | Follow the writer's or user's punctuation habits |

When tools are available, measure before claiming a repair worked: count the repeated phrases above, and report the sentence-length range, mean and spread for the scope checked. Report the counts as descriptive, not as evidence of authorship.

## Repair for meaning

Make the smallest effective change:

- combine sentences when repetition is only restating the same point;
- split a breathless sentence when distinct reasoning is being compressed;
- remove a transition when the relationship is already clear;
- replace a generic abstraction with a supported detail from the source or draft;
- let a paragraph end when its actual job is complete;
- vary sentence shape only when the thought changes;
- retain repetition when it creates emphasis, rhythm, accessibility, or voice.

After repair, check that the argument, evidence, quotation, citation, number, uncertainty, dialect, and stated position are unchanged. Mention any material interpretive decision.

## Return contract

For an audit only:

1. Overall pattern assessment
2. Short quoted examples
3. Counterexamples and ordinary explanations
4. Limitations of the sample and method
5. Reader-focused next step

For a repair request:

1. Revised passage first
2. Pattern changes made
3. Patterns intentionally retained
4. Evidence, voice, or uncertainty checks

The goal is clearer, more specific, more recognisable writing. It is not detector evasion.
