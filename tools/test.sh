#!/bin/zsh

# Convert the _ephemeral/test_data fixtures across each supported type group and
# verify the results, exercising the sleepyconvert CLI end to end.
#
#   data : test.<ext> -> from_<ext>.csv        (every data format -> csv)
#   img  : img.<ext>  -> from_<ext>.<other>    (each image format -> the other)
#   doc  : test.<ext> -> from_<ext>.md         (every document format -> md)
#
# Output lands in _ephemeral/test_output/. Same-format conversions are no-ops
# and are skipped.
#
# Usage:
#     ./tools/test.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="${ROOT_DIR}/_ephemeral/test_data"
OUT_DIR="${ROOT_DIR}/_ephemeral/test_output"

mkdir -p "${OUT_DIR}"

# Prefer the installed console script; fall back to running the module.
if command -v sleepyconvert >/dev/null 2>&1; then
	CONVERT=(sleepyconvert)
else
	CONVERT=(python -m sleepyconvert.main)
fi

failures=0

runConvert() {
	local src="$1"
	local out_name="$2"
	echo "Converting ${src##*/} -> ${out_name}"
	if ! "${CONVERT[@]}" "${src}" "${OUT_DIR}/${out_name}"; then
		echo "  FAILED: ${src##*/} -> ${out_name}" >&2
		failures=$((failures + 1))
	fi
}

# convertAllTo <target-ext> <source>...: convert each source to the target
# format, skipping any source that is already in the target format.
convertAllTo() {
	local target="$1"
	shift
	local src ext
	for src in "$@"; do
		ext="${src##*.}"
		if [[ "${ext}" == "${target}" ]]; then
			continue
		fi
		runConvert "${src}" "from_${ext}.${target}"
	done
}

# Data: every data fixture -> csv.
convertAllTo csv "${DATA_DIR}"/test.{csv,json,parquet,pkl,xlsx}

# Doc: every document fixture -> md.
convertAllTo md "${DATA_DIR}"/test.{html,md,pdf}

# Image: each image fixture -> the other raster format.
runConvert "${DATA_DIR}/img.png" "from_png.jpg"
runConvert "${DATA_DIR}/img.jpg" "from_jpg.png"

if ((failures > 0)); then
	echo "${failures} conversion(s) failed." >&2
	exit 1
fi

echo "All conversions succeeded."

echo "Verifying outputs against sources..."
python "${ROOT_DIR}/tools/_verify_test.py"
