# STEPS
# [*] install pg_cron on server => 
    select name, comment, default_version, installed_version
    from pg_available_extensions
    where name = 'pg_cron';

# [*] Turn on extension by running 
    create extension if not exists pg_cron;

# [*] Run this command on terminal
    select
    cron.schedule(
        'cron-name', -- name of the cron job
        '*/10 * * * *', -- every minute
        $$
        -- Put your code between two dollar signs so that you can create full statements.
        -- Alternatively, you can write you code in a Postgres Function and call it here.
        dbname="hilt"
        username="hilt_user"
        psql $dbname $username << EOF
        begin;
        DELETE FROM hilt_annotation_globalexplanationdictionary
        DeLETE FROM hilt_annotation_localexplanationdictionary
        commit;
        $$
    );


# [*] To delete the cron job
    SELECT * FROM cron.job;
    SELECT cron.unschedule(1);





# reference: https://supabase.com/blog/postgres-as-a-cron-server

more references:
1. https://stackoverflow.com/questions/11250590/cron-job-to-remove-old-data-from-postgres-on-debian
2. https://dba.stackexchange.com/questions/142134/routinely-deleting-aged-postgresql-rows-via-cron