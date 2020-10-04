# example-git-actions-docker-openmc

This is a minimal example showing use of github actions to build a docker image containing openmc and perform simulation tests when there are changes to the repository source code.

The Action is currently triggered on pull requests or pushes to the main branch but can be rolled out to include other branches as well.

The automated continuous integration (CI) testing process takes about 20 minutes to report if the simulation values are as exspected.

The status of the git action can be reported via a badge [![ActionsCI](https://github.com/shimwell/example-git-actions-docker-openmc/workflows/CI/badge.svg)](https://github.com/Shimwell/example-git-actions-docker-openmc/actions?query=workflow%3ACI)
