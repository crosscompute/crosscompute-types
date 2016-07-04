#!/bin/bash
SCRIPT_NAMES="
mindmup-editabletable.js
crosscompute-table.js
"
pushd node_modules/crosscompute-table > /dev/null
cat $SCRIPT_NAMES > index.js
popd > /dev/null
refresh-assets \
    invisibleroads_uploads \
    crosscompute_table
