from json_utils import labeling, check_case
from npu_core import check_time
import json

epsilon = 1e-9

def json_mode():
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    filters  = data['filters']
    patterns = data['patterns']

    passCount       = 0
    failCount       = 0
    failedCases     = []
    performanceData = {}

    for caseName, caseData in patterns.items():
        validatedData, error = check_case(caseName, caseData, filters)

        if error is not None:
            failCount += 1
            failedCases.append((caseName, '데이터 오류', error))

            print('=' * 35)
            print(f'테스트 케이스: {caseName}')
            print('테스트 결과: FAIL')
            print(f'데이터 오류: {error}')
            continue

        size, pattern, crossFilter, xFilter, expected = validatedData
        expected = labeling(expected)

        crossScore, xScore, averageTime = check_time(crossFilter, xFilter, pattern)

        if size not in performanceData:
            performanceData[size] = []

        performanceData[size].append(averageTime)

        if abs(crossScore - xScore) < epsilon:
            result = 'UNDECIDED'
        elif crossScore > xScore:
            result = 'Cross'
        else:
            result = 'X'

        if result == expected:
            status = 'PASS'
            passCount += 1
        else:
            status = 'FAIL'
            failCount += 1
            failedCases.append((caseName, expected, result))

        print('=' * 35)
        print(f'테스트 케이스: {caseName}')
        print(f'필터 크기: {size}x{size}')
        print(f'+ 점수: {crossScore:.6f}')
        print(f'X 점수: {xScore:.6f}')
        print(f'판정 결과: {result}')
        print(f'예상 결과: {expected}')
        print(f'테스트 결과: {status}')
        print(f'평균 실행 시간(10회): {averageTime:.6f} ms')

    print()
    print('=' * 35)
    print('전체 테스트 결과')
    print(f'전체 케이스: {len(patterns)}')
    print(f'통과: {passCount}')
    print(f'실패: {failCount}')

    print('\n실패 케이스')
    if failedCases:
        for caseName, expected, actual in failedCases:
            if expected == '데이터 오류':
                print(f'{caseName} / FAIL / {actual}')
            else:
                print(f'{caseName} / expected: {expected} / actual: {actual}')
    else:
        print('없음')

    print('\n성능 분석')
    print('크기      평균 시간(ms)      연산 횟수')

    for size in sorted(performanceData):
        times          = performanceData[size]
        averageTime    = sum(times) / len(times)
        operationCount = 2 * size ** 2

        print(f'{size}x{size:<7} {averageTime:<18.6f} {operationCount}')