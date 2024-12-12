#!/usr/bin/env python3

from plnd4u_db_connect import *
from flask import g


def db_enroll_class(netid, course_id, sem, title):
    LOG.info(f"{netid}, {course_id}, {sem}, {title}")
    # check if enrollment exists
    try:
        class_check = db_check_class_in_enrollment(netid, course_id, sem, title, 0)
        if class_check == 1:
            return 1
        if len(class_check):
            return 1
        # check if enrollment exists but has been deleted
        already_deleted_list = db_check_class_in_enrollment(
            netid, course_id, sem, title, 1
        )
        if len(already_deleted_list):
            enrollment_id = already_deleted_list[0][0]
            return _db_undel_enrollment(enrollment_id)

        # if not, create the enrollment
        return _db_create_enrollment(netid, course_id, sem, title)

    except Exception as e:
        LOG.error(e)
        return 1


def db_check_class_in_enrollment(netid, course_id, sem, title, deleted):
    title = f"{title[0:(len(title)-3)]}%"
    #sql = "SELECT enrollment_id FROM has_enrollment WHERE netid = ? AND course_id = ? AND sem = ? AND title LIKE ? AND deleted = ?"
    val = (netid, course_id, sem, title, deleted)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        #result = list(mycursor)
        result = g.db_session.query(HasEnrollment.enrollment_id).filter(
            and_(
                HasEnrollment.netid == netid,
                HasEnrollment.course_id == course_id,
                HasEnrollment.sem == sem,
                HasEnrollment.title.like(title),
                HasEnrollment.deleted == deleted
            )
        ).all()

    except Exception as e:
        LOG.error(f"{val} : {e}")
        return 1

    return result


def _db_create_enrollment(netid, course_id, sem, title):
    #sql = "INSERT INTO has_enrollment (enrollment_id, netid, course_id, sem, title) SELECT COUNT(*), ?, ?, ?, ? FROM has_enrollment"
    #val = (netid, course_id, sem, title)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        #DB.commit()
        
        count = g.db_session.query(func.count(HasEnrollment.enrollment_id)).scalar()

        new_enrollment = HasEnrollment(
            enrollment_id=count,
            netid=netid,
            course_id=course_id,
            sem=sem,
            title=title
        )

        g.db_session.add(new_enrollment)
        g.db_session.commit()

        LOG.info(f"Class Enrolled : {netid} - {course_id} - {sem} - {title}")
        return 0
    except Exception as e:
        LOG.error(e)
        return 1


def _db_undel_enrollment(enrollment_id):
    #sql = "UPDATE has_enrollment SET deleted = 0 WHERE enrollment_id = ?"
    #val = (enrollment_id,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # DB.commit()
        g.db_session.query(HasEnrollment).filter(HasEnrollment.enrollment_id == enrollment_id).update(
            {'deleted': 0}, synchronize_session='fetch')
    except Exception as e:
        LOG.error(e)
        return 1


def db_register_student(netid, name, major_code, gradyear):
    #sql = "INSERT INTO student (netid, name, major_code, gradyear) VALUES (:1, :2, :3, :4)"
    val = [(netid, name, major_code, gradyear)]
    try:
        LOG.info(str(list(map(type, val[0]))))
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # DB.commit()

        new_student = Student(
            netid=netid,
            name=name,
            major_code=major_code,
            gradyear=gradyear
        ) 

        g.db_session.add(new_student)
        g.db_session.commit()

        LOG.info(f"Student Registered : {netid}")
        return 0
    except Exception as e:
        LOG.error(e)
        return 1


