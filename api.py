from datetime import date, timedelta
import json
from uuid import uuid4

from django.db import connection, models
from nanodjango import Django

app = Django(STATICFILES_DIRS=[])

from ninja.errors import HttpError

GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
)

STUDENT_STATUS_CHOICES = (
    ('active', 'active'),
    ('inactive', 'inactive'),
)

LESSON_TYPE_CHOICES = (
    ('NEW', 'NEW'),
    ('FRONT_REVISION', 'FRONT_REVISION'),
    ('MURAJAH', 'MURAJAH'),
)

LESSON_RATING_CHOICES = (
    ('Pass', 'Pass'),
    ('Re-do', 'Re-do'),
    ('Absent', 'Absent'),
    ('Not Ready', 'Not Ready'),
)

ASSESSMENT_TYPE_CHOICES = (
    ('Quarterly', 'Quarterly'),
    ('Test', 'Test'),
)

MILESTONE_WEEKS = {
    5: 1,
    10: 2,
    15: 3,
    20: 4,
    25: 5,
    30: 6,
}


@app.admin
class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'teacher'
        ordering = ['name', 'id']


@app.admin
class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    enrollment_date = models.DateField()
    current_juz = models.PositiveSmallIntegerField(default=1)
    total_juz_memorized = models.PositiveSmallIntegerField(default=0)
    goal_juz = models.PositiveSmallIntegerField(blank=True, null=True)
    goal_date = models.DateField(blank=True, null=True)
    challenges = models.TextField(blank=True, null=True)
    last_milestone_juz = models.PositiveSmallIntegerField(default=0)
    muraja_only_until = models.DateField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=10, choices=STUDENT_STATUS_CHOICES, default='active')

    class Meta:
        db_table = 'student'
        ordering = ['name', 'id']


@app.admin
class DailyLesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES)
    juz = models.PositiveSmallIntegerField()
    surah = models.CharField(max_length=255)
    ayah_start = models.PositiveSmallIntegerField()
    ayah_end = models.PositiveSmallIntegerField()
    comments = models.TextField(blank=True, null=True)
    rating = models.CharField(max_length=20, choices=LESSON_RATING_CHOICES)
    extra_work = models.BooleanField(default=False)

    class Meta:
        db_table = 'daily_lesson'
        ordering = ['-date', 'id']


@app.admin
class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=True)

    class Meta:
        db_table = 'attendance'
        ordering = ['-date', 'id']
        constraints = [
            models.UniqueConstraint(fields=['student', 'date'], name='uniq_attendance_student_date'),
        ]


