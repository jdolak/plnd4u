# PLND4U (Planned For You)

### Project Description

 PLND4U is a four-year planner that allows students to search courses that have been taught in past semesters at Notre Dame, and assign them to openings in their personal eight-semester plan. PLND4U will consider the major requirements of its user, as well as the prerequisites/corequisites of the selected courses, and inform the user if their four-year plan is valid.

## Getting Started

### Prerequisites

PLND4U runs as a container and Docker is required before installing. Information on how to do that can be found [here](https://docs.docker.com/get-started/get-docker/).

### Quick start:

For a quick start we will launch PLND4U on port 80 and using sqlite.

1. Pull our docker image:
```
docker pull jdolakk/plnd4u
```

2. To make the sqlite data persistant we must add a docker volume:
```
docker volume create plnd4u-data
```

3. Launch the container:
```
docker run -d -p 80:80 -v plnd4u-data:/plnd4u/data/sqlite
```

4. Visit the website on port 80:  
http://localhost

### More Options

For building the docker image, manual installation, or more options, vistit the [dev wiki](docs/dev-wiki.md)

## Contributing

Feel free to contribute to this project by creating an issue or pull request. For infomation about this codebase and how to get started, vist the [dev wiki](docs/dev-wiki.md)

New feature requests are also welcome.  

For any help, questions, or just to say hi, join our [discord server](https://discord.gg/wjR9znjZYS).




## Authors

Jachob Dolak [Maintainer]  
Sam Martin  
Andrew Myers  
Calista Suwita
