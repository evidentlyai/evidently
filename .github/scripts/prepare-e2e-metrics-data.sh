#!/usr/bin/env bash
set -e

becho() {
  echo -e "\033[36m$*\033[0m"
}

ipynb_pattent="examples/*/metrics.ipynb"
ui_e2e_folder="ui/e2e-tests-for-metrics"

rm -rf $ui_e2e_folder/dist example_scripts

becho convert notebooks to python #

jupyter nbconvert --to python \
  $ipynb_pattent --output-dir example_scripts


becho transform output to save html #

for file in example_scripts/*
do
  echo "prepare: $file"

  filename=$(basename $file)
  file_dist="$ui_e2e_folder/dist/$filename"

  mkdir -p $file_dist

  cp $file $file_dist
  node .github/scripts/transform-jupyter-python.mjs $file_dist/$filename

done

becho generate html #

for folder in $ui_e2e_folder/dist/*
do
  (
    cd $folder

    filename=$(ls .)
    echo "run: $filename"
    PYTHONWARNINGS="ignore" python $filename && rm $filename
  ) &
done

becho wait running python scripts #
wait

becho write test config #
for folder in $ui_e2e_folder/dist/*
do
  key=$(basename $folder)
  files=$(ls $folder | jq -R . | jq -s .)
  echo "{\"$key\": $files}"
done | jq -s 'add' > $ui_e2e_folder/config.json

becho done #
