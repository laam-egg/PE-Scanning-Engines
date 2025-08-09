# KicomAV

For Ubuntu, Mint and derivatives.

## Official Docs

<https://www.kicomav.com/>

Beware that the installation instruction in this home page
has been outdated, check out the `README.md` in the GitHub
repository at `https://github.com/hanul93/kicomav.git`.

## Installation

Steps 1, 2, 3 could be conducted **at the same time** (for saving time,
not a hard requirement). You should only move forward to step 4 and
beyond **after** completing all those previous steps.

1. Prepare the Python environment. You could replace `mamba` with `conda`
    in the commands below.

    ```sh
    mamba create -n kicomav python=3.8
    mamba activate kicomav
    mamba install -c conda-forge backports.lzma
    pip install pylzma
    ```

    It might also support Python up to `3.11` but I haven't test it out.
    Python 3.12 and later is certainly not supported, since KicomAV
    build tool makes use of the `imp` module, which was deprecated in
    Python 3.4 and completely removed in Python 3.12.

2. Compile and install YARA. See [Appendix A](#appendix-a-compile-and-install-yara).
    At the time of this writing, I was using yara 4.5.4 (and yara-python 4.5.4
    too, in step 4).

3. Clone the repo:

    ```sh
    git clone https://github.com/hanul93/kicomav.git
    ```

    The website suggests running `git clone git://github.com/hanul93/kicomav.git`
    but that actually does not work (at least for me).

4. Now that you've installed YARA, time to install the last
    Python dependency, `yara-python`.

    ```sh
    mamba activate kicomav
    pip install yara-python
    ```

5. The preparation for building KicomAV is done. Let's build it!
   
    ```sh
    mamba activate kicomav
    ./build.sh build
    ```

6. **IMPORTANT:** Fix the bugs in the `k2.py` file we've just built.
    See [Appendix B](#appendix-b-fix-bugs-in-k2py).

7. Update the malware signatures. See guide and notes on update
    in the [Usage](#usage) section.

## Usage

Be sure to run the following commands first
before using KicomAV:

```sh
mamba activate kicomav
cd $KicomAV_REPO_ROOT_DIRECTORY
cd Release/
```

Displaying help:

```sh
python k2.py
```

Update malware signatures (though you **should not** do this,
since the authors' update database contains update packages
for Python 2 only! Upon installation, all the signatures have
been built for you. So no need to run the update; however,
if you manage to update and then scan any PE file without
errors, please share your method!):

```sh
python k2.py --update
```

Scan single file:

```sh
python k2.py /path/to/file
```

Scan files in a directory:

```sh
python k2.py /path/to/dir -I
```

## Appendix A: Compile and install YARA

Based on official docs at
<https://yara.readthedocs.io/en/latest/gettingstarted.html>.

Steps 1 and 2 could be conducted **at the same time** (for saving
time, not a hard requirement). Still, only move forward to step 3
**after** completing all those previous steps.

1. Visit <https://github.com/VirusTotal/yara/releases> and download
    a release's *source code* archive, preferably `.tar.gz`.

2. Install the necessary tools for building YARA from source.
   
    ```sh
    sudo apt-get install automake libtool make gcc pkg-config
    # For enabling extensions in ./configure below
    sudo apt-get install libssl-dev libmagic-dev
    ```

3. Extract the downloaded archive and `cd` into the directory.
    Run the following commands to build and install YARA.

    ```sh
    ./bootstrap.sh
    ./configure --with-crypto --enable-magic --enable-dotnet
    make
    echo $?
    ```

    If the last command printed `0`, proceed:

    ```sh
    sudo make install
    ```

    Otherwise, something is wrong during the build phase.
    Check it before running the install command, or that
    command will *brick* your system.


4. Run the test cases to make sure everything is fine:

    ```sh
    make check
    ```

    Make sure `PASS` count is equal to `TOTAL` count.

## Appendix B: Fix bugs in k2.py

All the following instruction refer to the file `k2.py`
in `$KicomAV_REPO_ROOT_DIRECTORY/Release` directory.

1. Credit <https://github.com/hanul93/kicomav/issues/32>.
    
    Find the line
    
    ```python
    p_lists = re.compile(rb'([A-Fa-f0-9]{40}) (.+)')
    ```

    and replace it with

    ```
    p_lists = re.compile(r'([A-Fa-f0-9]{40}) (.+)')
    ```

2. Find the line
    
    ```python
    url = 'https://raw.githubusercontent.com/hanul93/kicomav-db/master/update_v3/'  # 서버 주소를 나중에 바꿔야 한다.
    ```

    and replace it with

    ```python
    url = 'https://raw.githubusercontent.com/hanul93/kicomav-db/refs/heads/master/update_v3/'
    ```
