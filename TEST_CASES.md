# Test Cases

| ID | Input | Expected result | Actual result | Status |
|---|---|---|---|---|
| TC01 | Valid text PDF resume | Text extracted and analysis returned | Run locally | Pending |
| TC02 | Valid DOCX resume | Text extracted and analysis returned | Run locally | Pending |
| TC03 | TXT or image file | 400 unsupported file message | Run locally | Pending |
| TC04 | Empty PDF/DOCX | 400 readable-text message | Run locally | Pending |
| TC05 | Resume plus empty job description | 400 validation message | Run locally | Pending |
| TC06 | Resume with Python, Flask, SQL | Matched skills and score reflect overlap | Run locally | Pending |
| TC07 | Resume missing job skills | Missing skills are labeled not detected | Run locally | Pending |
| TC08 | Corrupted document bytes | 400 extraction error, no traceback | Run locally | Pending |
| TC09 | Frontend with API stopped | Clear API unavailable message | Run locally | Pending |
| TC10 | Valid analysis report action | PDF download with score and breakdown | Run locally | Pending |
