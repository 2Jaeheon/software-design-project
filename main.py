import threading
import unittest
import argparse
import sys

from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI


class TestSOSFunctionality(unittest.TestCase):

    def test_sos_functionality(self):
        car_controller = CarController(Car())
        # SOS 신호 보내기
        execute_command_callback("SOS", car_controller)

        # 테스트 assertions
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertFalse(car_controller.get_trunk_status())

    # 차량이 잠겨 있을 때 SOS 호출 테스트
    def test_sos_when_locked(self):
        car_controller = CarController(Car())
        car_controller.lock_vehicle()  # 차량 잠금

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertFalse(car_controller.get_trunk_status())

    # 차량이 잠겨 있지 않을 때 SOS 호출 테스트
    def test_sos_when_unlocked_and_speed_one(self):
        car_controller = CarController(Car())
        car_controller.unlock_vehicle()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertFalse(car_controller.get_trunk_status())

    # 엔진이 켜져 있을 때 SOS 호출 테스트
    def test_sos_when_engine_on(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        car_controller.toggle_engine()  # 엔진 켜기

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertFalse(car_controller.get_trunk_status())

    # 엔진이 꺼져 있을 때 SOS 호출 테스트
    def test_sos_when_engine_off(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        if (car_controller.get_engine_status() == True):
            car_controller.toggle_engine()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertFalse(car_controller.get_trunk_status())

    # 문이 잠겨 있을 때 SOS 호출 테스트
    def test_sos_when_doors_locked(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        car_controller.lock_left_door()
        car_controller.lock_right_door()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertFalse(car_controller.get_trunk_status())

    # 문이 잠겨 있지 않을 때 SOS 호출 테스트
    def test_sos_when_doors_unlocked(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        car_controller.unlock_left_door()
        car_controller.unlock_right_door()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertFalse(car_controller.get_trunk_status())

    # 트렁크가 열려 있을 때 SOS 호출 테스트
    def test_sos_when_trunk_open(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        car_controller.open_trunk()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertFalse(car_controller.get_trunk_status())

    # 트렁크가 닫혀 있을 때 SOS 호출 테스트
    def test_sos_when_trunk_closed(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        car_controller.close_trunk()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertFalse(car_controller.get_trunk_status())

    # 속도가 0이 아닐 때 SOS 호출 테스트
    def test_sos_when_speed_not_zero(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        car_controller.accelerate()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertFalse(car_controller.get_trunk_status())

    # 속도가 120을 넘어갈 때 SOS 호출 테스트
    def test_sos_when_speed_over_120(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        for i in range(13):
            car_controller.accelerate()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertFalse(car_controller.get_trunk_status())


class TestLockDoorFunctionality(unittest.TestCase):
    def test_lock_door_functionality(self):
        car_controller = CarController(Car())

        execute_command_callback("UNLOCK", car_controller)

        execute_command_callback("LEFT_DOOR_LOCK", car_controller)
        self.assertEqual(car_controller.get_left_door_lock(), "LOCKED")

        execute_command_callback("RIGHT_DOOR_LOCK", car_controller)
        self.assertEqual(car_controller.get_right_door_lock(), "LOCKED")

        execute_command_callback("UNLOCK", car_controller)

        execute_command_callback("LEFT_DOOR_UNLOCK", car_controller)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")

        execute_command_callback("RIGHT_DOOR_UNLOCK", car_controller)
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")

    # 차량의 속도가 20을 넘어갈 때 문이 잠겼는지 잠금 테스트
    def test_auto_lock_doors_on_speed(self):
        car_controller = CarController(Car())

        execute_command_callback("UNLOCK", car_controller)
        execute_command_callback("LEFT_DOOR_UNLOCK", car_controller)
        execute_command_callback("RIGHT_DOOR_UNLOCK", car_controller)
        execute_command_callback("ENGINE_BTN", car_controller)
        execute_command_callback("ACCELERATE", car_controller)
        execute_command_callback("ACCELERATE", car_controller)
        execute_command_callback("ACCELERATE", car_controller)
        self.assertEqual(car_controller.get_left_door_lock(), "LOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "LOCKED")

    # 속도가 0일 때 문 잠금 해제 테스트
    def test_unlock_doors_at_zero_speed(self):
        car_controller = CarController(Car())

        # 속도가 0일 때 문 잠금 해제
        execute_command_callback("UNLOCK", car_controller)
        execute_command_callback("LEFT_DOOR_UNLOCK", car_controller)
        execute_command_callback("RIGHT_DOOR_UNLOCK", car_controller)
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")

        # 속도가 0이 아닐때 문 잠금 해제 불가능
        execute_command_callback("LEFT_DOOR_LOCK", car_controller)
        execute_command_callback("RIGHT_DOOR_LOCK", car_controller)
        execute_command_callback("ENGINE_BTN", car_controller)
        execute_command_callback("ACCELERATE", car_controller)
        execute_command_callback("LEFT_DOOR_UNLOCK", car_controller)
        execute_command_callback("RIGHT_DOOR_UNLOCK", car_controller)
        self.assertEqual(car_controller.get_left_door_lock(), "LOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "LOCKED")

    # 차량이 잠겨 있을 때 문 잠금, 잠금해제 불가능 테스트
    def test_lock_doors_when_vehicle_is_locked(self):
        car_controller = CarController(Car())
        # 차량 잠금 상태에서 잠금, 잠금해제 불가능
        execute_command_callback("UNLOCK", car_controller)
        execute_command_callback("LEFT_DOOR_LOCK", car_controller)
        execute_command_callback("RIGHT_DOOR_LOCK", car_controller)
        execute_command_callback("LOCK", car_controller)
        execute_command_callback("LEFT_DOOR_UNLOCK", car_controller)
        execute_command_callback("RIGHT_DOOR_UNLOCK", car_controller)
        self.assertEqual(car_controller.get_left_door_lock(), "LOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "LOCKED")

    # 문이 닫혀있을 때만 잠금 가능 테스트
    def test_lock_doors_when_doors_are_closed(self):
        car_controller = CarController(Car())

        execute_command_callback("UNLOCK", car_controller)
        execute_command_callback("LEFT_DOOR_CLOSE", car_controller)
        execute_command_callback("RIGHT_DOOR_CLOSE", car_controller)
        execute_command_callback("LEFT_DOOR_LOCK", car_controller)
        execute_command_callback("RIGHT_DOOR_LOCK", car_controller)
        self.assertEqual(car_controller.get_left_door_lock(), "LOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "LOCKED")

        # 문이 닫혀있지 않을 때 잠금 불가능
        execute_command_callback("LEFT_DOOR_UNLOCK", car_controller)
        execute_command_callback("RIGHT_DOOR_UNLOCK", car_controller)
        execute_command_callback("LEFT_DOOR_OPEN", car_controller)
        execute_command_callback("RIGHT_DOOR_OPEN", car_controller)
        execute_command_callback("LEFT_DOOR_LOCK", car_controller)
        execute_command_callback("RIGHT_DOOR_LOCK", car_controller)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")


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
# 전체잠금, 엔진 상태, 왼쪽 문 상태, 오른쪽 문 상태, 속도
ACCELERATE_CONDITION = {False, True, "CLOSED", "CLOSED", True}
# 전체잠금, 엔진 상태, 속도
BRAKE_CONDITION = {False, True, True}


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
        # 차량이 잠겨있지 않고, 엔진이 켜져있고, 왼쪽/오른쪽 문이 닫혀있고, 속도가 120 미만일 때 엑셀 페달 가동 가능
        cur_accelerate_condition = set()

        cur_accelerate_condition.add(car_controller.get_lock_status())
        cur_accelerate_condition.add(car_controller.get_engine_status())
        cur_accelerate_condition.add(car_controller.get_left_door_status())
        cur_accelerate_condition.add(car_controller.get_right_door_status())
        cur_accelerate_condition.add(car_controller.get_speed() < 120)

        if cur_accelerate_condition == ACCELERATE_CONDITION:
            car_controller.accelerate()  # 속도 +10

            if (car_controller.get_speed() >= 20):  # 속도가 20일 때 차 문을 잠그도록 함.
                car_controller.car.lock_left_door()
                car_controller.car.lock_right_door()

    elif command == "BRAKE":
        # 차량이 잠겨있지 않고, 엔진이 켜져있고, 속도가 0 이상일 때 브레이크 페달 가동 가능
        cur_brake_condition = set()

        cur_brake_condition.add(car_controller.get_lock_status())
        cur_brake_condition.add(car_controller.get_engine_status())
        cur_brake_condition.add(car_controller.get_speed() > 0)

        if cur_brake_condition == BRAKE_CONDITION:
            car_controller.brake()  # 속도 -10

    
    # 주정윤
    elif command == "LOCK":
        # 차량의 상태가 'unlock'이며, 속도가 10미만일 때만 차량 잠금 가능
        if car_controller.get_lock_status() == False and car_controller.get_speed() < 10:
            car_controller.lock_vehicle()  # 차량잠금

    elif command == "UNLOCK":
        # 차량의 상태가 'lock'일 때만 차량 잠금해제 가능
        if car_controller.get_lock_status() == True:
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
        car_controller.unlock_vehicle()

        # 1. 속도를 0으로 설정
        if car_controller.get_speed() != 0:
            for i in range(car_controller.get_speed()):
                car_controller.brake()

        # 2. 모든 문의 잠금을 해제하고 열기
        car_controller.unlock_left_door()
        car_controller.unlock_right_door()

        # 3. 트렁크 열기
        car_controller.open_trunk()


def can_operate_trunk(car_controller, trunk_status):
    return (
        car_controller.get_speed() == 0 and
        not car_controller.get_lock_status() and
        car_controller.get_trunk_status() == trunk_status
    )


def trunk_open_condition_check(car_controller):
    if can_operate_trunk(car_controller, trunk_status=True):
        car_controller.open_trunk()


def trunk_close_condition_check(car_controller):
    if can_operate_trunk(car_controller, trunk_status=False):
        car_controller.close_trunk()


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
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()

    car = Car()
    car_controller = CarController(car)

    if args.test:
        unittest.main(argv=[sys.argv[0]])

    else:
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
