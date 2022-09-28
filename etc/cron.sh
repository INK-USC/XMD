#!/bin/sh

dbname="hilt"
username="hilt_user"
psql $dbname $username << EOF
# begin;
# DELETE FROM links_groupseen WHERE which_reply_id IN (SELECT id FROM links_reply where "submitted_on" < now() - interval '7 days');
# DELETE FROM links_reply WHERE "submitted_on" < now() - interval '7 days';
# commit;
# begin;
# DELETE FROM links_vote WHERE link_id IN (SELECT id FROM links_link WHERE id NOT IN (select answer_to_id from links_publicreply) AND "submitted_on" < now() - interval '1 hour');
# DELETE FROM links_photoobjectsubscription WHERE which_link_id IN (SELECT id FROM links_link WHERE id NOT IN (select answer_to_id from links_publicreply) AND "submitted_on" < now() - interval '1 hour');
# DELETE FROM links_link WHERE id NOT IN (select answer_to_id from links_publicreply) AND "submitted_on" < now() - interval '1 hour';
# commit;
EOF

# https://dba.stackexchange.com/questions/43937/how-to-run-recurring-tasks-on-postgresql-without-an-external-cron-like-tool
In default setup, you can just do this:

$ sudo -u postgres crontab -e
In the editor, add to the crontab entry like so:

0    0    *     *    * bash /path/to/run_stored_procedure.sh
and in your /path/to/run_stored_procedure.sh file you simply just use psql to call your stores procedure

#!/usr/bin/env bash
psql my_db_name <<END
    SET ROLE limited_user;
    SELECT my_stored_proc();
    SELECT 1 FROM my_stored_proc();
END
