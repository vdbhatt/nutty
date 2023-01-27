# About

An educational RISC-V processor written tested and deployed on FPGA only using python libs.
If you are interested in computer architecture especially CPU and want to be in python land
this project might help you.

In this repo you'll find tutorial on how to build such CPU, verify it and run c code on it to blink some LEDs
I'll try to explain major blocks and how they are connected , what steps


# Acknowledgement:
First things first

Big thanks to following open source projects without which it would be not so easy to build this fun project
(in no particular order)

* [lambdaconcept](https://github.com/lambdaconcept)
* [amaranth-lang](https://github.com/amaranth-lang)
* [RobertBaruch](https://github.com/RobertBaruch/amaranth-tutorial)
* [minerva](https://github.com/minerva-cpu/minerva)
* [litex / enjoy-digital](https://github.com/enjoy-digital)


without their work I would be forced to write all of this in verilog. It is not easy to pick up if you have never designed any significant project already.

# Installation

* Clone the repo
* pull riscof verification image
    ```
    docker pull registry.gitlab.com/incoresemi/docker-images/compliance
    ```
* Open vscode in the docker, if not already known simply click on bottom left and from menu select re-open in container. If having difficulty here is [link](https://code.visualstudio.com/docs/devcontainers/containers) for tutorial. I've provided the .devcontainer file with image set to riscof docker image.

* update pip
    ```
    pip install --upgrade pip
    ```
* Big thanks to folks at lambdasoc Minerva as we will use components released by these projects. By using peripherals from lambdasoc you'll also learn how easy it is to use components developed by community. Other cools set of libraries I found are at litex project. We could also write our own components but in the end it would not be too different and anyway our focus is the CPU, other cool things we use from  open source projects and acknowledge them. Don't forget to star and follow these cool projects.


* Follow the [setup](https://github.com/lambdaconcept/lambdasoc) of lambdasoc - we need it for SRAM Peripheral, it will also install Minerva from which we will use registers. Below is copy of install instructions from their repo
    ```
    mkdir github_repos ; cd github_repos
    git clone https://github.com/lambdaconcept/lambdasoc
    cd lambdasoc
    git submodule update --init --recursive

    pip install -r requirements.txt
    python setup.py install
    ```

* Okay, external dependencies are installed now we move to Nutty
    cd into it and install
    ```
    pip install -r requirements.txt
    pip install -e . # notice -e for developer install.
    ```
* Install iverilog, and bsdmainutils we need it for simulation.
    ```
     apt-get update
     apt-get install bsdmainutils iverilog -y
    ```
* Running compliance test

navigate to  ``` test/rv_compliance ``` and run
    ```
    python run_tests.py
    ```
 it will take ~15-20 minutes but in the end you should see a list of 39 passing tests!

**Mission accomplished**, you have a risc-v core passing RV32I compliance tests.

* Setup is complete and it's time to replicate / understand how all this works

* Start with docs/nutty.md in the repo for understanding how it is built.

# LICENSE:
2 clause BSD, feel free to use in any educational endevour.


# FUTURE
* At some point I'll create short video series to describe it.
* Also release a pipelined version (which i have currently only in verilog, so translation is in progress)
* a Dual issue in order variant capable of running linux
* Cover more extensions especially M,CSR,F
* Add DRAM interface (most likely litex dram )
* instantiate 2-4 of these cores to create a MPSoC
* dedicated HW for cool things such as encryption AV etc.

I'll prioritize as per the request or whenever I'll get time ;)