@app.admin
class Homework(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    passed = models.BooleanField(default=False)

    class Meta:
        db_table = 'homework'
        ordering = ['-date', 'id']
        constraints = [
            models.UniqueConstraint(fields=['student', 'date'], name='uniq_homework_student_date'),
        ]


@app.admin
class MonthlyPoints(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.CharField(max_length=7)
    new_work_points = models.PositiveSmallIntegerField(default=0)
    front_work_points = models.PositiveSmallIntegerField(default=0)
    back_work_points = models.PositiveSmallIntegerField(default=0)
    extra_work_points = models.PositiveSmallIntegerField(default=0)
    attendance_points = models.PositiveSmallIntegerField(default=0)
    behavior_points = models.PositiveSmallIntegerField(default=0)
    total_points = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'monthly_points'
        ordering = ['month', 'id']
        constraints = [
            models.UniqueConstraint(fields=['student', 'month'], name='uniq_monthly_points_student_month'),
        ]


@app.admin
class Assessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE_CHOICES)
    score = models.PositiveSmallIntegerField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'assessment'
        ordering = ['-date', 'id']


@app.admin
class MurajaSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    muraja_juz_per_day = models.FloatField(default=1)
    cycle_length_days = models.PositiveSmallIntegerField(default=7)
    next_revision_due_date = models.DateField(blank=True, null=True)
    overdue = models.BooleanField(default=False)
    last_completed_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'muraja_schedule'
        ordering = ['id']


def parse_payload(request) -> dict:
    if not request.body:
        return {}
    return json.loads(request.body.decode())


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def format_date(value: date | None) -> str | None:
    if not value:
        return None
    return value.isoformat()


def get_muraja_daily_load(juz_memorized: int) -> float:
    if juz_memorized <= 2:
        return 0.25
    if juz_memorized <= 6:
        return 0.5
    if juz_memorized <= 10:
        return 1
    if juz_memorized <= 15:
        return 1.5
    if juz_memorized <= 20:
        return 2
    if juz_memorized <= 25:
        return 2.5
    return 3


def get_milestone_until(juz_memorized: int) -> date | None:
    weeks = MILESTONE_WEEKS.get(juz_memorized)
    if not weeks:
        return None
    return date.today() + timedelta(days=weeks * 7)


def ayah_count(lesson: DailyLesson) -> int:
    return max(0, lesson.ayah_end - lesson.ayah_start + 1)


def date_range(request, default_days: int = 30) -> tuple[date, date]:
    end_date = parse_date(request.GET.get('endDate')) or date.today()
    start_date = parse_date(request.GET.get('startDate')) or (end_date - timedelta(days=default_days))
    return start_date, end_date


def update_milestone(student: Student, total_juz_memorized: int) -> None:
    if total_juz_memorized in MILESTONE_WEEKS and total_juz_memorized > student.last_milestone_juz:
        student.last_milestone_juz = total_juz_memorized
        student.muraja_only_until = get_milestone_until(total_juz_memorized)


def serialize_teacher(teacher: Teacher, student_count: int | None = None) -> dict:
    payload = {
        'id': str(teacher.id),
        'name': teacher.name,
        'email': teacher.email,
    }
    if student_count is not None:
        payload['studentCount'] = student_count
    return payload


def serialize_student(student: Student, include_teacher: bool = True) -> dict:
    return {
        'id': str(student.id),
        'name': student.name,
        'gender': student.gender,
        'dateOfBirth': format_date(student.date_of_birth),
        'enrollmentDate': format_date(student.enrollment_date),
        'currentJuz': student.current_juz,
        'totalJuzMemorized': student.total_juz_memorized,
        'goalJuz': student.goal_juz,
        'goalDate': format_date(student.goal_date),
        'challenges': student.challenges,
        'murajaOnlyUntil': format_date(student.muraja_only_until),
        'teacherId': str(student.teacher_id) if student.teacher_id else None,
        'status': student.status,
        'teacher': serialize_teacher(student.teacher) if include_teacher and student.teacher else None,
    }


def serialize_lesson(lesson: DailyLesson, include_student: bool = True) -> dict:
    return {
        'id': str(lesson.id),
        'studentId': str(lesson.student_id),
        'date': format_date(lesson.date),
        'lessonType': lesson.lesson_type,
        'juz': lesson.juz,
        'surah': lesson.surah,
        'ayahStart': lesson.ayah_start,
        'ayahEnd': lesson.ayah_end,
        'comments': lesson.comments,
        'rating': lesson.rating,
        'extraWork': lesson.extra_work,
        'student': serialize_student(lesson.student, include_teacher=False) if include_student else None,
    }


def serialize_attendance(record: Attendance) -> dict:
    return {
        'id': str(record.id),
        'studentId': str(record.student_id),
        'date': format_date(record.date),
        'present': record.present,
    }


def serialize_homework(record: Homework, include_student: bool = True) -> dict:
    return {
        'id': str(record.id),
        'studentId': str(record.student_id),
        'date': format_date(record.date),
        'passed': record.passed,
        'student': serialize_student(record.student, include_teacher=False) if include_student else None,
    }


def serialize_monthly_points(points: MonthlyPoints, include_student: bool = True) -> dict:
    return {
        'id': str(points.id),
        'studentId': str(points.student_id),
        'month': points.month,
        'newWorkPoints': points.new_work_points,
        'frontWorkPoints': points.front_work_points,
        'backWorkPoints': points.back_work_points,
        'extraWorkPoints': points.extra_work_points,
        'attendancePoints': points.attendance_points,
        'behaviorPoints': points.behavior_points,
        'totalPoints': points.total_points,
        'student': serialize_student(points.student, include_teacher=False) if include_student else None,
    }


def serialize_assessment(record: Assessment, include_student: bool = True) -> dict:
    return {
        'id': str(record.id),
        'studentId': str(record.student_id),
        'date': format_date(record.date),
        'type': record.type,
        'score': record.score,
        'notes': record.notes,
        'student': serialize_student(record.student, include_teacher=False) if include_student else None,
    }


def serialize_muraja_schedule(schedule: MurajaSchedule, include_student: bool = True) -> dict:
    return {
        'id': str(schedule.id),
        'studentId': str(schedule.student_id),
        'murajaJuzPerDay': schedule.muraja_juz_per_day,
        'cycleLengthDays': schedule.cycle_length_days,
        'nextRevisionDueDate': format_date(schedule.next_revision_due_date),
        'overdue': schedule.overdue,
        'lastCompletedDate': format_date(schedule.last_completed_date),
        'student': serialize_student(schedule.student, include_teacher=False) if include_student else None,
    }


def update_monthly_points(student: Student, lesson: DailyLesson) -> None:
    month = lesson.date.strftime('%Y-%m')
    points = MonthlyPoints.objects.filter(student=student, month=month).first()

    if not points:
        points = MonthlyPoints.objects.create(
            student=student,
            month=month,
            new_work_points=0,
            front_work_points=0,
            back_work_points=0,
            extra_work_points=0,
            attendance_points=0,
            behavior_points=0,
            total_points=0,
        )

    if lesson.lesson_type == 'NEW':
        points.new_work_points += 1
    elif lesson.lesson_type == 'FRONT_REVISION':
        points.front_work_points += 1
    else:
        points.back_work_points += 1

    if lesson.extra_work:
        points.extra_work_points += 1

    recalculate_points(points, update_fields=[
        'new_work_points',
        'front_work_points',
        'back_work_points',
        'extra_work_points',
    ])


def month_bounds(month: str) -> tuple[date, date]:
    year, month_value = (int(part) for part in month.split('-'))
    start = date(year, month_value, 1)
    if month_value == 12:
        end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(year, month_value + 1, 1) - timedelta(days=1)
    return start, end


def recalculate_points(points: MonthlyPoints, update_fields: list[str] | None = None) -> None:
    points.total_points = (
        points.new_work_points
        + points.front_work_points
        + points.back_work_points
        + points.extra_work_points
        + points.attendance_points
        + points.behavior_points
    )
    fields = update_fields[:] if update_fields else []
    if 'total_points' not in fields:
        fields.append('total_points')
    points.save(update_fields=fields)


def update_attendance_points(student: Student, month: str) -> None:
    points = MonthlyPoints.objects.filter(student=student, month=month).first()
    if not points:
        points = MonthlyPoints.objects.create(student=student, month=month)

    start, end = month_bounds(month)
    present_count = Attendance.objects.filter(
        student=student,
        date__gte=start,
        date__lte=end,
        present=True,
    ).count()

    points.attendance_points = present_count
    recalculate_points(points, update_fields=['attendance_points'])


def lesson_range(student: Student, lesson_type: str | None, start_date: date | None, end_date: date | None) -> list[DailyLesson]:
    lessons = DailyLesson.objects.filter(student=student)
    if lesson_type:
        lessons = lessons.filter(lesson_type=lesson_type)
    if start_date:
        lessons = lessons.filter(date__gte=start_date)
    if end_date:
        lessons = lessons.filter(date__lte=end_date)
    return list(lessons)


def summarize_lessons(lessons: list[DailyLesson]) -> dict:
    ayahs = sum(ayah_count(lesson) for lesson in lessons)
    surahs = len({lesson.surah for lesson in lessons})
    return {'ayahs': ayahs, 'surahs': surahs}


def homework_stats(student: Student, start_date: date, end_date: date) -> dict:
    records = Homework.objects.filter(
        student=student,
        date__gte=start_date,
        date__lte=end_date,
    ).order_by('-date')
    total = records.count()
    passed = records.filter(passed=True).count()
    failed = records.filter(passed=False).count()
    pass_rate = round((passed / total) * 100) if total else 0
    last_record = records.first()
    return {
        'totalCount': total,
        'passedCount': passed,
        'failedCount': failed,
        'passRate': pass_rate,
        'lastDate': format_date(last_record.date) if last_record else None,
    }


def attendance_stats(student: Student, start_date: date, end_date: date) -> dict:
    records = Attendance.objects.filter(
        student=student,
        date__gte=start_date,
        date__lte=end_date,
    )
    total = records.count()
    present = records.filter(present=True).count()
    absent = records.filter(present=False).count()
    rate = round((present / total) * 100) if total else 0
    return {
        'totalCount': total,
        'presentCount': present,
        'absentCount': absent,
        'attendanceRate': rate,
    }


def week_start_for(value: date) -> date:
    return value - timedelta(days=value.weekday())


def weekly_trend(student: Student, weeks: int = 8) -> list[dict]:
    end_week_start = week_start_for(date.today())
    start_week = end_week_start - timedelta(days=(weeks - 1) * 7)
    lessons = lesson_range(student, 'NEW', start_week, end_week_start + timedelta(days=6))
    trend = []
    current = start_week
    for _ in range(weeks):
        week_end = current + timedelta(days=6)
        week_ayahs = sum(
            ayah_count(lesson)
            for lesson in lessons
            if current <= lesson.date <= week_end
        )
        trend.append({'weekStart': format_date(current), 'ayahs': week_ayahs})
        current = current + timedelta(days=7)
    return trend


def student_progress_report(student: Student) -> dict:
    today = date.today()
    week_start = week_start_for(today)
    month_start = today.replace(day=1)

    new_lessons = lesson_range(student, 'NEW', None, None)
    new_week = lesson_range(student, 'NEW', week_start, today)
    new_month = lesson_range(student, 'NEW', month_start, today)
    new_last_4_weeks = lesson_range(student, 'NEW', today - timedelta(days=27), today)

    last_new = DailyLesson.objects.filter(student=student, lesson_type='NEW').order_by('-date').first()
    last_revision = DailyLesson.objects.filter(student=student).exclude(lesson_type='NEW').order_by('-date').first()

    schedule = MurajaSchedule.objects.filter(student=student).first()
    recent_ratings = DailyLesson.objects.filter(student=student).order_by('-date')[:5]
    homework_window_start = today - timedelta(days=30)

    total_stats = summarize_lessons(new_lessons)
    week_stats = summarize_lessons(new_week)
    month_stats = summarize_lessons(new_month)
    four_week_stats = summarize_lessons(new_last_4_weeks)
    avg_per_week = round(four_week_stats['ayahs'] / 4, 1) if four_week_stats['ayahs'] else 0

    recent_assessments = Assessment.objects.filter(student=student).order_by('-date')[:3]

    return {
        'student': serialize_student(student),
        'currentMemorization': {
            'juz': student.current_juz,
            'surah': last_new.surah if last_new else None,
            'ayah': last_new.ayah_end if last_new else None,
        },
        'totals': {
            'totalJuz': student.total_juz_memorized,
            'totalSurahs': total_stats['surahs'],
            'totalAyahs': total_stats['ayahs'],
        },
        'newWork': {
            'thisWeekAyahs': week_stats['ayahs'],
            'thisWeekSurahs': week_stats['surahs'],
            'thisMonthAyahs': month_stats['ayahs'],
            'thisMonthSurahs': month_stats['surahs'],
            'averageAyahsPerWeek': avg_per_week,
            'lastNewWorkDate': format_date(last_new.date) if last_new else None,
        },
        'revision': {
            'lastRevisionDate': format_date(last_revision.date) if last_revision else None,
            'nextRevisionDueDate': format_date(schedule.next_revision_due_date) if schedule else None,
            'murajaOnlyUntil': format_date(student.muraja_only_until),
            'overdue': schedule.overdue if schedule else False,
        },
        'assessments': [serialize_assessment(record, include_student=False) for record in recent_assessments],
        'recentRatings': [
            {
                'date': format_date(record.date),
                'lessonType': record.lesson_type,
                'rating': record.rating,
                'surah': record.surah,
                'ayahStart': record.ayah_start,
                'ayahEnd': record.ayah_end,
            }
            for record in recent_ratings
        ],
        'homework': homework_stats(student, homework_window_start, today),
        'challenges': student.challenges,
        'performanceTrend': weekly_trend(student),
    }


def seed_data() -> None:
    if 'teacher' not in connection.introspection.table_names():
        return
    if Teacher.objects.exists():
        return

    teacher1 = Teacher.objects.create(name='Ustadh Ahmad', email='ahmad@school.edu')
    teacher2 = Teacher.objects.create(name='Ustadh Ibrahim', email='ibrahim@school.edu')

    student1 = Student.objects.create(
        name='Abdullah Khan',
        gender='male',
        date_of_birth=parse_date('2010-05-15'),
        enrollment_date=parse_date('2023-09-01'),
        current_juz=5,
        total_juz_memorized=4,
        goal_juz=10,
        goal_date=parse_date('2026-06-01'),
        challenges='Needs consistency with daily muraja.',
        teacher=teacher1,
        status='active',
    )
    student2 = Student.objects.create(
        name='Fatima Ahmed',
        gender='female',
        date_of_birth=parse_date('2011-03-22'),
        enrollment_date=parse_date('2023-09-01'),
        current_juz=8,
        total_juz_memorized=7,
        goal_juz=15,
        goal_date=parse_date('2026-12-01'),
        teacher=teacher1,
        status='active',
    )
    student3 = Student.objects.create(
        name='Omar Hassan',
        gender='male',
        date_of_birth=parse_date('2009-11-10'),
        enrollment_date=parse_date('2022-09-01'),
        current_juz=15,
        total_juz_memorized=14,
        goal_juz=20,
        goal_date=parse_date('2026-08-15'),
        challenges='Struggles with retention on longer surahs.',
        teacher=teacher2,
        status='active',
    )
    student4 = Student.objects.create(
        name='Aisha Malik',
        gender='female',
        date_of_birth=parse_date('2012-07-03'),
        enrollment_date=parse_date('2024-01-15'),
        current_juz=2,
        total_juz_memorized=1,
        goal_juz=5,
        goal_date=parse_date('2026-03-01'),
        teacher=teacher2,
        status='active',
    )

    students = [student1, student2, student3, student4]
    for student in students:
        update_milestone(student, student.total_juz_memorized)
        if student.last_milestone_juz:
            student.save(update_fields=['last_milestone_juz', 'muraja_only_until'])

    today = date.today()
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)

    for index, student in enumerate(students):
        MurajaSchedule.objects.create(
            student=student,
            muraja_juz_per_day=get_muraja_daily_load(student.total_juz_memorized),
            cycle_length_days=7,
            next_revision_due_date=yesterday if index == 0 else tomorrow,
            overdue=index == 0,
        )

    lesson1 = DailyLesson.objects.create(
        student=student1,
        date=today,
        lesson_type='NEW',
        juz=5,
        surah="Al-Ma'idah",
        ayah_start=1,
        ayah_end=10,
        comments=None,
        rating='Pass',
        extra_work=False,
    )
    lesson2 = DailyLesson.objects.create(
        student=student2,
        date=today,
        lesson_type='MURAJAH',
        juz=7,
        surah="Al-A'raf",
        ayah_start=50,
        ayah_end=70,
        comments=None,
        rating='Pass',
        extra_work=True,
    )

    update_monthly_points(student1, lesson1)
    update_monthly_points(student2, lesson2)

    current_month = today.strftime('%Y-%m')
    for index, student in enumerate(students):
        MonthlyPoints.objects.update_or_create(
            student=student,
            month=current_month,
            defaults={
                'new_work_points': 10 + index * 2,
                'front_work_points': 8 + index,
                'back_work_points': 5 + index,
                'extra_work_points': index * 2,
                'attendance_points': 18 + index,
                'behavior_points': 15 + index,
                'total_points': 56 + index * 7,
            },
        )

    for index, student in enumerate(students):
        Homework.objects.create(
            student=student,
            date=today - timedelta(days=index),
            passed=index % 2 == 0,
        )

    Assessment.objects.create(
        student=student1,
        date=today - timedelta(days=10),
        type='Test',
        score=88,
        notes='Strong fluency, needs focus on tajweed.',
    )
    Assessment.objects.create(
        student=student2,
        date=today - timedelta(days=20),
        type='Quarterly',
        score=92,
        notes='Excellent retention.',
    )
    Assessment.objects.create(
        student=student3,
        date=today - timedelta(days=15),
        type='Test',
        score=76,
        notes='Needs more muraja for recent juz.',
    )


