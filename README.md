# colabctl v0.2.1

Task executioner &amp; controller for Google Colaboratory notebooks. Google Colaboratory is a game-changing innovation.
It allows anyone to access powerful hardware for machine learning, for free. Unfortunately, it's not possible to run
colab notebooks programmatically or otherwise in the background unless you leave your browser running. Colabctl is a
sort of shim that solves this problem by using headless Selenium.

## BROKEN NOTICE

After realizing a few issues being submitted, I reran the code and saw that there are a few new issues due to Google
changing their code. I'm now working to correct them. It shouldn't take too long, depending on what exactly they've
done.

## TODOs

- [ ] Resolve issues TensorTom/colabctl#1 TensorTom/colabctl#2 TensorTom/colabctl#3 TensorTom/colabctl#4
- [ ] Async execution of tasks.
- [ ] Proper module structure for user command install via pip.
- [ ] Better args parsing.
- [ ] Revise & refactor the Seleium code.
- [ ] Proper logging.

Pull requests welcomed.

## Usage
First, add your Colaboratory URLs to `notebooks.csv`.

In colab, go to `tools -> keyboard shortcuts` and set "Clear all outputs" to `CTRL + SHIFT + Q`

In colab, go to `tools -> keyboard shortcuts` and set "Reset all runtimes" to `CTRL + SHIFT + k`

At the end of your notebook, add: `print("forkin"+"me")`

Now you're ready:

`python colabctl.py <end-string> <sleep-seconds>`

Example:

`python colabctl.py forkinme 1800`

## Important!!!

Notice that the example delay is 1,800 seconds (30 minutes). Please **DO NOT poll Google Colaboratory frequently**.
We're very lucky to have these notebooks and even luckier that this ctl is even possible. Please don't push them to
block us from doing this.

Thank you
