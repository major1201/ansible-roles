#Fetch username and login ip
declare -x LOGIN_USER=`/usr/bin/who am i | awk '{print $1}'`
declare -x LOGIN_IP=`echo $SSH_CLIENT | cut -f1 -d' '`

#Define promption for root and other users
if [ $USER == root ];then
    declare -x PROMPT="#"
else
    declare -x PROMPT="$"
fi

LAST_HISTORY="$(history 1)"
LAST_COMMAND="$(history 1)"

declare -x logcmd='
CURRENT_HISTORY="$(history 1)"
COMMAND="$(history 1)"
if [ "$LAST_HISTORY" != "$CURRENT_HISTORY" ];then
    LAST_COMMAND="$COMMAND"
    LAST_HISTORY="$CURRENT_HISTORY"
    logger -p local4.notice -i -t $LOGIN_USER $LOGIN_IP "[$USER@$HOSTNAME $PWD]$PROMPT $COMMAND"
fi'

trap "$logcmd" DEBUG
