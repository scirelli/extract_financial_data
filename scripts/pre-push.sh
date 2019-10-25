#!/usr/bin/env bash
set -o errexit -o pipefail -o noclobber -o nounset

make lint
make test
