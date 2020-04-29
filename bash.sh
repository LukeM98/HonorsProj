#!/bin/sh


cd ~/Documents/LucasMartinHonors

echo "Running program with $1 processors"
 mpiexec -n $1 -oversubscribe python3 parallel.py
sudo su