def db_search_past_classes(netid, search, filters):
    
    # obtain major of student separately to simplify following queries
    

    search = f"%{search}%"
    levels = ""
    tables = "course"
    sem = ""
    reqs = ""
    core_reqs = ("WKAL", "WKCD", "WKDT", "WKFP", "WKFT", "WKHI", "WKIN", "WKLC", "WKQR", "WKSP", "WKSS", "WKST", "WRIT", "WRRH", "USEM", "FYS1", "FYS2")

    fall_semester = filters[0]
    spring_semester = filters[1]
    level_one = filters[2]
    level_two = filters[3]
    level_three = filters[4]
    level_four = filters[5]
    uni_req = filters[6]
    major_req = filters[7]
    major_elective = filters[8]

    if major_elective or major_req:
        sql = "SELECT major_code FROM student WHERE netid=:netid AND deleted <> 1"
        # val = (netid, )
        try:
            # mycursor = DB.cursor()
            # mycursor.execute(sql, val)
            with Session(ENGINE) as session:
                result = g.db_session.execute(text(sql),{"netid": netid})
                g.db_session.commit()
            major_code = list(result)[0][0]
        except Exception as e:
            LOG.error(e)
            return 1

    # form queries based on filters
    if fall_semester ^ spring_semester:
        tables = tables + ", section"
        if fall_semester:
            sem = (
                " AND section.course_id = course.course_id AND section.sem LIKE 'FA__'"
            )
        else:
            sem = (
                " AND section.course_id = course.course_id AND section.sem LIKE 'SP__'"
            )

    if level_one:
        levels = levels + " OR course.course_id LIKE '%1____'"
    if level_two:
        levels = levels + " OR course.course_id LIKE '%2____'"
    if level_three:
        levels = levels + " OR course.course_id LIKE '%3____'"
    if level_four:
        levels = levels + " OR course.course_id LIKE '%4____'"

    if uni_req or major_elective:
        tables = tables + ", course_fulfills_core_req AS cfcr"
    if uni_req:
        reqs = f"{reqs} AND course.course_id=cfcr.course_id AND req_code IN {core_reqs}"
    if major_req:
        tables = tables + ", major_requires_course AS mrc"
        reqs = f"{reqs} AND major_code=\"{major_code}\" AND course.course_id=mrc.course_id"
    if major_elective:
        reqs = f"{reqs} AND course.course_id=cfcr.course_id AND req_code IN (SELECT elective_code FROM major_requires_elective WHERE major_code=\"{major_code}\")"

    # execute search query
    #sql = f"SELECT DISTINCT course.course_id, course.title FROM {tables} WHERE course.deleted <> 1 AND (course.title LIKE ? or course.course_id LIKE ?) AND (0=1{levels}){sem}{reqs} ORDER BY course.course_id"
    sql = text(f"SELECT DISTINCT course.course_id, course.title FROM {tables} WHERE course.deleted <> 1 AND (course.title LIKE :query or course.course_id LIKE :query) AND (0=1{levels}){sem}{reqs} ORDER BY course.course_id")
    # val = (search, search)

    try:
        # mycursor = DB.cursor()
        # list comprehension to shorten course titles to max 80 chars
        # mycursor.execute(sql, val)

        result = g.db_session.execute(sql, {"query": search})
        g.db_session.commit()

        results = [
            tuple(
                [
                    row[i]
                    if (i != 1 or len(str(row[i])) <= 80)
                    else f"{row[1][:77]}..."
                    for i in range(len(row))
                ]
            )
            # for row in list(mycursor)
            for row in list(result)
        ]

        LOG.info(f"Class searched : {search}")
        if not len(results):
            LOG.info("No results")
            return 0
        else:
            return results

    except Exception as e:
        LOG.error(f"{val} : {e}")
        return 2


def _db_del_enrollment(enrollment_id):
    #sql = "UPDATE has_enrollment SET deleted = 1 WHERE enrollment_id = ?"
    #val = (enrollment_id,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # DB.commit()

        g.db_session.query(HasEnrollment).filter(
            HasEnrollment.enrollment_id == enrollment_id).update({'deleted': 1}, synchronize_session='fetch') 
        g.db_session.commit()
        return 0
    except Exception as e:
        LOG.error(e)
        return e


def db_del_enrollment(netid, course_id, sem, title):
    try:
        _db_del_enrollment(
            db_check_class_in_enrollment(netid, course_id, sem, title, 0)[0][0]
        )
    except IndexError:
        LOG.error("Cannot delete: entry not found.")
        return 1
    except Exception as e:
        LOG.error(e)
        return 1
    LOG.info(f"Deleted : {course_id}, {title}")
    return 0


def _db_del_enrollment_permanent(enrollment_id):
    #sql = "DELETE FROM has_enrollment WHERE enrollment_id = ?"
    #val = (enrollment_id,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # DB.commit()

        g.db_session.query(HasEnrollment).filter(
            HasEnrollment.enrollment_id == enrollment_id).delete(synchronize_session='fetch')
        g.db_session.commit()

        return 0
    except Exception as e:
        LOG.error(e)
        return e


def db_del_student(netid):
    #sql = "UPDATE student SET deleted = 1 WHERE netid = ?"
    #val = (netid,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # DB.commit()

        g.db_session.query(Student).filter(
            Student.netid == netid).update({'deleted': 1}, synchronize_session='fetch') 
        g.db_session.commit()
        return 0
    except Exception as e:
        LOG.error(e)
        return 1


