import unittest

from car import Car
from car_controller import CarController
from main import execute_command_callback


class TestSOSFunctionality(unittest.TestCase):
    def test_sos_functionality(self):
        car_controller = CarController(Car())

        # SOS 신호 보내기
        execute_command_callback("SOS", car_controller)

        # 테스트 assertions
        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_left_door_status(), "OPEN")
        self.assertEqual(car_controller.get_right_door_status(), "OPEN")
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

    def test_unlock_door_functionality(self):
        car_controller = CarController(Car())

        execute_command_callback("UNLOCK", car_controller)

        execute_command_callback("LEFT_DOOR_UNLOCK", car_controller)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")

        execute_command_callback("RIGHT_DOOR_UNLOCK", car_controller)
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")

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

    def test_lock_doors_when_doors_are_closed(self):
        car_controller = CarController(Car())
        # 문이 닫혀있을 때만 잠금 가능
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


class TrunkControllerTests(unittest.TestCase):

    #########################################################################
    # 정상 케이스
    def test_trunk_open_normal(self):
        car_controller = CarController(Car())

        execute_command_callback("UNLOCK", car_controller)
        execute_command_callback("TRUNK_OPEN", car_controller)

        self.assertEqual(car_controller.get_trunk_status(), False)

    def test_trunk_close_normal(self):
        car_controller = CarController(Car())

        execute_command_callback("UNLOCK", car_controller)
        execute_command_callback("TRUNK_OPEN", car_controller)
        execute_command_callback("TRUNK_CLOSE", car_controller)

        self.assertEqual(car_controller.get_trunk_status(), True)

    ##########################################################################
    # 비정상 케이스

    # 이미 열리거나 닫힘
    def test_trunk_open_already(self):
        car_controller = CarController(Car())

        execute_command_callback("UNLOCK", car_controller)
        execute_command_callback("TRUNK_OPEN", car_controller)
        execute_command_callback("TRUNK_OPEN", car_controller)

        self.assertEqual(car_controller.get_trunk_status(), False)

    def test_trunk_close_already(self):
        car_controller = CarController(Car())

        execute_command_callback("UNLOCK", car_controller)
        execute_command_callback("TRUNK_OPEN", car_controller)
        execute_command_callback("TRUNK_CLOSE", car_controller)
        execute_command_callback("TRUNK_CLOSE", car_controller)

        self.assertEqual(car_controller.get_trunk_status(), True)

    # 속도 0이 아님
    def test_trunk_speed_nonzero(self):
        car_controller = CarController(Car())

        execute_command_callback("UNLOCK", car_controller)
        execute_command_callback("ENGINE_BTN", car_controller)
        execute_command_callback("ACCELERATE", car_controller)
        execute_command_callback("ACCELERATE", car_controller)
        execute_command_callback("TRUNK_OPEN", car_controller)

        self.assertEqual(car_controller.get_trunk_status(), True)

    # 전체 잠금 상태
    def test_trunk_car_locked(self):
        car_controller = CarController(Car())

        execute_command_callback("TRUNK_OPEN", car_controller)

        self.assertEqual(car_controller.get_trunk_status(), True)


if __name__ == '__main__':
    unittest.main()
