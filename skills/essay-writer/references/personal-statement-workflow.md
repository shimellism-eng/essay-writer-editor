# Personal statement workflow

Use this end to end whenever the user asks for a personal statement, or asks to adapt one for another programme. The aim is one pass that ends in a statement ready to submit, without the user having to request each check.

## 1. Gather inputs

Required:

- the writer's material: an existing statement, a CV, notes, or a list of facts;
- the target programme's official page (a link or the programme name and institution).

Optional, with defaults:

- **Word limit:** use the limit the user or the application states; otherwise aim for 800 to 900 words.
- **Spelling:** match the writer's existing statement; if there is none, match the target institution's own pages.
- **Facts:** use only the supplied material. Do not use other files that happen to be nearby, such as older drafts for other programmes, unless the user says to.

Ask only for a required input that is missing. Proceed on the defaults otherwise.

## 2. Lock the facts

Before drafting, save the writer's material as plain text. Every grade, score, rank, date, paper title, organisation, role, award and stated goal in the final statement must come from it. Keep stated goals exactly as written; do not upgrade them to suit the new programme. Leave out a detail whose meaning is unclear rather than guessing, and mention it to the user in one line.

## 3. Research the programme

Read the official programme page and, where one exists, the official course catalogue. Some university pages load their content inside an embedded frame; if the page text looks empty, open the frame's own address. Use the current or next intake year that is actually published.

Save programme notes as plain text: the exact award title, required courses, relevant electives (with exact names and a phrase from each description), project or internship components, placement locations, and any stated focus such as national targets or a region. Use course names exactly as published. Do not use rankings, league tables or marketing superlatives.

## 4. Plan the throughline

Find the one idea that links the writer's existing story to the new field, and state it in a sentence. Plan at most three short bridging sentences that connect the writer's experience to the programme. Bridges are reasoning, not new facts.

## 5. Draft

Write in a natural human voice (see [voice-and-editing.md](voice-and-editing.md)) from the locked facts and programme notes only. A usual order:

1. Opening built on something from the writer's own material, then the link to the target field and the application.
2. Academic record and the most relevant research, with what the writer took from it.
3. Experience, with the principle it taught that carries into the new field.
4. Other achievements and roles, briefly.
5. Specific courses and programme components, each tied to a gap or interest already shown.
6. Career goal as the writer stated it, and a closing sentence that adds consequence rather than repeating the opening.

Follow the adaptation rules in [specialized-writing.md](specialized-writing.md) when an existing statement is supplied.

## 6. Cut to the limit

If the draft is over the limit, apply "Cut to a word limit" in [voice-and-editing.md](voice-and-editing.md). Do not drop a supporting fact without the user's agreement.

## 7. Run the checker and fix

Run the checker on the draft, with the writer's material and the programme notes as sources:

```bash
python3 scripts/check_statement.py draft.txt --limit 800-900 --source writer-material.txt programme-notes.txt
```

The script is in this skill's `scripts` folder. Fix every FAIL. Review every WARN: fix it when it is a real habit or an untraced fact, and leave it when it is a proper name, a course title, or a sentence that carries content. Run the checker again until nothing fails. Then read the whole statement once more against the formula habits in [pattern-audit.md](pattern-audit.md), since a script cannot judge every sentence.

Repair every formula habit you find yourself, writing as the student would: plain, specific sentences built only from the locked facts. Do not hand a list of flagged sentences back to the user or the student as homework. Keep the student's own sentences from the source where they read naturally. If a better sentence would need a detail the sources do not give, write the plain version and list the question in the reply.

## 8. Deliver

Create the Word file:

```bash
python3 scripts/make_docx.py draft.txt "Name - Programme.docx" --title "Personal Statement" --subtitle "Name | Programme, Institution"
```

The file carries no author, software or editing-history metadata. Return the statement and the Word file. In the chat reply, add only what the user must act on: any detail left out because its meaning was unclear, and any fact that still needs confirming. Do not promise any AI-detector or similarity score.
