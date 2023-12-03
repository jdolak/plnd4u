# Relational Database Schema

## Notes
 - Implementing this schema on Azure as it is below
 - Last Updated 11/5/23
 - Many classes in the dataset have `TBA` for unknown meeting times, `TBD` for unknown profs
 - Data has ~100 instances of courses with same class code and different titles

## Past Course Tables (User-Unmodifiable)

```SQL
course(
    course_id CHAR(10) NOT NULL,
    title VARCHAR(200),
    credits VARCHAR(17),
    deleted INT DEFAULT 0,
    PRIMARY KEY(course_id)
)
```
 - `course_id` is a 2/3/4-letter major code, a space, and a 5 digit number, e.g. "CSE 30246"

```SQL
section(
    crn CHAR(5) NOT NULL,
    sem CHAR(4) NOT NULL,
    course_id CHAR(10),
    prof VARCHAR(50),
    meets VARCHAR(75),
    deleted INT DEFAULT 0,
    PRIMARY KEY(crn, sem)
)
```
 - Section days and times `meets`, e.g. "TTh 3:30-4:45p"
 - 4-letter semester code `sem`, e.g. "FA23"
 - `meets` has to be 75 characters due to oddly-formatted law research courses

```SQL
description(
    course_id CHAR(10) NOT NULL,
    description LONGTEXT,
    deleted INT DEFAULT 0,
    PRIMARY KEY(course_id)
)
```

```SQL
course_has_prereq(
    course_id CHAR(10) NOT NULL,
    prereq_ids VARCHAR(250) NOT NULL,
    deleted INT DEFAULT 0,
    PRIMARY KEY(course_id, prereq_ids)
)
```
 - Each tuple represents a requirement that must be fulfilled
 - If multiple courses fulfill the same requirement, they are combined on the same tuple

```SQL
course_has_coreq(
    course_id CHAR(10) NOT NULL,
    coreq_id CHAR(10) NOT NULL,
    deleted INT DEFAULT 0,
    PRIMARY KEY(course_id, coreq_id)
)
```

```SQL
major(
    major_code CHAR(4) NOT NULL,
    deleted INT DEFAULT 0,
    PRIMARY KEY(major_code)
)
```
 - 2/3/4-letter `major_code` from PATH, e.g. "EG", "CSE", "ACMS"
 - I can make a doc with all possible major codes if needed

```SQL
core_req(
    req_code CHAR(4) NOT NULL,
    deleted INT DEFAULT 0,
    PRIMARY KEY(req_code)
)
```
 - 4-letter `req_code` codes from PATH, e.g. "WRRH" for writing & rhetoric
 - I can also compile all of these if needed
 - Also planning to use this for any requirement fulfilled by many courses, e.g. CSE electives

```SQL
major_requires_course(
    major_code CHAR(4) NOT NULL,
    course_id CHAR(10) NOT NULL,
    deleted INT DEFAULT 0,
    PRIMARY KEY(major_code, course_id)
)
```
 - For courses that are *explicitly* required by a major
 - i.e. CSE explicitly requires Discrete, but not Databases

```SQL
major_requires_core_req(
    major_code CHAR(4) NOT NULL,
    req_code CHAR(5) NOT NULL,
    double_count_check INT NOT NULL,
    deleted INT DEFAULT 0,
    PRIMARY KEY(major_code, req_code, double_count_check)
)
```
 - If two requirements have the same value for `double_count_check`, then they cannot be fulfilled by the same course

```SQL
course_fulfills_core_req(
    req_code CHAR(5) NOT NULL, 
    course_id CHAR(10) NOT NULL, 
    deleted INT DEFAULT 0,
    PRIMARY KEY(req_code, course_id)
)
```

## Future Planning Tables (User-Modifiable)

```SQL
student(
    netid CHAR(8) NOT NULL, 
    name VARCHAR(50), 
    major_code CHAR(4), 
    gradyear INT, 
    deleted INT DEFAULT 0,
    PRIMARY KEY(netid),
    FOREIGN KEY(major_code) REFERENCES major(major_code)
)
```

```SQL
has_enrollment(
    enrollment_id INT NOT NULL, 
    netid CHAR(8) NOT NULL, 
    course_id CHAR(10), 
    sem CHAR(4), 
    title VARCHAR(200), 
    user_created INT DEFAULT 0, 
    deleted INT DEFAULT 0, 
    PRIMARY KEY(enrollment_id), 
    FOREIGN KEY(netid) REFERENCES student(netid) ON UPDATE CASCADE,
    CONSTRAINT uc_enrollment UNIQUE (netid, course_id, sem, title)
)
```
 - `sem` does not include years here, instead formatted with grades ("FAFR", "SPJU")

```SQL
login(
    netid CHAR(8) NOT NULL, 
    salt CHAR(32) NOT NULL, 
    hash CHAR(32) NOT NULL,
    PRIMARY KEY(netid)
)
```
 - Users cannot directly modify, only through login functions
 - In this section because this table is not static
