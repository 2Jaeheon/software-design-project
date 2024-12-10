import threading
import unittest
import argparse
import sys

from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI


class TestSOSFunctionality(unittest.TestCase):
    def sos_conditions(self, car_controller):
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertFalse(car_controller.get_trunk_status())


    def test_sos_functionality(self):
        car_controller = CarController(Car())
        # SOS 신호 보내기
        execute_command_callback("SOS", car_controller)

        # 테스트 assertions
        self.sos_conditions(car_controller)

    # 차량이 잠겨 있을 때 SOS 호출 테스트
    def test_sos_when_locked(self):
        car_controller = CarController(Car())
        car_controller.lock_vehicle()  # 차량 잠금

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.sos_conditions(car_controller)

    # 차량이 잠겨 있지 않을 때 SOS 호출 테스트
    def test_sos_when_unlocked_and_speed_one(self):
        car_controller = CarController(Car())
        car_controller.unlock_vehicle()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.sos_conditions(car_controller)

    # 엔진이 켜져 있을 때 SOS 호출 테스트
    def test_sos_when_engine_on(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        car_controller.toggle_engine()  # 엔진 켜기

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.sos_conditions(car_controller)

    # 엔진이 꺼져 있을 때 SOS 호출 테스트
    def test_sos_when_engine_off(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        if (car_controller.get_engine_status() == True):
            car_controller.toggle_engine()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.sos_conditions(car_controller)

    # 문이 잠겨 있을 때 SOS 호출 테스트
    def test_sos_when_doors_locked(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        car_controller.lock_left_door()
        car_controller.lock_right_door()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.sos_conditions(car_controller)

    # 문이 잠겨 있지 않을 때 SOS 호출 테스트
    def test_sos_when_doors_unlocked(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        car_controller.unlock_left_door()
        car_controller.unlock_right_door()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.sos_conditions(car_controller)

    # 트렁크가 열려 있을 때 SOS 호출 테스트
    def test_sos_when_trunk_open(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        car_controller.open_trunk()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.sos_conditions(car_controller)

    # 트렁크가 닫혀 있을 때 SOS 호출 테스트
    def test_sos_when_trunk_closed(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        car_controller.close_trunk()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.sos_conditions(car_controller)

    # 속도가 0이 아닐 때 SOS 호출 테스트
    def test_sos_when_speed_not_zero(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        car_controller.accelerate()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.sos_conditions(car_controller)

    # 속도가 120을 넘어갈 때 SOS 호출 테스트
    def test_sos_when_speed_over_120(self):
        car_controller = CarController(Car())

        car_controller.unlock_vehicle()
        for i in range(13):
            car_controller.accelerate()

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.sos_conditions(car_controller)

    # SOS 여러 번 호출
    def test_sos_multiple(self):
        car_controller = CarController(Car())

        # 비정상적인 초기 상태 설정
        car_controller.unlock_vehicle()
        car_controller.toggle_engine()
        car_controller.open_trunk()
        car_controller.accelerate()

        execute_command_callback("SOS", car_controller)
        execute_command_callback("SOS", car_controller)

        # 1차 Assertions
        self.sos_conditions(car_controller)

        execute_command_callback("SOS", car_controller)

        # 2차 Assertions
        self.sos_conditions(car_controller)

    # 다양한 잘못된 상태에 있을 때의 경우 테스트(경계값 테스트)
    def test_sos_invalid_state(self):
        car_controller = CarController(Car())

        # 비정상적인 상태 조합 설정
        car_controller.unlock_vehicle()
        car_controller.toggle_engine()
        car_controller.open_trunk()
        car_controller.lock_left_door()
        car_controller.accelerate()
        car_controller.open_left_door()
        # 상태:
        # 잠금 해제
        # 엔진 켜짐, 트렁크 개방, 좌측 문 잠금, 속도 10km/h, 좌측 문 열림

        execute_command_callback("SOS", car_controller)

        # Assertions
        self.sos_conditions(car_controller)


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
        execute_command_callback("BRAKE ENGINE_BTN", car_controller)
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
        execute_command_callback("BRAKE ENGINE_BTN", car_controller)
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

unit_test_file_list_ON_True = [
    ".\example_engin_for_unitTest_ON_1_True",
    ".\example_engin_for_unitTest_ON_2_True",
]
unit_test_file_list_ON_False = [
    ".\example_engin_for_unitTest_ON_3_False",
    ".\example_engin_for_unitTest_ON_4_False",
    ".\example_engin_for_unitTest_ON_5_False",
    ".\example_engin_for_unitTest_ON_6_False",
]

unit_test_file_list_OFF_True = [
    ".\example_engin_for_unitTest_OFF_2_True"
]
unit_test_file_list_OFF_False = [
    ".\example_engin_for_unitTest_OFF_1_False"
] # 유닛 테스트를 위한 입력값이 저장된 파일들

def test_engin_functionality(self, error_file : list, file_list : list, expect : bool) -> list:
        for file_path in file_list :
            try:
                unitTest_File = open(file_path, 'r')
                commands = unitTest_File.read().splitlines()
                # 유닛 테스트를 위한 명령어가 입력된 파일을 읽어오고, 각 줄의 명령어를 commands에 저장
                car_controller = CarController(Car())

                for command in commands :
                    print(command)
                    execute_command_callback(command, car_controller)
                # 각 명령어를 execute_command_callback 함수를 통해 시행
                print(file_path)
                unitTest_File.close()
                if expect :
                    self.assertTrue(car_controller.get_engine_status())
                else :
                    self.assertFalse(car_controller.get_engine_status())
                # 파일을 읽어온 뒤 유닛 테스트 실행

            except FileNotFoundError:
                print(f"Error: File '{file_path}' not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
                error_file.append(file_path) 
                # 유닛 테스트에서 fail 발생할 경우 error_file 리스트에 해당 파일 이름 저장
                # fail 발생 x

class TestEnginFunctionality_file(unittest.TestCase):

    def test_engin_functionality_ON_True(self):
        error_file = []
        test_engin_functionality(self, error_file, unit_test_file_list_ON_True, True)

        if error_file : 
            self.fail(msg=error_file) # fail 발생한 파일이 있을 경우 fail 발생

    
    def test_engin_functionality_ON_False(self):
        error_file = []
        test_engin_functionality(self, error_file, unit_test_file_list_ON_False, False)

        if error_file :
            self.fail(msg=error_file) # fail 발생한 파일이 있을 경우 fail 발생
    

    def test_engin_functionality_OFF_True(self):
        error_file = []
        test_engin_functionality(self, error_file, unit_test_file_list_OFF_True, True)

        if error_file : 
            self.fail(msg=error_file) # fail 발생한 파일이 있을 경우 fail 발생
        
    def test_engin_functionality_OFF_False(self):
        error_file = []
        test_engin_functionality(self, error_file, unit_test_file_list_OFF_False, False)

        if error_file :
            self.fail(msg=error_file) # fail 발생한 파일이 있을 경우 fail 발생


class TestEngineFunctionality(unittest.TestCase):

    # TESTCASE 1
    def test_example_new_engin_1(self):
        car_controller = CarController(Car())

        execute_command_callback("ENGINE_BTN BRAKE", car_controller)
        execute_command_callback("UNLOCK", car_controller)
        execute_command_callback("ENGINE_BTN", car_controller)
        execute_command_callback("ENGINE_BTN", car_controller)
        
        self.assertFalse(car_controller.get_engine_status(), "Engine OFF")
    
    # TESTCASE 2
    def test_example_new_engin_2(self):
        car_controller = CarController(Car())

        execute_command_callback("UNLOCK", car_controller)
        execute_command_callback("ENGINE_BTN BRAKE", car_controller)
        execute_command_callback("ACCELERATE", car_controller)
        execute_command_callback("ENGINE_BTN", car_controller)
        execute_command_callback("BRAKE", car_controller)
        execute_command_callback("ENGINE_BTN", car_controller)

        self.assertFalse(car_controller.get_engine_status(), "Engine OFF")

    # TESTCASE 3
    def test_example_new_engin_3(self):
        car_controller = CarController(Car())

        execute_command_callback("UNLOCK", car_controller)
        execute_command_callback("TRUNK_OPEN", car_controller)
        execute_command_callback("LEFT_DOOR_UNLOCK", car_controller)
        execute_command_callback("LEFT_DOOR_OPEN", car_controller)
        execute_command_callback("ENGINE_BTN BRAKE", car_controller)
        execute_command_callback("ENGINE_BTN", car_controller)
        execute_command_callback("LEFT_DOOR_CLOSE", car_controller)
        execute_command_callback("LEFT_DOOR_LOCK", car_controller)
        execute_command_callback("TRUNK_CLOSE", car_controller)
        execute_command_callback("ENGINE_BTN BRAKE", car_controller)
        execute_command_callback("ENGINE_BTN", car_controller)

        self.assertFalse(car_controller.get_engine_status(), "Engine OFF")


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
# 전체잠금, 왼쪽 문 상태, 오른쪽 문 상태, 왼쪽 문 잠금, 오른쪽 문 잠금, 엔진 상태, 트렁크 상태
LOCK_CONDITION = {False, "CLOSED", "CLOSED", "LOCKED", "LOCKED", False,
                  True}
ENGIN_ON_CONDITION = {False, False, "BRAKE"} # 전체 잠금, 엔진 상태, 선행 상태
ENGIN_OFF_CONDITION = {False, True, 0} # 전체 잠금, 엔진 상태, 현재 속도


from collections import deque
def execute_command_callback(command, car_controller):
    # 임찬우
    CONCURRENT_CONDITION = set() # 한 줄, 즉 동시에 발생된 상태를 저장할 집합입니다.
    
    command_que = deque(command.split()) 
    # 공백으로 구분되는 한 줄의 command를 나눠서 저장할 덱입니다.

    while command_que:
        command = command_que.popleft() 
        CONCURRENT_CONDITION.add(command)
        # command_que가 빌 때까지 동시에 동작하므로, command를 CONCURRENT_CONDITION에 저장합니다.
        
        if command == "ENGINE_BTN" :
            # 차량이 전체 잠금 상태가 아니면 엔진을 킬 수 있음
            print("시동 ON/OFF")

            if car_controller.get_lock_status() == False:
                if car_controller.get_engine_status() == False and "BRAKE" in CONCURRENT_CONDITION :
                    car_controller.toggle_engine()
                    print("시동 ON-------------------")

                # 엔진이 켜져 있을 때 속도가 0인지 확인 후 엔진을 끌 수 있는지 판단
                elif car_controller.get_engine_status() == True:
                    if car_controller.get_speed() == 0:
                        car_controller.toggle_engine()  # 시동 OFF 가능

        # 송혜주
        elif command == "ACCELERATE":
            print("가속")
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
            print("감속")
            # 차량이 잠겨있지 않고, 엔진이 켜져있고, 속도가 0 이상일 때 브레이크 페달 가동 가능
            cur_brake_condition = set()

            cur_brake_condition.add(car_controller.get_lock_status())
            cur_brake_condition.add(car_controller.get_engine_status())
            cur_brake_condition.add(car_controller.get_speed() > 0)

            if cur_brake_condition == BRAKE_CONDITION:
                car_controller.brake()  # 속도 -10

        # 주정윤
        elif command == "LOCK":
            print("차량 잠금")
            cur_lock_condition = set()

            cur_lock_condition.add(car_controller.get_lock_status())  # 차량 잠금 상태
            cur_lock_condition.add(car_controller.get_left_door_status())  # 왼쪽 문 상태
            cur_lock_condition.add(
                car_controller.get_right_door_status())  # 오른쪽 문 상태
            cur_lock_condition.add(
                car_controller.get_left_door_lock())  # 왼쪽 문 잠금 상태
            cur_lock_condition.add(
                car_controller.get_right_door_lock())  # 오른쪽 문 잠금 상태
            cur_lock_condition.add(car_controller.get_engine_status())  # 엔진 상태
            cur_lock_condition.add(car_controller.get_trunk_status())  # 트렁크 상태

            if car_controller.get_speed() < 10:
                if cur_lock_condition == LOCK_CONDITION:
                    car_controller.lock_vehicle()

        elif command == "UNLOCK":
            print("차량 잠금해제")
            # 차량의 상태가 'lock'일 때만 차량 잠금해제 가능
            if car_controller.get_lock_status() == True:
                car_controller.unlock_vehicle()  # 차량잠금해제

        # 이재헌
        elif command == "LEFT_DOOR_LOCK":
            print("왼쪽문 잠금")
            # 차량이 잠겨있지 않고, 왼쪽문이 닫혀있을 때만 왼쪽문 잠금
            cur_left_door_lock_condition = set()

            cur_left_door_lock_condition.add(car_controller.get_lock_status())
            cur_left_door_lock_condition.add(car_controller.get_left_door_lock())
            cur_left_door_lock_condition.add(car_controller.get_left_door_status())

            if cur_left_door_lock_condition == DOOR_LOCK_CONDITION:
                car_controller.car.lock_left_door()  # 왼쪽문 잠금

        elif command == "LEFT_DOOR_UNLOCK":
            print("왼쪽문 잠금해제")
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
            print("오른쪽문 잠금")
            # 차량이 잠겨있지 않고, 오른쪽문이 닫혀있을 때만 오른쪽문 잠금
            cur_right_door_lock_condition = set()
            cur_right_door_lock_condition.add(car_controller.get_lock_status())
            cur_right_door_lock_condition.add(car_controller.get_right_door_lock())
            cur_right_door_lock_condition.add(
                car_controller.get_right_door_status())

            if cur_right_door_lock_condition == DOOR_LOCK_CONDITION:
                car_controller.car.lock_right_door()

        elif command == "RIGHT_DOOR_UNLOCK":
            print("오른쪽문 잠금해제")
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
            print("왼쪽문 열기")
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
            print("왼쪽문 닫기")
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
            print("오른쪽문 열기")
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
            print("오른쪽문 닫기")
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
            print("트렁크 열기")
            # car_controller.open_trunk()  # 트렁크 열기
            trunk_open_condition_check(car_controller)
        elif command == "TRUNK_CLOSE":
            print("트렁크 닫기")
            # car_controller.close_trunk()  # 트렁크 닫기
            trunk_close_condition_check(car_controller)

        # SOS 기능 추가
        elif command == "SOS":
            print("SOS 호출")
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
        unittest.main(argv=[sys.argv[0]], exit=False)
        
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