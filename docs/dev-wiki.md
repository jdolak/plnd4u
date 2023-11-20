# Developer Wiki

## Useful commands

#### Importing a sql dump into database

1. From the base directory of the repository run `make db-term` to enter the shell of the database container
2. Run `mysql -u root -p plnd4u < /mnt/data/dump.sql` in the new shell, replacing dump.sql with the dump file that you want
