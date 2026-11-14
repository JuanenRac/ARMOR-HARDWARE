# Measurement record

A row of the [bench acceptance](BENCH_ACCEPTANCE.md) matrix turns to *passed* only with a dated measurement record. This page says how a record is kept; `measurement_record_template.csv` is the template, with one line for each row of the matrix.

## How to fill it in

1. Copy `measurement_record_template.csv` next to the prototype (never edit the template).
2. For each row you measure, fill in: `date` (the day of the measurement), `operator`, `instrument` (make, model and when it was last calibrated), `method` (what you did, in a sentence, or the step of the matrix), `value` and `unit` (what you read), `result` (`passed`, `failed` or `not applicable`, against the pass criterion in the third column) and `evidence`.
3. `evidence` names a file in a folder next to the copy: a photo of the set-up and of the reading, or the log. One photo shows the whole set-up and one shows the instrument's display.
4. Only then change the status of the row in the matrix, by hand, in the same commit that says which record it rests on.

## What a record is not

A line without a value, an instrument or a piece of evidence is not a record. A criterion that cannot be measured is rewritten in the matrix until it can; it is not marked *passed*. The template is generated from the matrix (`python tools/make_measurement_template.py`) and a test fails when it is out of date, so a new row of the matrix has its line.
