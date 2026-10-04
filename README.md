# *AI Meeting Action-Item Extractor*

An AI assistant that converts meeting transcripts into structured action items — task, owner, deadline, confidence, and status — using a transformer-based pretrained model to recognize names and dates, instead of hand-written keyword lists.

## What it does 

Meetings produce spoken commitments ("I'll send the report by Friday," "Can you call the vendor tomorrow?") that are easy to lose track of. This tool automates turning those spoken lines into structured records:

1. A meeting transcript is uploaded as a `.txt` file or pasted directly into a web page.
2. The tool scans each line of dialogue for action-indicating phrases (e.g. "I'll", "can you", "needs to").
3. For each action line, it uses **spaCy's transformer-based NER (Named Entity Recognition) model** (`en_core_web_trf`, built on the RoBERTa transformer architecture) to detect:
   - **Owner** — who is responsible (a `PERSON` entity recognized in the sentence, or the speaker themselves if they're committing to it)
   - **Deadline** — when it's due (a `DATE` entity recognized in the sentence)
4. Duplicate mentions of the same task are automatically skipped.
5. Each item gets a **confidence score** (0–100) based on whether an owner and deadline were both found, and is flagged **CONFIDENT** or **NEEDS REVIEW** accordingly.

## Project structure 🪜
├── sample_transcript.txt # Example meeting transcript used for testing
├── extract_actions.py # Early exploratory version, kept to show development process
├── extractor.py # Final extraction logic (transformer-based NER + validation rules)
├── annotated_transcripts.py # Hand-annotated test transcripts with known correct answers
├── evaluate.py # Evaluation script comparing predictions against the annotated answers
├── app.py # Streamlit web app (upload or paste a transcript, see results)

## How to run it 🏃🏼‍♀️

1. Install the required libraries:
2. pip install streamlit spacy spacy-curated-transformers
python -m spacy download en_core_web_trf
   Note: this downloads a transformer model (several hundred MB) and installs `torch`, the deep-learning engine it runs on. This is a larger install than a typical small Python package — expect it to take a few minutes.

3. Launch the app:
4. python -m streamlit run app.py
   
5. Open the local URL shown in the terminal (usually `http://localhost:8501`), upload a `.txt` transcript file or paste one directly (formatted as `Speaker: dialogue line`, one line per turn), and click **Extract action items**.

6. To run the evaluation separately:
7. python evaluate.py
   
## Approach 🧬

The project brief asks for an LLM **or** transformer model to be used for the extraction step. We used a transformer model — specifically **spaCy's `en_core_web_trf`**, a RoBERTa-based transformer pipeline, which is a genuine transformer architecture, not a large language model (LLM) like GPT. The brief allows either, and a transformer model is free to run locally with no API key or cost, which made it the right choice given the project timeline.

1. **Input format**: A transcript is split line by line, and each line is separated into `speaker` and `text` using the `:` character.
2. **Action detection**: Each line's text is checked against a list of action-indicating phrases (`i'll`, `i will`, `can you`, `could you`, `needs to`, `need to`, `will`). Lines without any of these are skipped.
3. **Duplicate detection**: A line is skipped if its exact text has already been processed earlier in the same transcript, preventing the same task from appearing twice.
4. **Owner detection**:
   - If the speaker is committing to the task themselves (text starts with "I " or contains "I'll"/"I will"), the owner is the speaker.
   - Otherwise, the sentence is passed through the transformer model, and any entity it tags as `PERSON` is taken as the owner.
5. **Deadline detection**: The same sentence is checked for entities the model tags as `DATE` (e.g. "Friday", "next Tuesday", "the 15th", "tomorrow").
6. **Confidence scoring**: Each item gets 50 points for a found owner (10 if not found) and 50 points for a found deadline (10 if not found), for a score out of 100. Items scoring 70+ are marked **CONFIDENT**; below that, **NEEDS REVIEW**.
7. **Evaluation**: Three hand-annotated transcripts (`annotated_transcripts.py`) with known correct owner/deadline answers are run through the extractor, and `evaluate.py` compares the results, reporting accuracy.
8. **Deployment**: A Streamlit web app (`app.py`) provides the interface — upload or paste a transcript, click a button, see the extracted items as cards.

## Evaluation results 📠

Running `evaluate.py` against the 3 annotated test transcripts (7 total action items, including one deliberately duplicated line to test duplicate detection):

- **Owner accuracy: 7/7 = 100%**
- **Deadline accuracy: 7/7 = 100%**
- The duplicated line in the first test transcript was correctly detected only once (not twice), confirming the duplicate-detection rule works.

## A real technical challenge we ran into 💪🏼

Installing the transformer model wasn't simple. The first install attempt (`spacy-transformers` + `en_core_web_trf`) failed because one of its dependencies (`spacy-alignments`) needed to be compiled from source code, and the development machine's Python version (3.14, a very new release) didn't have prebuilt installation files available for it yet. We found that spaCy offers an alternative installation path using `spacy-curated-transformers`, which uses ready-made installable files instead of requiring anything to be compiled. That install succeeded.

## Honest limitations 🤦🏼‍♀️

- **Requires a `Speaker: text` format**: The parser depends on each line having a speaker name followed by a colon.
- **One sentence at a time**: Each line is analyzed independently, with no memory of earlier or later lines.
- **Small, self-made evaluation set**: The 3 annotated transcripts were written by us, not sourced from a larger external dataset.
- **Confidence score is a simple heuristic, not a trained probability**.
- **No real "project" context**: The tool reacts to phrasing patterns and entity tags, so it can misfire on sentences that use action-like phrasing without being real commitments.

## Possible next steps 🪜

- Expand the annotated test set with transcripts from more varied sources.
- Add context across multiple lines instead of treating each line in isolation.
- Support transcript formats that don't use a `Speaker:` prefix.
- Let users correct wrong extractions in the app and use those corrections to improve the rules over time.

## 🤣 *What I Learnt and the Challenges I faced while making this Project* 🤣
I with my ai assistant help built the simple transcripts[meeting scripts] file so that we added random meeting conversation into that file. As I moved forward we created a file where the main body of this project [where ai model analyse the owner, task, deadline of the transcript] gets to implement, but here I got an error where the model didn't figured out the owner ,deadline or the task. So we replaced that file and added the action-phases to figure out the owner. Here the model figured out the action-phase[task] but I was not getting the owner and the deadline ,so we replaced it and added the names[owner] and time[deadline]. I got my desired output by this step. In the next step we add the confidence file in the 'extract_action.py' to show how confident is the model about given transcripts . In that file there was an indentation error so, I corrected it and the model was showing the confident level correctly. In next step we should create a new file called extractor.py but I didn't understood that and replaced the extractor file in extract_actions file 🤣🤣 I realised my mistake and replaced the files to their own places .Later we built app.py to show the output in the webpage using streamlit . But in the output only took the saved names in the file. So the model didn't took the new names . So I change whole file of extractor.py and the output was correct , but the deadline was not specifying even though i gave a date because the file only could identified days.  I change that by adding date_match in the code and the output was correct. We added slight correct in the confidence code to add score and added confident score in app.py . Just like this more code were updated in many file for the corrections . Until here everything was going great but 😥 but😖😖😖😖I forgot that this project should include llm or transformer model🤦🏼‍♀️🤦🏼‍♀️.Then we added spaCy and replaced EVERY SINGLE FILE . but again and again I was facing lots of errors in code and in indentation .Atlas I got the output that I wanted.

## Thankyou for Reading