def db_del_student_permanent(netid):
    #sql = "DELETE FROM student WHERE netid = ?"
    # val = (netid,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # DB.commit()
        
        g.db_session.query(Student).filter(
            Student.netid == netid).delete(synchronize_session='fetch')
        g.db_session.commit()

        return 0
    except Exception as e:
        LOG.error(e)
        return 1


def db_update_student_major(netid, major_code):
    #sql = "UPDATE student SET major_code = ? WHERE netid = ?"
    # val = (major_code, netid)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # DB.commit()

        g.db_session.query(Student).filter(
            Student.netid == netid).update({'major_code': major_code}, synchronize_session='fetch') 
        g.db_session.commit()

        return 0
    except Exception as e:
        LOG.error(e)
        return 1


def db_update_student_gradyear(netid, gradyear):
    #sql = "UPDATE student SET gradyear = ?  WHERE netid = ?"
    # val = (gradyear, netid)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # DB.commit()

        g.db_session.query(Student).filter(
            Student.netid == netid).update({'gradyear': gradyear}, synchronize_session='fetch')
        g.db_session.commit()
        
        return 0
    except Exception as e:
        LOG.error(e)
        return 1


def db_show_student_enrollments(netid, sem):
    #sql = "SELECT enrollment_id, course_id, sem, title, user_created FROM has_enrollment WHERE netid = ? AND sem = ? AND deleted <> 1"
    # val = (netid, sem)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # return list(mycursor)
        result = g.db_session.query(
            HasEnrollment.enrollment_id,
            HasEnrollment.course_id,
            HasEnrollment.sem,
            HasEnrollment.title,
            HasEnrollment.user_created
        ).filter(
            HasEnrollment.netid == netid,
            HasEnrollment.sem == sem,
            HasEnrollment.deleted != 1  # Exclude deleted records
        ).all()
        
        result = map(list, result)
        return list(result)
    
    except Exception as e:
        LOG.error(e)
        return 1


def db_show_student_enrollments_short(netid, sem):
    # sql = "SELECT enrollment_id, course_id, sem, title, user_created FROM has_enrollment WHERE netid = ? AND sem = ? AND deleted <> 1"
    # val = (netid, sem)
    try:
        # mycursor = DB.cursor()
        # list comprehension to shorten course titles to max 20 chars
        # jachob dared me to do it
        # mycursor.execute(sql, val)

        result = g.db_session.query(
            HasEnrollment.enrollment_id,
            HasEnrollment.course_id,
            HasEnrollment.sem,
            HasEnrollment.title,
            HasEnrollment.user_created
        ).filter(
            HasEnrollment.netid == netid,
            HasEnrollment.sem == sem,
            HasEnrollment.deleted != 1  # Exclude deleted records
        ).all() 

        return [
            tuple(
                [
                    row[i]
                    if (i != 3 or len(str(row[i])) <= 20)
                    else f"{row[3][:17]}..."
                    for i in range(len(row))
                ]
            )
            #for row in list(mycursor)
            for row in list(result)

        ]
    except Exception as e:
        LOG.error(e)
        return 1


def db_del_all_enrollments(netid):
    # sql = "UPDATE has_enrollment SET deleted = 1 WHERE netid = ?"
    # val = (netid,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        #DB.commit()

        g.db_session.query(HasEnrollment).filter(
            HasEnrollment.netid == netid).update({'deleted': 1}, synchronize_session='fetch') 
        g.db_session.commit()

        LOG.debug("Deleted all enrollments")
        return 0
    except:
        LOG.error("Did not delete all enrollments")
        return 1


# section details queried using below functions
def db_show_description(course_id):
    # sql = "SELECT description FROM description WHERE course_id=? AND deleted <> 1"
    # val = (course_id,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # return list(mycursor)
        
        result = g.db_session.query(Description.description).filter(
            Description.course_id == course_id,
            Description.deleted != 1).all()
        
        result = map(list, result)
        return list(result)
    except Exception as e:
        LOG.error(e)
        return 1


def db_show_credits(course_id):
    # sql = "SELECT credits FROM course WHERE course_id=? AND deleted <> 1"
    # val = (course_id,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        #return list(mycursor)
        
        result = g.db_session.query(Course.credits).filter(
            Course.course_id == course_id,
            Course.deleted != 1).all()
        
        result = map(list, result)
        return list(result)
    except Exception as e:
        LOG.error(e)
        return 1


