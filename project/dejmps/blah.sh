#!/bin/bash
cd ~/CS4090/project/dejmps || exit
echo > .out
netqasm simulate | cat >> .out | sed -i "s/    fidelity: 1.0/    fidelity: 0.0/g" network.yaml


