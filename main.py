import threading
import unittest

from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI

# execute_command를 제어하는 콜백 함수
# -> 이 함수에서 시그널을 입력받고 처리하는 로직을 구성하면, 알아서 GUI에 연동이 됩니다.

# 속도, 전체 잠금 상태, 문 상태, 문 잠금 상태
DOOR_OPEN_CONDITION = {0, False, "CLOSED", "UNLOCKED"}
# 전체 잠금 상태, 문 상태
DOOR_CLOSE_CONDITION = {False, "OPEN"}
# 전체잠금, 차량 문 잠금, 문 상태
DOOR_LOCK_CONDITION = {False, "UNLOCKED", "CLOSED"}
# 전체잠금, 차량 문 잠금, 문 상태, 속도
DOOR_UNLOCK_CONDITION = {False, "LOCKED", "CLOSED", 0}


def execute_command_callback(command, car_controller):
    # 임찬우
    if command == "ENGINE_BTN":
        # 차량이 전체 잠금 상태가 아니면 엔진을 킬 수 있음

        if car_controller.get_lock_status() == False:
            if car_controller.get_engine_status() == False:
                car_controller.toggle_engine()

            # 엔진이 켜져 있을 때 속도가 0인지 확인 후 엔진을 끌 수 있는지 판단
            elif car_controller.get_engine_status() == True:
                if car_controller.get_speed() == 0:
                    car_controller.toggle_engine()  # 시동 OFF 가능


    # 송혜주
    elif command == "ACCELERATE":
        if (car_controller.get_lock_status() == False and
            car_controller.get_engine_status() == True and
            car_controller.get_left_door_status() == "CLOSED" and
            car_controller.get_right_door_status() == "CLOSED" and
            car_controller.get_speed() <= 120):

            car_controller.accelerate()  # 속도 +10

            if (car_controller.get_speed() >= 20):  # 속도가 20일 때 차 문을 잠그도록 함.
                car_controller.car.lock_left_door()
                car_controller.car.lock_right_door()



    elif command == "BRAKE":
        if (car_controller.get_lock_status() == False and
            car_controller.get_engine_status() == True and
            car_controller.get_speed() > 0):
            car_controller.brake()  # 속도 -10

    # 주정윤
    elif command == "LOCK":
        # 차량의 상태가 'unlock'이며, 속도가 10미만일 때만 차량 잠금 가능
        if car_controller.get_lock_status() == False and car_controller.get_speed() < 10:
            car_controller.lock_vehicle()  # 차량잠금

    elif command == "UNLOCK":
        # 차량의 상태가 'lock'일 때만 차량 잠금해제 가능
        if not car_controller.get_lock_status() == "LOCKED":
            car_controller.unlock_vehicle()  # 차량잠금해제



    # 이재헌
    elif command == "LEFT_DOOR_LOCK":
        # 차량이 잠겨있지 않고, 왼쪽문이 닫혀있을 때만 왼쪽문 잠금
        cur_left_door_lock_condition = set()

        cur_left_door_lock_condition.add(car_controller.get_lock_status())
        cur_left_door_lock_condition.add(car_controller.get_left_door_lock())
        cur_left_door_lock_condition.add(car_controller.get_left_door_status())

        if cur_left_door_lock_condition == DOOR_LOCK_CONDITION:
            car_controller.car.lock_left_door()  # 왼쪽문 잠금

    elif command == "LEFT_DOOR_UNLOCK":
        # 차량이 잠겨있지 않고, 왼쪽문이 닫혀있고, 속도가 0일 때만 왼쪽문 잠금해제
        cur_left_door_unlock_condition = set()
        cur_left_door_unlock_condition.add(car_controller.get_lock_status())
        cur_left_door_unlock_condition.add(car_controller.get_left_door_lock())
        cur_left_door_unlock_condition.add(
            car_controller.get_left_door_status())
        cur_left_door_unlock_condition.add(car_controller.get_speed())

        if cur_left_door_unlock_condition == DOOR_UNLOCK_CONDITION:
            car_controller.car.unlock_left_door()  # 왼쪽문 잠금해제

    elif command == "RIGHT_DOOR_LOCK":
        # 차량이 잠겨있지 않고, 오른쪽문이 닫혀있을 때만 오른쪽문 잠금
        cur_right_door_lock_condition = set()
        cur_right_door_lock_condition.add(car_controller.get_lock_status())
        cur_right_door_lock_condition.add(car_controller.get_right_door_lock())
        cur_right_door_lock_condition.add(
            car_controller.get_right_door_status())

        if cur_right_door_lock_condition == DOOR_LOCK_CONDITION:
            car_controller.car.lock_right_door()

    elif command == "RIGHT_DOOR_UNLOCK":
        # 차량이 잠겨있지 않고, 오른쪽문이 닫혀있고, 속도가 0일 때만 오른쪽문 잠금해제
        cur_right_door_unlock_condition = set()
        cur_right_door_unlock_condition.add(car_controller.get_lock_status())
        cur_right_door_unlock_condition.add(
            car_controller.get_right_door_lock())
        cur_right_door_unlock_condition.add(
            car_controller.get_right_door_status())
        cur_right_door_unlock_condition.add(car_controller.get_speed())

        if cur_right_door_unlock_condition == DOOR_UNLOCK_CONDITION:
            car_controller.car.unlock_right_door()

    # 한재일
    elif command == "LEFT_DOOR_OPEN":
        # 속도가 0이며, 차량 전체 잠금이 해제되어 있어야 합니다.
        # 차량 문이 닫혀 있어야 하고, 문이 잠겨 있지 않아야 합니다.
        # door_open_set_of_precondition = {0, False, "CLOSED", "UNLOCKED"} <- 차량 문 열기 동작의 필요 차량 상태를 미리 저장한 집합입니다.

        cur_car_status_set_for_door_open = set()  # 동작을 위해 필요한 차량의 현재 상태를 저장하기 위한 집합입니다.

        cur_car_status_set_for_door_open.add(car_controller.get_speed())
        cur_car_status_set_for_door_open.add(car_controller.get_lock_status())
        cur_car_status_set_for_door_open.add(
            car_controller.get_left_door_status())
        cur_car_status_set_for_door_open.add(
            car_controller.get_left_door_lock())

        # 차량의 속도, 전체 잠금 상태, 문 상태, 문 잠금 상태를 집합에 저장합니다.
        if cur_car_status_set_for_door_open == DOOR_OPEN_CONDITION:  # 차량의 현재 상태 집합과 동작의 필요 차량 상태 집합이 같은지 확인합니다.
            car_controller.open_left_door()  # 왼쪽문 열기

    elif command == "LEFT_DOOR_CLOSE":
        # 차량 전체 잠금이 해제되어 있어야 하며, 문이 열려있어야합니다.
        # door_close_set_of_precondition = {False, "OPENED"} <- 차량 문 닫기 동작의 필요 차량 상태를 미리 저장한 집합입니다.

        cur_car_status_set_for_door_close = set()  # 동작을 위해 필요한 차량의 현재 상태를 저장하기 위한 집합입니다.
        cur_car_status_set_for_door_close.add(car_controller.get_lock_status())
        cur_car_status_set_for_door_close.add(
            car_controller.get_left_door_status())
        # 차량의 전체 잠금 상태, 문 상태를 집합에 저장합니다.

        if cur_car_status_set_for_door_close == DOOR_CLOSE_CONDITION:  # 차량의 현재 상태 집합과 동작의 필요 차량 상태 집합이 같은지 확인합니다.
            car_controller.close_left_door()  # 왼쪽문 닫기


    elif command == "RIGHT_DOOR_OPEN":
        # 속도가 0이며, 차량 전체 잠금이 해제되어 있어야 합니다.
        # 차량 문이 닫혀 있어야 하고, 문이 잠겨 있지 않아야 합니다.
        # door_open_set_of_precondition = {0, False, "CLOSED", "UNLOCKED"} <- 차량 문 열기 동작의 필요 차량 상태를 미리 저장한 집합입니다.

        cur_car_status_set_for_door_open = set()  # 동작을 위해 필요한 차량의 현재 상태를 저장하기 위한 집합입니다.

        cur_car_status_set_for_door_open.add(car_controller.get_speed())
        cur_car_status_set_for_door_open.add(car_controller.get_lock_status())
        cur_car_status_set_for_door_open.add(
            car_controller.get_right_door_status())
        cur_car_status_set_for_door_open.add(
            car_controller.get_right_door_lock())
        # 차량의 속도, 전체 잠금 상태, 문 상태, 문 잠금 상태를 집합에 저장합니다.

        if cur_car_status_set_for_door_open == DOOR_OPEN_CONDITION:  # 차량의 현재 상태 집합과 동작의 필요 차량 상태 집합이 같은지 확인합니다.
            car_controller.open_right_door()  # 오른쪽문 열기

    elif command == "RIGHT_DOOR_CLOSE":
        # 차량 전체 잠금이 해제되어 있어야 하며, 문이 열려있어야합니다.
        # door_close_set_of_precondition = {False, "OPENED"} <- 차량 문 닫기 동작의 필요 차량 상태를 미리 저장한 집합입니다.

        cur_car_status_set_for_door_close = set()  # 동작을 위해 필요한 차량의 현재 상태를 저장하기 위한 집합입니다.

        cur_car_status_set_for_door_close.add(car_controller.get_lock_status())
        cur_car_status_set_for_door_close.add(
            car_controller.get_right_door_status())
        # 차량의 전체 잠금 상태, 문 상태를 집합에 저장합니다.

        if cur_car_status_set_for_door_close == DOOR_CLOSE_CONDITION:  # 차량의 현재 상태 집합과 동작의 필요 차량 상태 집합이 같은지 확인합니다.
            car_controller.close_right_door()  # 오른쪽문 닫기



    # 송국선
    elif command == "TRUNK_OPEN":
        # car_controller.open_trunk()  # 트렁크 열기
        trunk_open_condition_check(car_controller)
    elif command == "TRUNK_CLOSE":
        # car_controller.close_trunk()  # 트렁크 닫기
        trunk_close_condition_check(car_controller)

        # SOS 기능 추가
    elif command == "SOS":
        # 1. 속도를 0으로 설정
        if car_controller.get_speed() != 0:
            for i in range(car_controller.get_speed()):
                car_controller.brake()

        # 2. 모든 문의 잠금을 해제하고 열기
        car_controller.unlock_vehicle()
        car_controller.unlock_left_door()
        car_controller.unlock_right_door()
        car_controller.open_left_door()
        car_controller.open_right_door()

        # 3. 트렁크 열기
        car_controller.open_trunk()


