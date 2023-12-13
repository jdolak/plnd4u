# Developer Wiki

## Getting Started

#### Prerequisites
* This project runs as containers so docker is required on the host machine
  * It is possible to run this without containers but requires addtional setup that will not be covered
* This repository cloned with the repository base directory as your current working directory
* Deploying on remote servers automatically requires anisble installed on the local machine


#### Inital start
1. `.env` files are used for secrets, run `echo "MYSQL_ROOT_PASSWORD=your_password_here" > ./src/.env"` to create this file
   * This will be the password for you MySQL database when you log into mysql later
   * Optionally add the line `DEPLOY_ENV=prod` to the end of this file if this system is intended for a production environment
2. Also append the pepper with `echo "PEPPER=your_random_string_here" >> ./src/.env"` to add a pepper for password hashing
   * This should be a random string that will be used to enhance password security
2. Run `make up` to start the inital build process for the the flask app
3. After the image is built, the database and flask containers will configure and start to run, however the data in the database still needs to be populated

### Quick Start

1. Run `make configure`

### Manual Start

#### Configuring the database
1. From the base directory of the repository run `make db-term` to enter the shell of the database container
2. First, the database needs to be created in MySQl, so run `mysql -p` to enter MySQL's shell
3. Execute `CREATE DATABASE plnd4u;` and return to the shell by typing `exit`
4. From the container's shell, import the data into the new database by running `mysql -u root -p plnd4u < /mnt/data/dump.sql`
5. The database should now be populated, you can use `make db-term` again to check if the import was done correctly

#### Finalizing
1. At this point the application stack is set up but it is recommened to do `make down && make up` to resart the stack to reset any exponetial timeouts that may have occured during the database setup
2. The app should now be serving on `localhost` on port 80
3. To use most of plnd4u's features, an account is required, so head to [http://localhost/register](http://localhost/register) to create an account

## Useful commands

#### Importing a sql dump into database

1. From the base directory of the repository run `make db-term` to enter the shell of the database container
2. Run `mysql -u root -p plnd4u < /mnt/data/dump.sql` in the new shell, replacing dump.sql with the dump file that you want
