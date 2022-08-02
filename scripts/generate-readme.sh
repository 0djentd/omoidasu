#!/usr/bin/env bash

rm README.md
cp README.template.md README.md

function generate_readme() {
    function generate_readme_for_command () {
       echo '```'
       eval "poetry run omoidasu $1 --help"
       echo '```'
       echo ''
    }
    
    commands=('list' 'review' 'add' 'new')
    
    echo '```'
    poetry run omoidasu --help
    echo '```'
    echo ''

    for command in ${commands[*]}
    do
        generate_readme_for_command "$command"
    done
}

generate_readme >> README.md
