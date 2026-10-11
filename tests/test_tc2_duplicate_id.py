# /****************/
# 202418872
# Nguyễn Minh Đức
# /****************/

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Computer, LabRoom


def run_test() -> bool:
    print("=" * 70)
    print("TEST CASE 2: THỬ THÊM THIẾT BỊ TRÙNG MÃ (VALIDATION DUPLICATE ID)")
    print("=" * 70)

    room = LabRoom(room_id="LAB-101", room_name="Phòng Đồ Họa & AI", capacity=40)

    # Thiết bị 1
    pc1 = Computer("PC001", "Dell Precision T3640", 2021, 22_000_000.0, 32, "i7-10700K", True)
    room.add_device(pc1)
    print(f"-> Đã thêm thiết bị hợp lệ ban đầu: [{pc1.device_id}] {pc1.device_name}")

    # 1. Thử thêm lại chính đối tượng pc1 vào phòng
    duplicate_same_obj = False
    try:
        room.add_device(pc1)
    except ValueError as ex:
        duplicate_same_obj = True
        print(f"-> Thử thêm lại cùng một đối tượng pc1: Bắt ngoại lệ đúng ({ex})")
    assert duplicate_same_obj, "Thất bại: Cho phép thêm đối tượng trùng vào phòng!"

    # 2. Thử thêm một đối tượng khác nhưng có cùng device_id = 'PC001'
    pc_clone = Computer("PC001", "HP ProDesk Clone", 2023, 14_000_000.0, 16, "i5-10500", False)
    duplicate_diff_obj = False
    try:
        room.add_device(pc_clone)
    except ValueError as ex:
        duplicate_diff_obj = True
        print(f"-> Thử thêm đối tượng khác có trùng mã 'PC001': Bắt ngoại lệ đúng ({ex})")
    assert duplicate_diff_obj, "Thất bại: Cho phép thêm đối tượng có trùng mã vào phòng!"

    # 3. Kiểm thử ràng buộc: Không cho phép khởi tạo thiết bị với mã rỗng
    empty_id_passed = False
    try:
        Computer("   ", "Máy tính mã rỗng", 2022, 10_000_000.0, 8, "i3", False)
    except ValueError as ex:
        empty_id_passed = True
        print(f"-> Kiểm tra khởi tạo thiết bị có mã rỗng: Bắt ngoại lệ đúng ({ex})")
    assert empty_id_passed, "Thất bại: Cho phép tạo thiết bị với mã rỗng!"

    # 4. Kiểm tra mã thiết bị là Read-Only (không thể gán lại sau khi tạo)
    readonly_passed = False
    try:
        pc1.device_id = "PC999"  # type: ignore
    except AttributeError:
        readonly_passed = True
        print("-> Kiểm tra tính bất biến (Read-only) của mã thiết bị: Không cho phép sửa (Thành công)")
    assert readonly_passed, "Thất bại: Thuộc tính device_id bị cho phép sửa đổi!"

    print("\n=> TEST CASE 2: PASSED (Tất cả assertions đều hợp lệ)")
    return True


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
