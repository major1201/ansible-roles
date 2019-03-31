prompt_cmd() {
    local EXIT="$?"
    PS1=""
    local END='\[\e[0m\]'
    local RED='\[\e[0;31m\]'
    local GRE='\[\e[0;32m\]'

    if [ ${EXIT} != 0 ]; then
        PS1+="${RED}"
    else
        PS1+="${GRE}"
    fi  
    PS1+="[\u@\H \t]\W\\$ ${END}"
}
PROMPT_COMMAND=prompt_cmd
