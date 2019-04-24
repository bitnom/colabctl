# colabctl
Task executioner &amp; controller for Google Colaboratory notebooks. Google Colaboratory is a game-changing innovation. It allows anyone to access powerful hardware for machine learning, for free. Unfortunately, it's not possible to run colab notebooks programmatically or otherwise in the background unless you leave your browser running. Colabctl is a sort of shim that solves this problem by using headless Selenium.

## Roadmap
The first and current version simply runs a colaboratory notebook until the text is detected, waits and runs the notebook again. Currently having trouble detecting the forkinme string. Run to see what I mean. The next version will use threading to manage an arbitrary number of notebooks as a proper ctl.

**usage:** `python colabctl.py forkinme 1800 https://colab.research.google.com/drive/yournotebookurl`

**At the end of the notebook:** `print("forkin"+"me")`

Pull requests welcomed.

## Important!!!

Notice that the example delay is 1,800 seconds (30 minutes). Please **DO NOT poll Google Colaboratory frequently**. We're very lucky to have these notebooks and even luckier that this ctl is even possible. Please don't push them to block us from doing this.

Thank you
