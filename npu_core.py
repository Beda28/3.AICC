import time

def pattern_input(line=3):
    pattern = []

    for i in range(line):
        while True:
            try:
                row = list(map(int, input(f'{i + 1}행 입력: ').split()))

                if len(row) != line:
                    print(f'입력 형식 오류: 숫자를 {line}개 입력하세요.')
                    continue

                pattern.append(row)
                break

            except ValueError: print('입력 형식 오류: 숫자만 입력하세요.')
    print('')
    return pattern

def mac_score(filter_List: list, pattern: list):
    score = 0
    for i in range(len(filter_List)):
        for j in range(len(filter_List[i])):
            score += filter_List[i][j] * pattern[i][j]
    return score

def check_time(crossFilter, xFilter, pattern):
    elapsedTimes = []

    for _ in range(10):
        start      = time.perf_counter()
        crossScore = mac_score(crossFilter, pattern)
        xScore     = mac_score(xFilter, pattern)
        end        = time.perf_counter()
        elapsedTimes.append(end - start)

    averageTime = sum(elapsedTimes) / 10 * 1000
    return crossScore, xScore, averageTime
