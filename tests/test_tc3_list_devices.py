# /****************/
# 202418872
# Nguyễn Minh Đức
# /****************/

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Computer, Printer, NetworkPrinter, Projector, LabRoom


def run_test() -> bool:
    print("=" * 70)
    print("TEST CASE 3: IN DANH SÁCH THIẾT BỊ TỪNG PHÒNG & TÍNH ĐÓNG GÓI")
    print("=" * 70)

    room = LabRoom("LAB-201", "Phòng Thực Hành Mạng", 35)

    pc = Computer("PC101", "Dell OptiPlex", 2022, 18_000_000.0, 16, "Core i5", False)
    pr = NetworkPrinter("PR101", "HP LaserJet Pro", 2021, 12_000_000.0, "laser", 80_000, True)
    pj = Projector("PJ101", "Sony VPL", 2020, 20_000_000.0, 4000, 2800)

    room.add_device(pc)
    room.add_device(pr)
    room.add_device(pj)

    # 1. Kiểm tra in danh sách thông tin thiết bị (Ghi đè __str__ đa hình)
    print(f"\nDanh sách thiết bị trong {room}:")
    for idx, d in enumerate(room.devices, 1):
        info = str(d)
        print(f"  {idx}. {info}")
        assert d.device_id in info, f"Chuỗi __str__ phải chứa mã thiết bị {d.device_id}"
        assert d.__class__.__name__ in info, f"Chuỗi __str__ phải chứa tên lớp {d.__class__.__name__}"

    # 2. Kiểm tra tính đóng gói (Encapsulation): Danh sách trả về phải là bản sao
    dev_list = room.devices
    dev_list.clear()  # Xóa list bên ngoài
    assert len(room.devices) == 3, "Lỗi đóng gói: Can thiệp list trả về đã làm mất dữ liệu bên trong LabRoom!"
    print("\n-> Kiểm tra tính đóng gói: Thuộc tính devices trả về bản sao an toàn (Thành công)")

    # 3. Kiểm tra thao tác xóa thiết bị (remove_device)
    removed = room.remove_device("PC101")
    assert removed is True, "Xóa PC101 phải trả về True"
    assert len(room.devices) == 2, "Sau khi xóa số thiết bị phải còn 2"
    assert room.find_device("PC101") is None, "Không được tìm thấy PC101 sau khi xóa"
    print(f"-> Thao tác xóa thiết bị 'PC101': Thành công (Số thiết bị còn lại: {len(room.devices)})")

    # Xóa thiết bị không tồn tại
    assert room.remove_device("KHONG_TON_TAI") is False, "Xóa thiết bị không có phải trả về False"

    print("\n=> TEST CASE 3: PASSED (Tất cả assertions đều hợp lệ)")
    return True


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