seed_data()


@app.api.get('/dashboard/stats')
def dashboard_stats(request):
    students = list(Student.objects.all())
    active_students = [s for s in students if s.status == 'active']
    total_juz = sum(s.total_juz_memorized for s in students)
    total_new_ayahs = sum(
        ayah_count(lesson) for lesson in DailyLesson.objects.filter(lesson_type='NEW')
    )
    total_new_surahs = len({
        lesson.surah for lesson in DailyLesson.objects.filter(lesson_type='NEW')
    })

    today = date.today()
    lessons_today = DailyLesson.objects.filter(date=today).count()

    overdue_schedules = MurajaSchedule.objects.filter(
        models.Q(overdue=True)
        | models.Q(next_revision_due_date__lt=today),
        student__status='active',
    ).count()

    month_start = today.replace(day=1)
    attendance_records = Attendance.objects.filter(date__gte=month_start, date__lte=today)
    present_count = attendance_records.filter(present=True).count()
    attendance_rate = round((present_count / attendance_records.count()) * 100) if attendance_records.exists() else 95

    rate_start = today - timedelta(days=27)
    rate_ayahs = sum(
        ayah_count(lesson)
        for lesson in DailyLesson.objects.filter(
            lesson_type='NEW',
            date__gte=rate_start,
            date__lte=today,
        )
    )
    average_rate = round((rate_ayahs / len(active_students) / 4), 1) if active_students else 0

    completed_students = Student.objects.filter(total_juz_memorized__gte=30)
    completion_days = []
    for student in completed_students:
        last_new = DailyLesson.objects.filter(student=student, lesson_type='NEW').order_by('-date').first()
        if last_new and student.enrollment_date:
            completion_days.append((last_new.date - student.enrollment_date).days)
    average_completion_days = round(sum(completion_days) / len(completion_days)) if completion_days else 0

    retention_rate = round(((len(active_students) - overdue_schedules) / len(active_students)) * 100) if active_students else 0

    return {
        'totalStudents': len(students),
        'activeStudents': len(active_students),
        'totalTeachers': Teacher.objects.count(),
        'totalJuzMemorized': total_juz,
        'totalAyahsMemorized': total_new_ayahs,
        'totalSurahsMemorized': total_new_surahs,
        'studentsOverdueMuraja': overdue_schedules,
        'averageMemorizationRate': average_rate,
        'lessonsToday': lessons_today,
        'attendanceRate': attendance_rate,
        'averageCompletionDays': average_completion_days,
        'retentionRate': retention_rate,
    }


