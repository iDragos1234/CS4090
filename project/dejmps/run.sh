#!/bin/bash
cd ~/CS4090/project/dejmps || exit

netqasm simulate | cat > .out

sed -i "s/    fidelity: 1.0/    fidelity: 0.0/g" network.yaml



#echo > dejmps.out  # remove any existing contents in the output file
#for (( i = 1; i <= 5; i++ ))
#do
#  netqasm simulate | grep "Fidelity: *" | cat >> dejmps.out  # output only the fidelity
#done

#echo > dejmps.out  # remove any existing contents in the output file
#for (( i = 1; i <= 5; i++ ))
#do
#  netqasm simulate | grep "Fidelity: *" | cat >> dejmps.out  # output only the fidelity
#done

