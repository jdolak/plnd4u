# Relational Database Schema

## Notes TBD
 - Incomplete: Last Updated 10/03/23
 - Determine how to identify majors in a unified way
   - We need to use queries to find everyone of the same major
   - Would four-letter codes work? i.e. CSE, ACCT
 - Is the major relation needed? Don't think so

## Past Course Tables (User-Unmodifiable)

course(_course_id char(10)_, title varchar(50))

section(_crn char(5)_, course_id char(10), prof varchar(50), days char(5), time varchar(20))

sectionBelongs(_crn char(5)_, _course_id char(10)_)

hasPrereq(_course_id char(10)_, prereq_id char(10))

hasCoreq(_course_id char(10)_, coreq_id char(10))

major(_major char(4)_)

## Future Planning Tables (User-Modifiable)

student(_netid char(8)_, name varchar(50), major char(4))

hasEnrollment(_netid char(8)_, _course_id char(10)_, _sem char(4)_)