@app.api.get('/teachers')
def list_teachers(request):
    teachers = list(Teacher.objects.all())
    return [
        serialize_teacher(teacher, student_count=Student.objects.filter(teacher=teacher).count())
        for teacher in teachers
    ]


@app.api.get('/teachers/{teacher_id}')
def get_teacher(request, teacher_id: str):
    teacher = Teacher.objects.filter(id=teacher_id).first()
    if not teacher:
        raise HttpError(404, 'Teacher not found')
    return serialize_teacher(teacher)


@app.api.post('/teachers')
def create_teacher(request):
    data = parse_payload(request)
    teacher = Teacher.objects.create(
        name=data.get('name', '').strip(),
        email=data.get('email', '').strip(),
    )
    return serialize_teacher(teacher)


@app.api.patch('/teachers/{teacher_id}')
def update_teacher(request, teacher_id: str):
    teacher = Teacher.objects.filter(id=teacher_id).first()
    if not teacher:
        raise HttpError(404, 'Teacher not found')

    data = parse_payload(request)
    if 'name' in data:
        teacher.name = data.get('name') or teacher.name
    if 'email' in data:
        teacher.email = data.get('email') or teacher.email
    teacher.save(update_fields=['name', 'email'])
    return serialize_teacher(teacher)


@app.api.delete('/teachers/{teacher_id}')
def delete_teacher(request, teacher_id: str):
    teacher = Teacher.objects.filter(id=teacher_id).first()
    if not teacher:
        raise HttpError(404, 'Teacher not found')
    teacher.delete()
    return 204, {}


