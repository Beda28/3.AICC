from npu_core import pattern_input, check_time

def user_mode():
    print('필터 A를 입력해주세요')
    filterA = pattern_input(3)

    print('필터 B를 입력해주세요')
    filterB = pattern_input(3)

    print('비교할 패턴을 입력해주세요')
    pattern = pattern_input(3)

    Amac, Bmac, averageTime = check_time(filterA, filterB, pattern)

    if abs(Amac - Bmac) < 1e-9: result = '판정 불가'
    elif Amac > Bmac          : result = 'A 필터'
    else                      : result = 'B 필터'

    print(f'A: {Amac} vs B: {Bmac}')
    print(f'판정 결과: {result}')
    print(f'\n평균 연산 시간: {averageTime:.6f} ms')