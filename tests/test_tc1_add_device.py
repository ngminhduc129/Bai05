# /****************/
# 202418872
# Nguyễn Minh Đức
# /****************/

import sys
import os

# Cho phép chạy file trực tiếp từ thư mục tests/ hoặc thư mục gốc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Computer, Printer, NetworkPrinter, Projector, LabRoom, DeviceStatus


def run_test() -> bool:
    print("=" * 70)
    print("TEST CASE 1: THÊM THIẾT BỊ VÀO PHÒNG THỰC HÀNH & VALIDATION")
    print("=" * 70)

    # 1. Khởi tạo phòng
    room = LabRoom(room_id="LAB-101", room_name="Phòng Đồ Họa & AI", capacity=40)
    assert len(room.devices) == 0, "Ban đầu phòng phải trống!"

    # 2. Khởi tạo các thiết bị hợp lệ
    pc = Computer("PC001", "Dell Precision", 2021, 20_000_000.0, 32, "i7-11700", True)
    printer = Printer("PR001", "Canon LBP2900", 2022, 4_000_000.0, "laser", 20_000)
    net_printer = NetworkPrinter("PR002", "HP Color MFP", 2023, 15_000_000.0, "laser", 50_000, True)
    projector = Projector("PJ001", "Panasonic VX430", 2020, 18_000_000.0, 4500, 2500)

    # 3. Thêm các thiết bị vào phòng
    room.add_device(pc)
    room.add_device(printer)
    room.add_device(net_printer)
    room.add_device(projector)

    assert len(room.devices) == 4, f"Kỳ vọng 4 thiết bị, thực tế: {len(room.devices)}"
    print(f"-> Đã thêm thành công 4 thiết bị vào '{room.room_name}'.")

    # 4. Kiểm tra tìm kiếm thiết bị đã thêm
    found = room.find_device("PC001")
    assert found is not None and found.device_id == "PC001", "Không tìm thấy PC001!"
    print(f"-> Tìm kiếm thiết bị theo mã 'PC001': {found.device_name} (Thành công)")

    # 5. Kiểm thử ràng buộc: Không chấp nhận đối tượng None
    none_passed = False
    try:
        room.add_device(None)  # type: ignore
    except TypeError as ex:
        none_passed = True
        print(f"-> Kiểm tra thêm None: Bắt ngoại lệ đúng (Expected: {ex})")
    assert none_passed, "Lỗi: Không bắt được ngoại lệ khi thêm đối tượng None!"

    # 6. Kiểm thử ràng buộc: Không chấp nhận đối tượng không phải Device
    invalid_type_passed = False
    try:
        room.add_device("Đây là một chuỗi")  # type: ignore
    except TypeError as ex:
        invalid_type_passed = True
        print(f"-> Kiểm tra thêm sai kiểu: Bắt ngoại lệ đúng (Expected: {ex})")
    assert invalid_type_passed, "Lỗi: Không bắt được ngoại lệ khi thêm sai kiểu đối tượng!"

    print("\n=> TEST CASE 1: PASSED (Tất cả assertions đều hợp lệ)")
    return True


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
