To verify your code is working correctly you can do the following

1. Enter queries into the `data/queries.json` file that you want MAP answers to
2. Run `python pgmpy_answers.py data/queries.json data/answers.json` to get the answers to the queries from Pgmpy
3. Run the tests in `test_map.py` by running entering `pytest` on the terminal in the root folder of the project. This will run your MAP implementation with the queries in `data/queries.json` and compare your answers to those in produced by Pgmpy in `data/answers.json`. If you don't have `pytest` installed you can install it using `pip install pytest`.