#!/bin/bash -x

# Start all projects/external projects with all configs.

set -x

pedl_opts=$@

projects=$(ls -d -- examples/official/*/)

for project in $projects; do
  ls $project/*.yaml | xargs -n1 -I{} pedl $pedl_opts e create {} $project
done