@app.api.get('/students')
def list_students(request):
    teacher_id = request.GET.get('teacherId')
    status = request.GET.get('status')
    gender = request.GET.get('gender')
    min_juz = request.GET.get('minJuz')
    max_juz = request.GET.get('maxJuz')
    enrollment_start = parse_date(request.GET.get('enrollmentStart'))
    enrollment_end = parse_date(request.GET.get('enrollmentEnd'))
    min_age = request.GET.get('minAge')
    max_age = request.GET.get('maxAge')
    limit_value = request.GET.get('limit')

    students = Student.objects.all()
    if teacher_id:
        students = students.filter(teacher_id=teacher_id)
    if status:
        students = students.filter(status=status)
    if gender:
        students = students.filter(gender=gender)
    if min_juz and min_juz.isdigit():
        students = students.filter(total_juz_memorized__gte=int(min_juz))
    if max_juz and max_juz.isdigit():
        students = students.filter(total_juz_memorized__lte=int(max_juz))
    if enrollment_start:
        students = students.filter(enrollment_date__gte=enrollment_start)
    if enrollment_end:
        students = students.filter(enrollment_date__lte=enrollment_end)
    if min_age and min_age.isdigit():
        students = students.filter(date_of_birth__lte=date.today() - timedelta(days=int(min_age) * 365))
    if max_age and max_age.isdigit():
        students = students.filter(date_of_birth__gte=date.today() - timedelta(days=int(max_age) * 365))

    limit = int(limit_value) if limit_value and limit_value.isdigit() else None
    if limit:
        students = students.order_by('-enrollment_date', '-id')[:limit]

    return [serialize_student(student) for student in students]


@app.api.get('/students/{student_id}')
def get_student(request, student_id: str):
    student = Student.objects.filter(id=student_id).select_related('teacher').first()
    if not student:
        raise HttpError(404, 'Student not found')
    return serialize_student(student)


@app.api.post('/students')
def create_student(request):
    data = parse_payload(request)
    teacher_id = data.get('teacherId') or None
    teacher = Teacher.objects.filter(id=teacher_id).first() if teacher_id else None

    student = Student.objects.create(
        name=data.get('name', '').strip(),
        gender=data.get('gender') or 'male',
        date_of_birth=parse_date(data.get('dateOfBirth')),
        enrollment_date=parse_date(data.get('enrollmentDate')) or date.today(),
        current_juz=int(data.get('currentJuz') or 1),
        total_juz_memorized=int(data.get('totalJuzMemorized') or 0),
        goal_juz=int(data.get('goalJuz')) if data.get('goalJuz') else None,
        goal_date=parse_date(data.get('goalDate')),
        challenges=data.get('challenges') or None,
        teacher=teacher,
        status=data.get('status') or 'active',
    )
    update_milestone(student, student.total_juz_memorized)
    if student.last_milestone_juz:
        student.save(update_fields=['last_milestone_juz', 'muraja_only_until'])

    MurajaSchedule.objects.create(
        student=student,
        muraja_juz_per_day=get_muraja_daily_load(student.total_juz_memorized),
        cycle_length_days=7,
        next_revision_due_date=date.today() + timedelta(days=7),
        overdue=False,
    )

    return serialize_student(student)


