#!/bin/sh
cd ~/CS4090/project/dejmps || exit
netqasm simulate | grep "Fidelity: *" | cat > dejmps.out  # output only the fidelity