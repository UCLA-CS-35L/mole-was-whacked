# Whack-A-Mole Debugging

![Whack-A-Mole clip art](assets/mole-was-whacked.jpg)

Thank you for helping with <https://github.com/UCLA-CS-35L/whack-a-mole>! Now,
all the moles have been whacked, and I have correct implementations of all of
my algorithms in `src/algo.py`.

It's time to use my algorithms library! I'm trying to write a vending machine
application. However, it's got some problems.

Your goal:

1. Investigating symptoms to reproduce the bug
1. Locating the faulty code
1. Determining the root cause of the bug
1. Implementing and verifying a fix

<!-- markdownlint-disable MD024 -->

## Setup

As a reminder, see <https://github.com/UCLA-CS-35L/whack-a-mole> for setup.

It may be helpful to do `pipenv shell` and run the commands from within this
shell.

## Using the Vending Machine

The source code is found in `src/vending_machine.py`. Notice that it imports
some functions from `algo`. To see instruction on how to run the application,
use `python3 src/vending_machine.py --help`.

The vending machine CSV file (the `file` argument) is provided in
`machine.csv`. The contents of this file are reproduced below (space added):

```text
row, column, name,      price
1,   A,      Chips,     120
1,   B,      Soda,      150
1,   C,      Candy,     80
2,   A,      Gum,       50
2,   B,      Cookie,    100
2,   C,      Chocolate, 200
```

- `row` and `column` encode the cell where it is in the machine
- `name` is the name of the item
- `price` is the price of the item

An example invocation would be as follows:

```sh
$ python3 run src/vending_machine.py machine.csv price Chips
Price of Chips is $120
```

This is correct as the price of the chips in the table is $120.

## Debugging

As a reminder, your goal is to fix the bugs!

| debugging step                              | how                                                              |
| ------------------------------------------- | ---------------------------------------------------------------- |
| Investigating symptoms to reproduce the bug | partially complete; see `tests/test_vending_machine.py`          |
| Locating the faulty code                    | adding breakpoints and running tests in debug mode               |
| Determining the root cause of the bug       | describing what is logically wrong in the code                   |
| Implementing and verifying a fix            | edit the source code in `src/vending_machine.py` and rerun tests |

Here's a step-by-step checklist to do this activity:

- [ ] make a fork of this repository
- [x] find some buggy behavior: this has been done for you!

  - `tests/test_vending_machine.py` is provided to check some potential problems
  - make sure you can describe what each test does!

- [ ] run all the tests
- [ ] for each failing test, go to the corresponding function and add a breakpoint somewhere
- [ ] rerun failing tests in debug mode
- [ ] identify at what point are the variables' values are no longer correct
- [ ] note down a potential fix at each point
- [ ] determine the root cause
- [ ] consider how `src/vending_machine.py` might be refactored to address multiple fixes at once
- [ ] run all the tests

  - ensure your fixes didn't break any existing passing tests!

- [ ] push to your fork and ensure the GitHub CI passes (green check mark)

  - you may need to enable GitHub CI in the "Actions" tab
  - optionally, submit a pull request with a fix!
