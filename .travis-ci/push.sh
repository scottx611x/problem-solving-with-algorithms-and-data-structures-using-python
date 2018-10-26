#!/bin/sh

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
  git remote rm origin
  git remote add origin-master https://${GH_TOKEN}@github.com/scottx611x/problem-solving-with-algorithms-and-data-structures-using-python.git
}

commit_coverage_files() {
  git add coverage
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git push --force --set-upstream origin-master master 
}

setup_git
commit_coverage_files
upload_files