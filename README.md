# Crack-Driving-Exam
A Jupyter-based interface for cracking the theoretical test of Chinese driving license exam

# Instructions

Start `exercise.ipynb`:
- Run `select_subject(sub)` and `set_mode(mode, shuffle=False, max_count=10000, offset=0)` before starting, where `mode` can be `'all'` or `'marked'`; use `exam` or `e` to quickstart an exam.
- Commands: `n` (next question), `p` (previous quesion), `m` (mark), `u` (unmark), `s` (show stats).
- Type the answer in lower case, e.g., `a` (for single choice), `t` (for True/False question), `abc` (for multiple choice).

# Acknowledgement

The data is provided by https://github.com/li-xinyang/OS_ChineseDrivingTestQuestionBank.