@app.api.patch('/students/{student_id}')
def update_student(request, student_id: str):
    student = Student.objects.filter(id=student_id).first()
    if not student:
        raise HttpError(404, 'Student not found')

    data = parse_payload(request)
    previous_total = student.total_juz_memorized

    if 'name' in data:
        student.name = data.get('name') or student.name
    if 'gender' in data:
        student.gender = data.get('gender') or student.gender
    if 'dateOfBirth' in data:
        student.date_of_birth = parse_date(data.get('dateOfBirth'))
    if 'enrollmentDate' in data:
        student.enrollment_date = parse_date(data.get('enrollmentDate')) or student.enrollment_date
    if 'currentJuz' in data:
        student.current_juz = int(data.get('currentJuz') or student.current_juz)
    if 'totalJuzMemorized' in data:
        student.total_juz_memorized = int(data.get('totalJuzMemorized') or student.total_juz_memorized)
    if 'goalJuz' in data:
        student.goal_juz = int(data.get('goalJuz')) if data.get('goalJuz') else None
    if 'goalDate' in data:
        student.goal_date = parse_date(data.get('goalDate'))
    if 'challenges' in data:
        student.challenges = data.get('challenges') or None
    if 'teacherId' in data:
        teacher_id = data.get('teacherId')
        student.teacher = Teacher.objects.filter(id=teacher_id).first() if teacher_id else None
    if 'status' in data:
        student.status = data.get('status') or student.status

    update_milestone(student, student.total_juz_memorized)
    student.save()

    if student.total_juz_memorized != previous_total:
        schedule = MurajaSchedule.objects.filter(student=student).first()
        if schedule:
            schedule.muraja_juz_per_day = get_muraja_daily_load(student.total_juz_memorized)
            schedule.save(update_fields=['muraja_juz_per_day'])
    return serialize_student(student)


@app.api.delete('/students/{student_id}')
def delete_student(request, student_id: str):
    student = Student.objects.filter(id=student_id).first()
    if not student:
        raise HttpError(404, 'Student not found')

    DailyLesson.objects.filter(student=student).delete()
    Attendance.objects.filter(student=student).delete()
    Homework.objects.filter(student=student).delete()
    MonthlyPoints.objects.filter(student=student).delete()
    MurajaSchedule.objects.filter(student=student).delete()

    student.delete()
    return 204, {}


@app.api.get('/lessons')
def list_lessons(request):
    date_value = request.GET.get('date')
    student_id = request.GET.get('studentId')

    lessons = DailyLesson.objects.select_related('student')
    if date_value:
        lessons = lessons.filter(date=parse_date(date_value))
    if student_id:
        lessons = lessons.filter(student_id=student_id)

    return [serialize_lesson(lesson) for lesson in lessons]


@app.api.post('/lessons')
def create_lesson(request):
    data = parse_payload(request)
    student = Student.objects.filter(id=data.get('studentId')).first()
    if not student:
        raise HttpError(404, 'Student not found')

    lesson = DailyLesson.objects.create(
        student=student,
        date=parse_date(data.get('date')) or date.today(),
        lesson_type=data.get('lessonType') or 'NEW',
        juz=int(data.get('juz') or 1),
        surah=data.get('surah') or '',
        ayah_start=int(data.get('ayahStart') or 1),
        ayah_end=int(data.get('ayahEnd') or 1),
        comments=data.get('comments') or None,
        rating=data.get('rating') or 'Pass',
        extra_work=bool(data.get('extraWork')),
    )

    if lesson.rating == 'Pass':
        update_monthly_points(student, lesson)

    return serialize_lesson(lesson)


@app.api.get('/attendance')
def list_attendance(request):
    student_id = request.GET.get('studentId')
    start_date = parse_date(request.GET.get('startDate'))
    end_date = parse_date(request.GET.get('endDate'))

    records = Attendance.objects.all()
    if student_id:
        records = records.filter(student_id=student_id)
    if start_date:
        records = records.filter(date__gte=start_date)
    if end_date:
        records = records.filter(date__lte=end_date)

    return [serialize_attendance(record) for record in records]


@app.api.post('/attendance')
def upsert_attendance(request):
    data = parse_payload(request)
    student = Student.objects.filter(id=data.get('studentId')).first()
    if not student:
        raise HttpError(404, 'Student not found')

    record_date = parse_date(data.get('date')) or date.today()
    present = bool(data.get('present'))

    record = Attendance.objects.filter(student=student, date=record_date).first()
    if record:
        record.present = present
        record.save(update_fields=['present'])
    else:
        record = Attendance.objects.create(student=student, date=record_date, present=present)

    update_attendance_points(student, record_date.strftime('%Y-%m'))
    return serialize_attendance(record)


@app.api.get('/homework')
def list_homework(request):
    date_value = request.GET.get('date')
    student_id = request.GET.get('studentId')

    records = Homework.objects.select_related('student')
    if date_value:
        records = records.filter(date=parse_date(date_value))
    if student_id:
        records = records.filter(student_id=student_id)

    return [serialize_homework(record) for record in records]


@app.api.post('/homework')
def upsert_homework(request):
    data = parse_payload(request)
    student = Student.objects.filter(id=data.get('studentId')).first()
    if not student:
        raise HttpError(404, 'Student not found')

    record_date = parse_date(data.get('date')) or date.today()
    passed = bool(data.get('passed'))

    record = Homework.objects.filter(student=student, date=record_date).first()
    if record:
        record.passed = passed
        record.save(update_fields=['passed'])
    else:
        record = Homework.objects.create(student=student, date=record_date, passed=passed)

    return serialize_homework(record)


@app.api.get('/assessments')
def list_assessments(request):
    student_id = request.GET.get('studentId')
    start_date, end_date = date_range(request, default_days=90)

    records = Assessment.objects.select_related('student').filter(
        date__gte=start_date,
        date__lte=end_date,
    )
    if student_id:
        records = records.filter(student_id=student_id)

    return [serialize_assessment(record) for record in records]


@app.api.post('/assessments')
def create_assessment(request):
    data = parse_payload(request)
    student = Student.objects.filter(id=data.get('studentId')).first()
    if not student:
        raise HttpError(404, 'Student not found')

    record = Assessment.objects.create(
        student=student,
        date=parse_date(data.get('date')) or date.today(),
        type=data.get('type') or 'Test',
        score=int(data.get('score') or 0),
        notes=data.get('notes') or None,
    )
    return serialize_assessment(record)


