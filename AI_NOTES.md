# AI Notes

## 1. What was AI generated vs written by me

I used Claude to scaffold the whole project: the FastAPI app in src/main.py, the Pydantic models in src/models.py, the JSON file storage layer in src/storage.py, and the test suite in tests/test_expenses.py. I did not write the initial code by hand.

What I did instead was treat the generated code as something I had to fully understand before I could call it mine. I went through each file with Claude explaining it line by line, in plain terms, until I could describe what every endpoint does and why, without looking anything up. I also set up the whole environment myself from scratch,created the virtual environment, installed the dependencies, ran the server, and pushed it to GitHub, so the parts around the code are as much mine as the code itself.

## 2. What I validated or tested, and why

I ran pytest tests/ -v myself on my own machine and got all 11 tests passing. I did not just trust that number, I read through what each test was actually checking, like rejecting a negative amount or a blank title, and deleting an expense that does not exist and getting a 404 back.

After that I started the server with uvicorn and went through every endpoint manually using the Swagger docs at /docs, not just the automated tests. This is actually where I caught something myself: when I tested the category filter, I had left the sample field as "category": "string" instead of typing a real category like "food", so filtering by food came back empty. At first I thought something was broken, but going back through it I realized it was my own test data, not the code. I re-ran it with a real category value and it worked as expected. That was a useful reminder to actually check my own inputs before assuming the API is wrong.

I also manually confirmed the totals endpoint gives the right overall number and the right breakdown by category, that the monthly summary groups correctly by year and month, and that deleting an expense actually removes it from the list on a follow up GET request.

## 3. AI suggestions I did not use, and why

Honestly, I did not reject any specific AI suggestion in this build, Claude generated the structure in one pass and I reviewed and tested it rather than asking for alternatives. I would rather say that plainly than invent a rejection that did not happen.

The one thing I would flag as a limitation, not something I changed, is that expenses are stored in a local JSON file rather than a real database. That is fine for a take home assignment of this size, but if this were going into production I would want to move to something like SQLite so multiple users and larger data sets are handled properly.

## A note on how I like to work with AI

I enjoy prompt engineering and I use AI a lot, but my rule for myself is that I am not allowed to submit something I cannot explain. So with this project, once the code worked, I made Claude walk me through every file and every endpoint like I was learning it from zero, asked questions until the gaps closed, and only then started writing this document. If someone asks me about the storage locking, the validation rules, or why the totals endpoint is structured the way it is, I can answer that directly now.