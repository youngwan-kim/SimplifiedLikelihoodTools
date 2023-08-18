#!/bin/bash
directory="./Datacards"

cards=("$directory"/*.txt)
mkdir -p Rootfiles 

for card in "${cards[@]}"; do
    if [ -f "$card" ]; then
        cardname=$(basename "$card")          # Extracts the filename
        rawname="${cardname%.*}"
        echo "Making workspace for datacard: $cardname"
        text2workspace.py --X-allow-no-signal --X-allow-no-background $card
        echo "Running FitDiagnostics for datacard: $cardname"
        combine -M FitDiagnostics --saveShapes --saveWithUnc --numToysForShape 2000 \
        --saveOverall --preFitValue 0  "Datacards/${rawname}.root" --name ${rawname} 
        cp "fitDiagnostics${rawname}.root" "Rootfiles/fitDiagnostics_${rawname}.root"
    fi
done
