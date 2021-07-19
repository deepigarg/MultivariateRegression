#!bin/bash

awk 'BEGIN{FS=";" ; min=10}$3<min{minc=$1; min=$3;} END{print minc " " min}' Output.csv

awk 'BEGIN{FS=";" ; min=10}$2<min{minc=$1; min=$2;} END{print minc " " min}' Output.csv

