# Developer Wiki

## Getting Started

#### Configuring the database
1. From the base directory of the repository run `make db-term` to enter the shell of the database container
2. First, the database needs to be created in MySQl, so run `mysql -p` to enter MySQL's shell
3. Execute `CREATE DATABASE plnd4u;` and return to the shell by typing `exit`
4. From the container's shell, import the data into the new database by running `mysql -u root -p plnd4u < /mnt/data/dump.sql`
5. The database should now be populated, you can use `make db-term` again to check if the import was done correctly

## Useful commands

#### Importing a sql dump into database

1. From the base directory of the repository run `make db-term` to enter the shell of the database container
2. Run `mysql -u root -p plnd4u < /mnt/data/dump.sql` in the new shell, replacing dump.sql with the dump file that you want
