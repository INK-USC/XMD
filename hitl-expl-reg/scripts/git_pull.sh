#!/bin/bash
cd ..
for i in {0..46}
do
   echo "Running git pull for expl-reg_$i..."
   cd expl-reg_$i; git pull; cd ..
   echo ""
done