def can_operate_trunk(car_controller, trunk_status):
    return (
        car_controller.get_speed() == 0 and
        not car_controller.get_lock_status() and
        car_controller.get_trunk_status() == trunk_status
    )


def trunk_open_condition_check(car_controller):
    if can_operate_trunk(car_controller, trunk_status=True):    # True = close
        car_controller.car.open_trunk()


def trunk_close_condition_check(car_controller):
    if can_operate_trunk(car_controller, trunk_status=False):   # False = open
        car_controller.car.close_trunk()


# 파일 경로를 입력받는 함수
# -> 가급적 수정하지 마세요.
#    테스트의 완전 자동화 등을 위한 추가 개선시에만 일부 수정이용하시면 됩니다. (성적 반영 X)
def file_input_thread(gui):
    while True:
        file_path = input(
            "Please enter the command file path (or 'exit' to quit): ")

        if file_path.lower() == 'exit':
            print("Exiting program.")
            break

        # 파일 경로를 받은 후 GUI의 mainloop에서 실행할 수 있도록 큐에 넣음
        gui.window.after(0, lambda: gui.process_commands(file_path))


# 메인 실행
# -> 가급적 main login은 수정하지 마세요.
if __name__ == "__main__":
    car = Car()
    car_controller = CarController(car)

    # GUI는 메인 스레드에서 실행
    gui = CarSimulatorGUI(car_controller,
                          lambda command: execute_command_callback(command,
                                                                   car_controller))

    # 파일 입력 스레드는 별도로 실행하여, GUI와 병행 처리
    input_thread = threading.Thread(target=file_input_thread, args=(gui,))
    input_thread.daemon = True  # 메인 스레드가 종료되면 서브 스레드도 종료되도록 설정
    input_thread.start()

    # GUI 시작 (메인 스레드에서 실행)
    gui.start()
