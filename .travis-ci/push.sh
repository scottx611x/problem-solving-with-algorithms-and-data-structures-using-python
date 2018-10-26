#!/bin/sh

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
  git remote rm origin
  git remote add origin-master https://${GH_TOKEN}@github.com/scottx611x/problem-solving-with-algorithms-and-data-structures-using-python.git
}

commit_coverage_files() {
  echo "Checkout master"
  git checkout master
  
  echo "Pull master"
  git pull

  echo "Add Coverage"
  git add coverage

  echo "Commit"
  git commit -m "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  echo "Push"
  git push
}

setup_git
commit_coverage_files
upload_files