@app.api.get('/points')
def list_points(request):
    month = request.GET.get('month')
    records = MonthlyPoints.objects.select_related('student')
    if month:
        records = records.filter(month=month)

    return [serialize_monthly_points(record) for record in records]


@app.api.post('/points')
def upsert_points(request):
    data = parse_payload(request)
    student = Student.objects.filter(id=data.get('studentId')).first()
    if not student:
        raise HttpError(404, 'Student not found')

    month = data.get('month') or date.today().strftime('%Y-%m')

    record, _ = MonthlyPoints.objects.update_or_create(
        student=student,
        month=month,
        defaults={
            'new_work_points': int(data.get('newWorkPoints') or 0),
            'front_work_points': int(data.get('frontWorkPoints') or 0),
            'back_work_points': int(data.get('backWorkPoints') or 0),
            'extra_work_points': int(data.get('extraWorkPoints') or 0),
            'attendance_points': int(data.get('attendancePoints') or 0),
            'behavior_points': int(data.get('behaviorPoints') or 0),
            'total_points': int(data.get('totalPoints') or 0),
        },
    )

    return serialize_monthly_points(record)


@app.api.get('/muraja')
def list_muraja(request):
    schedules = MurajaSchedule.objects.select_related('student')
    return [serialize_muraja_schedule(schedule) for schedule in schedules]


@app.api.get('/muraja/overdue')
def list_overdue_muraja(request):
    today = date.today()
    schedules = MurajaSchedule.objects.select_related('student').filter(
        models.Q(overdue=True)
        | models.Q(next_revision_due_date__lt=today)
    )
    return [serialize_muraja_schedule(schedule) for schedule in schedules]


@app.api.post('/muraja/recalculate')
def recalculate_muraja(request):
    today = date.today()
    schedules = MurajaSchedule.objects.select_related('student')

    for schedule in schedules:
        schedule.muraja_juz_per_day = get_muraja_daily_load(schedule.student.total_juz_memorized)
        schedule.overdue = bool(schedule.next_revision_due_date and schedule.next_revision_due_date < today)
        schedule.save(update_fields=['muraja_juz_per_day', 'overdue'])

    return {'status': 'ok'}


@app.api.post('/muraja/{schedule_id}/complete')
def complete_muraja(request, schedule_id: str):
    schedule = MurajaSchedule.objects.filter(id=schedule_id).first()
    if not schedule:
        raise HttpError(404, 'Schedule not found')

    next_due = date.today() + timedelta(days=schedule.cycle_length_days)
    schedule.next_revision_due_date = next_due
    schedule.overdue = False
    schedule.last_completed_date = date.today()
    schedule.save(update_fields=['next_revision_due_date', 'overdue', 'last_completed_date'])

    return serialize_muraja_schedule(schedule)


@app.api.get('/reports/student/{student_id}')
def report_student(request, student_id: str):
    student = Student.objects.filter(id=student_id).first()
    if not student:
        raise HttpError(404, 'Student not found')
    return student_progress_report(student)


@app.api.get('/reports/milestones')
def report_milestones(request):
    students = list(Student.objects.all())
    lesson_map = {
        str(student.id): lesson_range(student, 'NEW', None, None)
        for student in students
    }

    milestones = {}
    for juz in MILESTONE_WEEKS.keys():
        milestones[str(juz)] = [
            serialize_student(student)
            for student in students
            if student.total_juz_memorized >= juz
        ]

    percent_milestones = {}
    for percent in [25, 50, 75, 100]:
        percent_milestones[str(percent)] = [
            serialize_student(student)
            for student in students
            if (student.total_juz_memorized / 30) * 100 >= percent
        ]

    surah_milestones = {}
    for target in [10, 30, 60, 114]:
        surah_milestones[str(target)] = [
            serialize_student(student)
            for student in students
            if len({lesson.surah for lesson in lesson_map[str(student.id)]}) >= target
        ]

    return {
        'juzMilestones': milestones,
        'percentMilestones': percent_milestones,
        'surahMilestones': surah_milestones,
    }


@app.api.get('/reports/revision-status')
def report_revision_status(request):
    today = date.today()
    week_ago = today - timedelta(days=7)
    schedules = list(MurajaSchedule.objects.select_related('student'))

    overdue = [schedule for schedule in schedules if schedule.overdue or (schedule.next_revision_due_date and schedule.next_revision_due_date < today)]
    due = [schedule for schedule in schedules if schedule.next_revision_due_date == today]
    recently_completed = [schedule for schedule in schedules if schedule.last_completed_date and schedule.last_completed_date >= week_ago]
    muraja_only = [serialize_student(schedule.student) for schedule in schedules if schedule.student.muraja_only_until and schedule.student.muraja_only_until >= today]

    return {
        'overdue': [serialize_muraja_schedule(schedule) for schedule in overdue],
        'due': [serialize_muraja_schedule(schedule) for schedule in due],
        'recentlyCompleted': [serialize_muraja_schedule(schedule) for schedule in recently_completed],
        'murajaOnly': muraja_only,
    }


