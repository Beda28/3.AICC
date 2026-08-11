from user_mode import user_mode
from json_mode import json_mode

def main():
    print("=== Mini NPU Simulator ===")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    mode = input("선택: ").strip()

    if mode == "1":
        user_mode()
    elif mode == "2":
        json_mode()
    else:
        print("잘못된 선택입니다.")

if __name__ == "__main__":
    main()