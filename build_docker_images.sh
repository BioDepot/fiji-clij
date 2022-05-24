#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "WARNING: You are not root; you may not be permitted to access the Docker daemon, causing an error."
    echo "  If this occurs, re-run this script as root."
    echo ""
fi

if [ -z "$NOSLEEP" ]; then
    echo "Assuming you are in the root directory of the repository"
    echo "Press CTRL+C now if this is not the case, and re-run this script from the root directory of the repository"
    sleep 5
    echo "Continuing..."
fi

ORIG_DIR="$(pwd)"

function build_container () {
    WIDGET_NAME=$1
    DOCKER_IMAGE=$2
    DOCKER_TAG=$3

    cd "clij_benchmarking_workflow/widgets/clij_benchmarking_workflow/$WIDGET_NAME/Dockerfiles"
    docker build -t "$DOCKER_IMAGE:$DOCKER_TAG" .
    cd "$ORIG_DIR"
}

build_container "jupyter_stats" "biodepot/jupyter-stats" \
		"5.6.0__ubuntu-18.04__firefox-61.0.1__081318"
build_container "fijiOCL" "biodepot/fiji-ocl" \
		"20201104-1356__update20211210__ubuntu_20.04__1fa37497"
build_container "downloadImages" "biodepot/python3-download" \
		"3.6.3-r9__alpine-3.7__min__081418"