def db_show_coreqs(course_id):
    # sql = "SELECT coreq_id FROM course_has_coreq WHERE course_id=? AND deleted <> 1"
    # val = (course_id,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # return list(mycursor)
        
        result = g.db_session.query(CourseHasCoreq.coreq_id).filter(
            CourseHasCoreq.course_id == course_id,
            CourseHasCoreq.deleted != 1).all() 

        result = map(list, result)
        return list(result)
    
    except Exception as e:
        LOG.error(e)
        return 1


def db_show_prereqs(course_id):
    # sql = "SELECT prereq_ids FROM course_has_prereq WHERE course_id=? AND deleted <> 1"
    # val = (course_id,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        #return list(mycursor)
        result = g.db_session.query(CourseHasPrereq.prereq_ids).filter(
            CourseHasPrereq.course_id == course_id,
            CourseHasPrereq.deleted != 1).all()
         
        result = map(list, result)
        return list(result)
    except Exception as e:
        LOG.error(e)
        return 1


def db_show_core_reqs(course_id):
    # sql = "SELECT req_code FROM course_fulfills_core_req WHERE course_id=? AND deleted <> 1"
    # val = (course_id,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # return list(mycursor)

        result = g.db_session.query(CourseFulfillsCoreReq.req_code).filter(
            CourseFulfillsCoreReq.course_id == course_id,
            CourseFulfillsCoreReq.deleted != 1).all() 

        result = map(list, result)
        return list(result)
    except Exception as e:
        LOG.error(e)
        return 1


def db_show_semesters(course_id):
    # sql = "SELECT DISTINCT sem FROM section WHERE course_id=? AND deleted <> 1"
    # val = (course_id,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # return list(mycursor)

        result = g.db_session.query(Section.sem).filter(
            Section.course_id == course_id, Section.deleted != 1).distinct().all()

        result = map(list, result)
        return list(result)
    except Exception as e:
        LOG.error(e)
        return 1


def db_show_profs(course_id):
    # sql = "SELECT DISTINCT prof FROM section WHERE course_id=? AND deleted <> 1"
    # val = (course_id,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # return list(mycursor)

        result = g.db_session.query(Section.prof).filter(
            Section.course_id == course_id, Section.deleted != 1 ).distinct().all()  

        result = map(list, result)
        return list(result)
    except Exception as e:
        LOG.error(e)
        return 1


def db_show_meeting_times(course_id):
    # sql = "SELECT DISTINCT meets FROM section WHERE course_id=? AND deleted <> 1"
    # val = (course_id,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # return list(mycursor)

        result = g.db_session.query(Section.meets).filter(
            Section.course_id == course_id, Section.deleted != 1 ).distinct().all() 

        result = map(list, result) 
        return list(result)
    except Exception as e:
        LOG.error(e)
        return 1


# returns sem/prof/time grouped by semester
# ask callie if she'd rather display that than individual, unique sem/prof/time values
def db_show_section_details(course_id):
    # sql = "SELECT sem, prof, meets FROM section WHERE course_id=? AND deleted <> 1"
    # val = (course_id,)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # return list(mycursor)

        result = g.db_session.query(Section.sem, Section.prof, Section.meets).filter(
            Section.course_id == course_id, Section.deleted != 1 ).all()
        
        result = map(list, result)
        return list(result)
    except Exception as e:
        LOG.error(e)
        return 1


def db_show_sem_credits(netid, sem):
    # sql = "SELECT credits FROM has_enrollment, course WHERE netid = ? AND sem = ? AND course.course_id = has_enrollment.course_id AND has_enrollment.deleted <> 1 AND course.deleted <> 1;"
    # val = (netid, sem)
    try:
        # mycursor = DB.cursor()
        # mycursor.execute(sql, val)
        # credit = list(mycursor)
        result = g.db_session.query(Course.credits).join(
            HasEnrollment, HasEnrollment.course_id == Course.course_id
        ).filter(
            HasEnrollment.netid == netid,
            HasEnrollment.sem == sem,
            HasEnrollment.deleted != 1, 
            Course.deleted != 1   
        ).all()
         
        credit = list(result)

    except Exception as e:
        LOG.error(e)
        return 1

    return sum([float(i[0].split()[0]) for i in credit])


def db_show_sem_credits_all(netid):
    sems = ["UNLT", "FRFA", "FRSP", "SOFA", "SOSP", "JUFA", "JUSP", "SEFA", "SESP"]
    arr = []

    for sem in sems:
        arr.append(db_show_sem_credits(netid, sem))
    return arr
