from npu_core import mac_score

import random
import time


SIZES = [25, 100, 1000, 2000]
REPEAT = 10


# 크기에 맞는 Cross 필터, X 필터, 랜덤 패턴을 생성한다.
def make_data(size):
    print(f'{size}x{size} Cross 필터 생성 중...', flush=True)

    crossFilter = []
    center = size // 2

    for i in range(size):
        if i == center:
            row = [1.0] * size
        else:
            row = [0.1] * size
            row[center] = 1.0

        crossFilter.append(row)

    print(f'{size}x{size} X 필터 생성 중...', flush=True)

    xFilter = []

    for i in range(size):
        row = [0.1] * size
        row[i] = 1.0
        row[size - 1 - i] = 1.0
        xFilter.append(row)

    print(f'{size}x{size} 랜덤 패턴 생성 중...', flush=True)

    pattern = []

    for _ in range(size):
        pattern.append(random.choices((0, 1), k=size))

    print('데이터 생성 완료')
    return crossFilter, xFilter, pattern


# 2차원 배열을 1차원 배열로 변환한다.
def flatten(matrix):
    return [value for row in matrix for value in row]


# 1차원 필터와 패턴의 MAC 점수를 계산한다.
def mac_flat(filterList, pattern):
    score = 0

    for i in range(len(filterList)):
        score += filterList[i] * pattern[i]

    return score


# 기존 2차원 방식으로 Cross와 X의 MAC 점수를 계산한다.
def current_mode(crossFilter, xFilter, pattern):
    crossScore = mac_score(crossFilter, pattern)
    xScore = mac_score(xFilter, pattern)
    return crossScore, xScore


# 1차원 직렬 방식으로 Cross와 X의 MAC 점수를 계산한다.
def flat_mode(crossFilter, xFilter, pattern):
    crossScore = mac_flat(crossFilter, pattern)
    xScore = mac_flat(xFilter, pattern)
    return crossScore, xScore


# 전달받은 계산을 반복 실행하여 평균 시간을 구한다.
def check_time(function, *args):
    elapsedTimes = []
    result = None

    for _ in range(REPEAT):
        start = time.perf_counter()
        result = function(*args)
        end = time.perf_counter()
        elapsedTimes.append((end - start) * 1000)

    averageTime = sum(elapsedTimes) / len(elapsedTimes)
    return result, averageTime


# 2D와 1D 방식의 계산 결과가 오차 범위 안에서 같은지 확인한다.
def same_result(currentResult, flatResult):
    crossSame = abs(currentResult[0] - flatResult[0]) < 1e-9
    xSame = abs(currentResult[1] - flatResult[1]) < 1e-9
    return crossSame and xSame


# 한 가지 배열 크기에 대해 2D와 1D 연산 시간을 측정한다.
def run_benchmark(size):
    print()
    print('=' * 60)
    print(f'{size}x{size} 성능 테스트 시작')
    print('=' * 60)
    print(f'반복 측정: {REPEAT}회')
    print()

    crossFilter, xFilter, pattern = make_data(size)

    print('\n현재 2D 방식 측정 중...', flush=True)
    currentResult, currentTime = check_time(current_mode, crossFilter, xFilter, pattern)

    print('1D 데이터 변환 중...', flush=True)
    start = time.perf_counter()
    flatCross = flatten(crossFilter)
    flatX = flatten(xFilter)
    flatPattern = flatten(pattern)
    flatPrepareTime = (time.perf_counter() - start) * 1000

    print('1D 직렬 방식 측정 중...', flush=True)
    flatResult, flatTime = check_time(flat_mode, flatCross, flatX, flatPattern)
    flatTotalTime = flatPrepareTime + flatTime

    print()
    print('-' * 60)
    print(f'{size}x{size} 측정 결과')
    print('-' * 60)
    print(f'현재 2D 계산       : {currentTime:.6f} ms')
    print(f'1D 직렬 계산       : {flatTime:.6f} ms')
    print(f'2D → 1D 변환      : {flatPrepareTime:.6f} ms')
    print(f'변환 포함 1D 전체  : {flatTotalTime:.6f} ms')
    print(f'2D와 1D 결과 일치 : {same_result(currentResult, flatResult)}')

    return {
        'size': size,
        'currentTime': currentTime,
        'flatTime': flatTime,
        'flatPrepareTime': flatPrepareTime,
        'flatTotalTime': flatTotalTime,
        'same': same_result(currentResult, flatResult)
    }


# 모든 배열 크기의 측정 결과를 표 형태로 출력한다.
def print_summary(results):
    print()
    print('=' * 78)
    print('전체 성능 테스트 결과')
    print('=' * 78)
    print(f'{"크기":<12}{"2D 계산(ms)":>15}{"1D 계산(ms)":>15}{"변환(ms)":>15}{"1D 전체(ms)":>15}')
    print('-' * 78)

    for result in results:
        sizeName = f'{result["size"]}x{result["size"]}'
        print(f'{sizeName:<12}{result["currentTime"]:>15.3f}{result["flatTime"]:>15.3f}{result["flatPrepareTime"]:>15.3f}{result["flatTotalTime"]:>15.3f}')

    print()
    print('결과 일치 여부')

    for result in results:
        sizeName = f'{result["size"]}x{result["size"]}'
        print(f'{sizeName:<12}{result["same"]}')


# 설정된 모든 배열 크기의 벤치마크를 순서대로 실행한다.
def main():
    random.seed(42)

    print('=' * 60)
    print('2D와 1D MAC 성능 비교')
    print('=' * 60)
    print('테스트 크기: ' + ', '.join(f'{size}x{size}' for size in SIZES))
    print(f'반복 측정: {REPEAT}회')

    results = []

    for size in SIZES:
        results.append(run_benchmark(size))

    print_summary(results)


if __name__ == '__main__':
    main()