@app.api.get('/reports/top-memorizers')
def report_top_memorizers(request):
    start_date, end_date = date_range(request, default_days=30)
    lessons = DailyLesson.objects.select_related('student').filter(
        lesson_type='NEW',
        date__gte=start_date,
        date__lte=end_date,
    )

    stats = {}
    for lesson in lessons:
        key = str(lesson.student_id)
        if key not in stats:
            stats[key] = {
                'student': serialize_student(lesson.student),
                'newAyahs': 0,
                'newSurahs': set(),
                'lessonCount': 0,
            }
        stats[key]['newAyahs'] += ayah_count(lesson)
        stats[key]['newSurahs'].add(lesson.surah)
        stats[key]['lessonCount'] += 1

    ranked = [
        {
            'student': value['student'],
            'newAyahs': value['newAyahs'],
            'newSurahs': len(value['newSurahs']),
            'lessonCount': value['lessonCount'],
        }
        for value in stats.values()
    ]
    ranked.sort(key=lambda item: (item['newAyahs'], item['lessonCount']), reverse=True)
    return ranked[:10]


@app.api.get('/reports/struggling')
def report_struggling_students(request):
    today = date.today()
    start_date = today - timedelta(days=27)
    schedules = {str(s.student_id): s for s in MurajaSchedule.objects.select_related('student')}
    students = Student.objects.filter(status='active')
    results = []

    for student in students:
        lessons = lesson_range(student, 'NEW', start_date, today)
        avg_week = round(sum(ayah_count(lesson) for lesson in lessons) / 4, 1) if lessons else 0
        redo_count = DailyLesson.objects.filter(
            student=student,
            rating='Re-do',
            date__gte=start_date,
            date__lte=today,
        ).count()
        attendance = attendance_stats(student, start_date, today)
        homework = homework_stats(student, start_date, today)
        schedule = schedules.get(str(student.id))
        is_overdue = bool(schedule and (schedule.overdue or (schedule.next_revision_due_date and schedule.next_revision_due_date < today)))
        reasons = []
        if avg_week < 5:
            reasons.append('Low memorization rate')
        if redo_count >= 2:
            reasons.append('Repeated re-dos')
        if is_overdue:
            reasons.append('Overdue revision')
        if attendance['totalCount'] and attendance['attendanceRate'] < 80:
            reasons.append('Poor attendance')
        if homework['totalCount'] and homework['passRate'] < 70:
            reasons.append('Low homework pass rate')
        if reasons:
            results.append({
                'student': serialize_student(student),
                'averageAyahsPerWeek': avg_week,
                'overdue': is_overdue,
                'redoCount': redo_count,
                'attendanceRate': attendance['attendanceRate'],
                'homeworkPassRate': homework['passRate'],
                'reasons': reasons,
            })

    return results


@app.api.get('/reports/teacher-workload')
def report_teacher_workload(request):
    start_date, end_date = date_range(request, default_days=30)
    results = []

    for teacher in Teacher.objects.all():
        students = list(Student.objects.filter(teacher=teacher))
        lessons = list(DailyLesson.objects.filter(
            student__in=students,
            date__gte=start_date,
            date__lte=end_date,
        ))
        upcoming_assessments = Assessment.objects.filter(
            student__in=students,
            date__gte=date.today(),
            date__lte=date.today() + timedelta(days=30),
        ).count()

        total_ayahs = sum(ayah_count(lesson) for lesson in lessons)
        total_surahs = len({lesson.surah for lesson in lessons})
        results.append({
            'teacher': serialize_teacher(teacher),
            'studentCount': len(students),
            'lessonCount': len(lessons),
            'totalAyahs': total_ayahs,
            'totalSurahs': total_surahs,
            'upcomingAssessments': upcoming_assessments,
        })

    return results


@app.api.get('/reports/attendance')
def report_attendance(request):
    start_date, end_date = date_range(request, default_days=30)
    results = []
    students = Student.objects.filter(status='active')

    for student in students:
        records = Attendance.objects.filter(
            student=student,
            date__gte=start_date,
            date__lte=end_date,
        )
        present_count = records.filter(present=True).count()
        absent_count = records.filter(present=False).count()
        total = records.count()
        rate = round((present_count / total) * 100) if total else 0
        results.append({
            'student': serialize_student(student),
            'presentCount': present_count,
            'absentCount': absent_count,
            'attendanceRate': rate,
        })

    return results


@app.api.get('/reports/homework')
def report_homework(request):
    start_date, end_date = date_range(request, default_days=30)
    results = []
    students = Student.objects.filter(status='active')

    for student in students:
        stats = homework_stats(student, start_date, end_date)
        results.append({
            'student': serialize_student(student),
            'passedCount': stats['passedCount'],
            'failedCount': stats['failedCount'],
            'passRate': stats['passRate'],
            'totalCount': stats['totalCount'],
        })

    return results


@app.api.get('/reports/assessments')
def report_assessments(request):
    start_date, end_date = date_range(request, default_days=90)
    results = []
    scores = []

    for student in Student.objects.filter(status='active'):
        records = Assessment.objects.filter(
            student=student,
            date__gte=start_date,
            date__lte=end_date,
        ).order_by('-date')
        if not records.exists():
            continue
        average_score = round(sum(record.score for record in records) / records.count(), 1)
        last = records.first()
        scores.extend(record.score for record in records)
        results.append({
            'student': serialize_student(student),
            'averageScore': average_score,
            'lastScore': last.score,
            'lastDate': format_date(last.date),
            'lastType': last.type,
        })

    overall_average = round(sum(scores) / len(scores), 1) if scores else 0
    return {'averageScore': overall_average, 'items': results}


@app.api.get('/reports/goals')
def report_goals(request):
    today = date.today()
    results = []
    for student in Student.objects.filter(goal_juz__isnull=False):
        target = student.goal_juz or 0
        progress = round((student.total_juz_memorized / target) * 100, 1) if target else 0
        status = 'in_progress'
        if student.total_juz_memorized >= target:
            status = 'met'
        elif student.goal_date and student.goal_date < today:
            status = 'overdue'

        results.append({
            'student': serialize_student(student),
            'goalJuz': target,
            'goalDate': format_date(student.goal_date),
            'progressPercent': progress,
            'status': status,
        })

    return results
