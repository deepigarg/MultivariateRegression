#!bin/bash

awk 'BEGIN{FS=";"} FILENAME == "ImpactF" { remember[$1]=$3; } FILENAME != "ImpactF" { if ( $3 in remember ) print $3 ";" $6 ";" $8 ";" $9 ";" $10 ";" $11 ";" $12 ";" $13 ";" $14 ";" $15 ";" remember[$3] ;} ' ImpactF Scimago >> Extracted.txt

