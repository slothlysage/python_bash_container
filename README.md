# Intel Deep Learning Systems Coding Challenge #

You are to build and make a deployable, containerized service that
executes and processes valid shell command strings.

Your service listens for POST requests at a specified endpoint
containing a multi-part encoded file parameter.  You will parse this
file to determine the set of valid commands to be executed.  We've
included an example `commands.txt` file in this repository so you can get a
sense of how it will be formatted. 

After executing each valid command, you'll store the command output and other
meta-data in a database so that this information can later be queried or
displayed.

To help get you started we've provided some skeleton code and fleshed out a few
of the basic details.  We've left TODO's in places that will need
to be completed for the service to work, and have outlined some of the specific
tasks in more detail below.  That being said, we've intentionally kept this
project fairly open-ended and would love to see what you come up with!  Feel
free to extend and modify any of the code as you see fit and be sure to
document your decisions (add new text files directly to the repo).

For someone with basic python and Docker familiarity we feel that a
working solution can be put together in a few hours (though we'll give you a
week to work on it).  

We expect you to fork this initial repository to do your work, then send us a
link to that when you are ready for us to test and review it.

**Good luck!**


## Implementation Specifics ##

- You may assume that every command list file is UTF-8 plain-text formatted
  into two sections denoted by the headers `COMMAND_LIST` and `VALID_COMMANDS`.
  The former are the list of command strings to be executed (one per line), and
  the latter represent the list of valid command strings.
  - There must be an exact, case-sensitive match of the entire command list
    command string in the valid command section for it to be considered
    "valid" and available for execution.
  - Invalid commands should be ignored.
  - You are provided one `commands.txt` example file, but your solution should
    be able to accept other files as input as well that are of the same
    structure.
  - Each file is independent and self-validating; i.e. the `VALID_COMMANDS`
    section of one file doesn't affect what's valid in another file.
  - You may assume the entire command file fits into memory.
- For every valid command, you need to execute it and store the following
  meta-data:
  - actual command itself as a string
  - length of command string
  - time to complete (if the command takes > 1 minute to complete, mark a 0
    value which will represent a "long running or not finished" scenario.
  - stdout output from executing the command.
- Do not store duplicate commands (you can assume a command with the same input
  command string will produce the exact same output).
- The command meta-data will be persisted in the db provided (you may assume
  the db is already created at time processing starts).
- Users can query the command meta-data that has been stored to date by hitting
  the endpoint specified in the code with a GET call.  You may assume that the
  amount of data to be returned in these queries is small enough to return all
  at once (though a solution that supports pagination or extended query options
  would be a great bonus feature)
- Think about time and space complexity as you perform command validation.
- Keep in mind edge cases; what about command strings that don't terminate in
  time?
- You may assume that commands that error when executed, or "malicious" command
  strings have been screened out, and will not appear in the `VALID_COMMANDS`
  section.
- Write a few tests for your code as well.
- Finally, when you're done, send us the link to where we can see the code on
  your Github/Bitbucket/etc.


## Running the server ##
You have a couple of options.  To get started it may be easier to get a python
virtualenv environment going first.  To complete the solution though you'll
need to build and start a Docker container that your service runs in.  This is
all driven from the `Makefile` so feel free to start poking around there.

### python virtualenv ###
1. Type `make run_venv` to create and initialize the environment, then start
   the service.

### docker container ###
1. Type `make run_container` to build and start the service inside a container.
   For this to work you'll need to first complete the skeleton `Dockerfile`
   appropriately.

In either case, you should then be able to connect to the web app to either
drop the db, init the db, fetch results, or input data (we recommend using
`curl` from the command line or the `requests` library if you are using python).
   - Sample request to feed in the example data:
     `curl -F "filename=@commands.txt" http://127.0.0.1:8080/commands`



## Some optional Bonus Tasks ##
**Bonus #1:** Assume the filename `commands.txt` file no longer fits in memory.
Tweak your solution to allow for this.

**Bonus #2:** Make the command executions themselves non-blocking.

**Bonus #3:** Change the API so that instead of passing a file formatted with
two sections listing valid commands and the command list, you come up with an
alternative scheme of conveying this information.  Maybe you want to pass these
as arrays?  What are the pros and cons of your chosen API relative to the
original one we provided?

**Bonus #4:** Run each of the commands individually inside their own docker
container. These runs need to be non-blocking (essentially requires bonus #2
above).

**Bonus #5:** From a security perspective, we've made several terrible
assumptions in our code that wouldn't pass muster in a real production setting.
Add a new text document to the repository in which you identify and discuss
some of these problems.  What would you do differently to make this service
more secure?

**Bonus #6:** Assume that invalid, "malicious", or erroring command strings
could exist in the `VALID_COMMANDS` section now; if a "valid" command turns
out to be invalid, treat it as though it were invalid in the first place.
- Definition of "invalid":
    1. returns an error on execution, ex: `ower0weg89245r`
- Definitions of "malicious":
    1. attempts to write anything to /tmp
    2. attempts to delete anything

In general, here are some tools that might prove useful as you work through
some of the bonuses: Redis, Celery, gunicorn, bashlex, htcondor/Kubernetes,
PostgreSQL/MySQL/MongoDB, Docker, cronjobs, python's `schedule` module, bash.
