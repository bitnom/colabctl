# colabctl
Task executioner &amp; controller for Google Colaboratory notebooks. Google Colaboratory is a game-changing innovation. It allows anyone to access powerful hardware for machine learning, for free. Unfortunately, it's not possible to run colab notebooks programmatically or otherwise in the background unless you leave your browser running. Colabctl is a sort of shim that solves this problem by using headless Selenium.

## Roadmap
The first and current version simply runs a colaboratory notebook and prints the output. The next version will use threading to manage an arbitrary number of notebooks as a proper ctl.
