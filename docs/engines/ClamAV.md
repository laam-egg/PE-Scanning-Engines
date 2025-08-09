# ClamAV usage

For Ubuntu, Mint and derivatives.

## Official Docs

<https://docs.clamav.net/Introduction.html>

## Installation

```sh
sudo apt update
sudo apt install clamav clamav-daemon
```

## Utilities

I wrote [a small script named `scan_exe`](../../src/ClamAV/scan_exe.py)
which uses `clamdscan` under the hood to scan `.exe` files
under a directory recursively. Install Python 3.12 and
you could use it like this:

```sh
python scan_exe /path/to/dir/to/scan
```

The following sections describe the ClamAV tools
in detail.

## Clamscan

```sh
clamscan "/path/to/file"
clamscan --recursive --follow-dir-symlinks=2 --follow-file-symlinks=2 "/path/to/dir"
```

Each time `clamscan` runs, it has to load all the signatures into
RAM before inference. For (recursive) directory scanning, this is
fine. But for single file scanning, that is slow.

## Clamdscan

This sends the file over to a running daemon server, so for scanning
a single file once, this is the fastest. But first, we need to get
the daemon running. Run this command:

```sh
sudo systemctl restart clamav-daemon
```

Then check with

```sh
sudo systemctl status clamav-daemon
```

If it's still "inactive (dead)", try rerun the `restart` command
above, and check the status again till it is "active (running)".
You might even have to wait some minutes after issuing a `restart`
command before checking it with `status`.

Then, we are ready to scan:

```sh
clamdscan "/path/to/file"
```

Or scan multiple files:

```sh
clamdscan "/path/to/dir"
```

Beware, `clamdscan` on your system might not support the `--recursive`
flag, in which case, it can only scan files right under the specified
directory, but *not any deeper*. For that, try `clamscan` instead.

If `clamdscan` fails due to some `Permission denied` error, try:

**Solution 1:** Quick test. Helpful if you're in a hurry.

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

However, this solution is not foolproof. If you get to
scan files that are owned by another user or having
too restrictive permissions, the tool might still fail.
In that case, try solution 1 (`--fdpass`) or fall back
to `clamscan`.
