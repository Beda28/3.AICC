def labeling(label):
    if not isinstance(label, str): return label

    label = label.lower()
    if label == '+' or label == 'cross':
        return 'Cross'
    elif label == 'x' : return 'X'

    return label


def check_size(caseName):
    parts = caseName.split('_')

    if len(parts) != 3 or parts[0] != 'size'           : return None
    if not parts[1].isdigit() or not parts[2].isdigit(): return None

    size = int(parts[1])
    if     size <= 0: return None
    return size

def check_error(matrix, size, matrixName):
    if not isinstance(matrix, list) or len(matrix) != size:
        return f'잘못된 {matrixName} 크기'

    for row in matrix:
        if not isinstance(row, list) or len(row) != size:
            return f'잘못된 {matrixName} 행 길이'

        for value in row:
            if type(value) not in (int, float):
                return f'{matrixName}에 숫자가 아닌 데이터가 있음'

    return None

def check_case(caseName, caseData, filters):
    size = check_size(caseName)
    if size is None: return None, '잘못된 테스트 케이스 이름 형식'

    filterName = f'size_{size}'
    if filterName not in filters: return None, f'{filterName} 필터가 없음'

    sizeFilter = filters[filterName]
    if not isinstance(sizeFilter, dict): return None, f'{filterName} 필터 형식 오류'
    if 'cross' not in sizeFilter       : return None, 'cross 필터가 없음'
    if 'x' not in sizeFilter           : return None, 'x 필터가 없음'
    if not isinstance(caseData, dict) or 'input' not in caseData: 
                                         return None, '패턴 데이터가 없음'
    if 'expected' not in caseData      : return None, '예상 라벨이 없음'

    pattern     = caseData['input']
    crossFilter = sizeFilter['cross']
    xFilter     = sizeFilter['x']

    error = check_error(pattern, size, '패턴')
    if error is None    : error = check_error(crossFilter, size, 'Cross 필터')
    if error is None    : error = check_error(xFilter, size, 'X 필터')
    if error is not None: return None, error

    return (size, pattern, crossFilter, xFilter, caseData['expected']), None
