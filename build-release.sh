#!/bin/bash

PROGRAM="mycv"
VERSION="${VERSION:-latest}"
STDOUT="$(mktemp -q -p /tmp -t mycv-build-XXXX)" || exit 2
STDERR="$(mktemp -q -p /tmp -t mycv-build-XXXX)" || exit 2
ROOTDIR="$(dirname $0)"
FILENAME="${PROGRAM}-${VERSION}.tar.gz"

TAREXCLUDE="--exclude=./data --exclude=.git --exclude=.gitignore --exclude=./src/__pycache__ --exclude=.vscode --exclude=./${FILENAME}"
rm -f ${ROOTDIR}/${FILENAME}
TARCMD="/usr/bin/tar -C ${ROOTDIR}/ -czvf ./${FILENAME} ${TAREXCLUDE} --owner=root --group=root ${ROOTDIR}/"

# echo "Intending to build ${FILENAME} using command: ${TARCMD}"
# echo "Redirecting STDERR to ${STDERR} and STDOUT to ${STDOUT}"
${TARCMD} 2>${STDERR} >${STDOUT}

RETURNCODE=$?

if [[ "${RETURNCODE}" -eq "2" ]]; then
  echo "ERROR! Failed to create ${FILENAME}"
  echo ""
  $(cat ${STDERR})
fi

# finally clean up the tempfiles created and exit using the tar cmd returncode
rm -f ${STDOUT}
rm -f ${STDERR}

exit ${RETURNCODE}
