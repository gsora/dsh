#`dsh`: dumb shell

#### What is this?
This is the result of some hours spent alone with Python3, and a book about Operating Systems structure.
It's a shell, or at least *sort of*.

Using Python3 with `subprocess`, `signal` and `os` here's a working implementation of a system shell.
No scripting, no TAB completion, nothing.

After all, it's only a **proof of concept**.

#### How to use it

Clone this repo, then

	cd the-folder-you-cloned-into
	python3 ./dsh.py
	
and have fun!

#### Configuration file

The default configuration file must be placed into your home, named as `.dshrc`.
See `dshrc.example` to understand how to configure it.