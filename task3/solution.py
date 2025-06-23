def appearance(intervals: dict[str, list[int]]) -> int:
    same_time = 0
    lesson_time = (intervals['lesson'][0], intervals['lesson'][1])
    if len(intervals["pupil"]) == 0 or len(intervals["tutor"]) == 0:
        return 0
    pupil_intervals = merge_intervals(intervals["pupil"])
    tutor_intervals = merge_intervals(intervals["tutor"])
    for i in range(0, len(pupil_intervals)):
        pupil_time = (pupil_intervals[i][0], pupil_intervals[i][1])
        for j in range(0, len(tutor_intervals)): 
            tutor_time = (tutor_intervals[j][0], tutor_intervals[j][1])
            result = check_interval_overlap(lesson_time, pupil_time, tutor_time)
            if result[0]:
                same_time += result[2] - result[1]
    return same_time

def merge_intervals(events):
    intervals = [(events[i], events[i+1]) for i in range(0, len(events), 2)]
    intervals_sorted = sorted(intervals, key=lambda x: x[0])
    merged = []
    current_start, current_end = intervals_sorted[0]
    for start, end in intervals_sorted[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end
    merged.append((current_start, current_end))
    return merged

def check_interval_overlap(lesson, interval1, interval2):
    lesson_start, lesson_end = lesson
    start1, end1 = interval1
    start2, end2 = interval2
    return (max(start1, start2) < min(end1, end2),
            max(lesson_start, start1, start2),
            min(lesson_end, end1, end2))

tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },

    # Добавленные тесты
    # 1. Нет пересечений
    {'intervals': {
        'lesson': [10, 20],
        'pupil': [1, 2, 3, 5],
        'tutor': [21, 25]
    }, 'answer': 0},
    
    # 2. Полное покрытие урока
    {'intervals': {
        'lesson': [10, 20],
        'pupil': [5, 25],
        'tutor': [5, 25]
    }, 'answer': 10},
    
    # 3. Интервалы внутри урока
    {'intervals': {
        'lesson': [10, 20],
        'pupil': [11, 15],
        'tutor': [12, 18]
    }, 'answer': 3},
    
    # 4. Выход за границы урока
    {'intervals': {
        'lesson': [10, 20],
        'pupil': [8, 25],
        'tutor': [5, 15]
    }, 'answer': 5},
    
    # 5. Множественные интервалы
    {'intervals': {
        'lesson': [10, 20],
        'pupil': [9, 12, 15, 18],
        'tutor': [11, 16]
    }, 'answer': 2},
    
    # 6. Граничные условия (совпадают с уроком)
    {'intervals': {
        'lesson': [10, 20],
        'pupil': [10, 20],
        'tutor': [10, 20]
    }, 'answer': 10},
    
    # 7. Пустые интервалы (ученик)
    {'intervals': {
        'lesson': [10, 20],
        'pupil': [],
        'tutor': [12, 18]
    }, 'answer': 0},
    
    # 8. Очень маленькое перекрытие (1 секунда)
    {'intervals': {
        'lesson': [10, 20],
        'pupil': [10, 11],
        'tutor': [10, 11]
    }, 'answer': 1},
    
    # 9. Соприкосновение без перекрытия
    {'intervals': {
        'lesson': [10, 20],
        'pupil': [10, 15],
        'tutor': [15, 20]
    }, 'answer': 0},
    
    # 10. Пересечение частично в уроке
    {'intervals': {
        'lesson': [60, 75],
        'pupil': [50, 80],
        'tutor': [70, 90]
    }, 'answer': 5},

    # 11. Большие числа
    {'intervals': {
        'lesson': [10**15, 10**15 + 1000],
        'pupil': [10**15 + 100, 10**15 + 900],
        'tutor': [10**15 + 200, 10**15 + 800]
    }, 'answer': 600},
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       print(f'Test {i}')
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'