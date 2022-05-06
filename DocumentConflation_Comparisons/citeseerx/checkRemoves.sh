#!/bin/bash

filename=$1

let remobed=0;

IFS=,
while read line; do {
  
  let removed1=0;
  let removed2=0;
  # split into an array
  fields=( $line )
  doc1=${fields[0]};
  doc2=${fields[1]};

  echo -ne "Checking ${doc1}...";

  let removed1=`wget -q -O -  http://citeseerx.ist.psu.edu/viewdoc/summary?doi=${doc1} | grep -i -e "The document with DOI" -e "has been removed" | wc -l`;
  if [ "$removed1" -gt 0 ]; then
      echo "yes";
  else
      echo "no";
  fi;

  echo -ne "Checking ${doc2}...";
  let removed2=`wget -q -O -  http://citeseerx.ist.psu.edu/viewdoc/summary?doi=${doc2} | grep -i -e "The document with DOI" -e "has been removed" | wc -l`;

  if [ "$removed2" -gt 0 ]; then
      echo "yes";
  else
      echo "no";
  fi;

  if [ "$removed1" -gt 0 ] || [ "$removed2" -gt 0 ]; then
      let remobed=$remobed+1;
  fi;

} done < ${filename}

echo $remobed;