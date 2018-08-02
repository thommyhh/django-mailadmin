#!/usr/bin/env bash
cmd=$1;
portNeeded=0
case "$cmd" in
    dev|build)
        yarnCmd="yarn $cmd"
        npmCmd="npm run $cmd";
        # Only enable port usage, when running the dev server
        if [ "$cmd" == "dev" ]; then
            portNeeded=1;
        fi
        ;;
    lint*|icons)
        yarnCmd="yarn $cmd"
        npmCmd="npm run $cmd"
        ;;
    setup)
        yarnCmd="yarn"
        npmCmd="npm install"
        ;;
    *)
        echo "Usage:
    ./frontend.sh (dev|build)";
        exit 1;
        ;;
esac

if [ $(which docker) -a -x $(which docker) ]; then
    # If docker was found, start a docker container with nodejs 8.x image and the current directory as /build
    # and run the given command with yarn.
    if [ $portNeeded -eq 1 ]; then
        docker run --rm -ti -v `pwd`:/build -e PORT=3000 -p 3000:3000 node:8 bash -c "cd /build/frontend && $yarnCmd"
    else
        docker run --rm -ti -v `pwd`:/build -v ~/.ssh:/root/.ssh node:8 bash -c "cd /build/frontend && $yarnCmd"
    fi
elif [ $(which yarn) -a -x $(which yarn) ]; then
    # If a local yarn executable is found, run the given cmd with yarn locally
    if [ $portNeeded -eq 1 ]; then
        cd frontend && PORT=3000 $yarnCmd
    else
        cd frontend && $yarnCmd
    fi
elif [ $(which npm) -a -x $(which npm) ]; then
    # If local npm executable is found, run the given command with npm locally
    if [ $portNeeded -eq 1 ]; then
        cd frontend && PORT=3000 $npmCmd
    else
        cd frontend && $npmCmd
    fi
else
    echo "Neither docker nor yarn nor npm was found on your system. You cannot run, this frontend build."
    exit 1;
fi
