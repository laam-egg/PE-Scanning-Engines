# ClamAV usage

For Ubuntu, Mint and derivatives.

## Official Docs

<https://docs.clamav.net/Introduction.html>

## Installation

```sh
sudo apt update
sudo apt install clamav clamav-daemon
```

## Scan Single File Once

```sh
clamscan "/path/to/file"
```

But it is slow since it has to load all the signatures into RAM
each time it's run.

## Scan Multiple Files Fast

Run this command and wait 2 minutes.

```sh
sudo systemctl restart clamav-daemon
```

Then check with

```sh
sudo systemctl status clamav-daemon
```

If it's still "inactive (dead)", try rerun the `restart` command
above, and check the status again till it is "active (running)".

Then, we are ready to scan:

```sh
clamdscan "/path/to/file"
```

If that fails, try:

**Solution 1:** Quick test. Only use if you're in a hurry.

```sh
clamdscan --fdpass "/path/to/file"
```

**Solution 2:** Fix the root cause: file's ownership and permissions.

First, check *your group*:

```sh
id -gn
```

Then, check the file's group:

```sh
ls -la /path/to/file
```

which should show something like

```sh
-rw-rw-r-- 1 user group 28864 Oct 15  2023 /path/to/file
```

Pay attention to the "group" column: if it is the same as
*your group*, then you're good to go. In fact this is the
expected scenario: you downloaded the file so it is gonna
belong to the same group as you.

Ok, now add the `clamav` user (which is the user on whose
behalf the clamav daemon is run) to the same group.

```sh
sudo usermod -aG your_group clamav
newgrp your_group
```

Restart the daemon

```sh
sudo service clamav-daemon restart
sudo service clamav-daemon status
```

And rerun the command to verify.

```sh
clamdscan /path/to/file
```

First run might appear slow, but subsequent ones should not!
