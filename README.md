# colabctl v0.21
Task executioner &amp; controller for Google Colaboratory notebooks. Google Colaboratory is a game-changing innovation. It allows anyone to access powerful hardware for machine learning, for free. Unfortunately, it's not possible to run colab notebooks programmatically or otherwise in the background unless you leave your browser running. Colabctl is a sort of shim that solves this problem by using headless Selenium.

## Roadmap
Currently, colabctl reads from the file `notebooks.csv` your list of Colaboratory URLs. It runs each notebook (In order, synchronously) and then pauses for a period of n seconds of time before running them again.

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

Notice that the example delay is 1,800 seconds (30 minutes). Please **DO NOT poll Google Colaboratory frequently**. We're very lucky to have these notebooks and even luckier that this ctl is even possible. Please don't push them to block us from doing this.

Thank you
