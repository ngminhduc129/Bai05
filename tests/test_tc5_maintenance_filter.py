# /****************/
# 202418872
# Nguyễn Minh Đức
# /****************/

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Computer, Printer, Projector, LabRoom, DeviceStatus


def run_test() -> bool:
    print("=" * 70)
    print("TEST CASE 5: LỌC THIẾT BỊ CẦN BẢO TRÌ (UNDER_MAINTENANCE HOẶC > 5 NĂM)")
    print("=" * 70)

    room = LabRoom("LAB-101", "Phòng Đồ Họa & AI", 40)

    # 1. PC1: Năm 2019 (Tuổi = 7 năm > 5), Active -> CẦN BẢO TRÌ (do tuổi > 5)
    pc1 = Computer("PC001", "Dell Precision", 2019, 25_000_000.0, 32, "i7", True, status=DeviceStatus.ACTIVE)

    # 2. PC2: Năm 2023 (Tuổi = 3 năm <= 5), UnderMaintenance -> CẦN BẢO TRÌ (do đang sửa chữa)
    pc2 = Computer("PC002", "HP ProDesk", 2023, 16_000_000.0, 16, "i5", False, status=DeviceStatus.UNDER_MAINTENANCE)

    # 3. PR1: Năm 2022 (Tuổi = 4 năm <= 5), Active -> KHÔNG CẦN BẢO TRÌ
    pr1 = Printer("PR001", "Canon 2900", 2022, 4_000_000.0, "laser", 20_000, status=DeviceStatus.ACTIVE)

    # 4. PJ1: Năm 2020 (Tuổi = 6 năm > 5), Active -> CẦN BẢO TRÌ (do tuổi > 5)
    pj1 = Projector("PJ001", "Panasonic", 2020, 18_000_000.0, 4500, 2000, status=DeviceStatus.ACTIVE)

    room.add_device(pc1)
    room.add_device(pc2)
    room.add_device(pr1)
    room.add_device(pj1)

    req_maintenance = room.get_devices_requiring_maintenance()
    req_ids = [d.device_id for d in req_maintenance]

    print(f"Tổng số thiết bị trong phòng: {len(room.devices)}")
    print(f"Số thiết bị cần bảo trì được lọc ra: {len(req_maintenance)}")
    for d in req_maintenance:
        reasons = []
        if d.status == DeviceStatus.UNDER_MAINTENANCE:
            reasons.append("Đang bảo trì")
        if d.age > 5:
            reasons.append(f"Tuổi {d.age} năm > 5")
        print(f"  - [{d.device_id}] {d.device_name} (Lý do: {' & '.join(reasons)})")

    # Kiểm tra assertions
    assert "PC001" in req_ids, "PC001 phải nằm trong danh sách cần bảo trì (tuổi > 5)"
    assert "PC002" in req_ids, "PC002 phải nằm trong danh sách cần bảo trì (UnderMaintenance)"
    assert "PJ001" in req_ids, "PJ001 phải nằm trong danh sách cần bảo trì (tuổi > 5)"
    assert "PR001" not in req_ids, "PR001 KHÔNG được nằm trong danh sách (Active và tuổi <= 5)"
    assert len(req_maintenance) == 3, f"Kỳ vọng đúng 3 thiết bị cần bảo trì, thực tế: {len(req_maintenance)}"

    print("\n=> TEST CASE 5: PASSED (Tất cả assertions đều hợp lệ)")
    return True


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
