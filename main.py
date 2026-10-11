# /****************/
# 202418872
# Nguyễn Minh Đức
# /****************/

"""
Chương trình chính (Test Runner) điều phối thực thi bộ 7 Test Cases độc lập
cho Hệ thống Quản lý Thiết bị và Hợp đồng Bảo trì (Lab W05 - OOP).

Sinh viên: Nguyễn Minh Đức - MSSV: 202418872
"""

import sys
import time

# Re-export các lớp miền nghiệp vụ từ models để đảm bảo tính tương thích
from models import (
    DeviceStatus,
    Device,
    INetworkable,
    Computer,
    Printer,
    NetworkPrinter,
    Projector,
    LabRoom
)

# Import 7 test cases độc lập từ package tests
from tests.test_tc1_add_device import run_test as test_tc1
from tests.test_tc2_duplicate_id import run_test as test_tc2
from tests.test_tc3_list_devices import run_test as test_tc3
from tests.test_tc4_maintenance_cost import run_test as test_tc4
from tests.test_tc5_maintenance_filter import run_test as test_tc5
from tests.test_tc6_network_connect import run_test as test_tc6
from tests.test_tc7_network_iteration import run_test as test_tc7


def main() -> None:
    print("=" * 80)
    print(" HỆ THỐNG QUẢN LÝ THIẾT BỊ VÀ HỢP ĐỒNG BẢO TRÌ PHÒNG THỰC HÀNH")
    print(" MASTER TEST RUNNER - ĐIỀU PHỐI BỘ 7 TEST CASES ĐỘC LẬP")
    print(" Sinh viên thực hiện: Nguyễn Minh Đức - MSSV: 202418872")
    print("=" * 80)
    print()

    test_suite = [
        ("TC-01", "Thêm thiết bị vào phòng & Kiểm tra ràng buộc kiểu dữ liệu", test_tc1),
        ("TC-02", "Thử thêm thiết bị trùng mã (Validation Duplicate ID) & Read-only", test_tc2),
        ("TC-03", "In danh sách thiết bị từng phòng & Tính đóng gói danh sách", test_tc3),
        ("TC-04", "Tính tổng chi phí bảo trì dự kiến các lớp & Tính Đa hình", test_tc4),
        ("TC-05", "Lọc thiết bị cần bảo trì (UnderMaintenance HOẶC > 5 năm)", test_tc5),
        ("TC-06", "Kiểm thử quy tắc kết nối / ngắt kết nối mạng trên INetworkable", test_tc6),
        ("TC-07", "Duyệt thiết bị mạng qua interface INetworkable độc lập lớp cụ thể", test_tc7),
    ]

    results = []
    total_start = time.time()

    for code, name, test_func in test_suite:
        print("\n" + "#" * 80)
        print(f" ĐANG THỰC THI: [{code}] - {name}")
        print("#" * 80)
        t_start = time.time()
        try:
            status = test_func()
            duration = (time.time() - t_start) * 1000
            results.append((code, name, "PASSED", duration))
        except Exception as ex:
            duration = (time.time() - t_start) * 1000
            print(f" LỖI THỰC THI [{code}]: {ex}")
            results.append((code, name, "FAILED", duration))

    total_duration = (time.time() - total_start) * 1000

    # In bảng tổng kết kết quả kiểm thử (Summary Table)
    print("\n" + "=" * 80)
    print(" TỔNG KẾT KẾT QUẢ KIỂM THỬ BỘ 7 TEST CASES")
    print("=" * 80)
    print(f"| {'Mã TC':<7} | {'Tên Test Case':<52} | {'Trạng thái':<10} |")
    print("|" + "-" * 9 + "|" + "-" * 54 + "|" + "-" * 12 + "|")
    
    passed_count = 0
    for code, name, status, _ in results:
        status_str = f"[{status}]"
        if status == "PASSED":
            passed_count += 1
        print(f"| {code:<7} | {name:<52} | {status_str:<10} |")

    print("=" * 80)
    print(f"KẾT QUẢ: {passed_count}/{len(test_suite)} Test Cases PASSED ({total_duration:.1f}ms)")
    if passed_count == len(test_suite):
        print(" TẤT CẢ CÁC TEST CASES ĐÃ VƯỢT QUA KIỂM THỬ THÀNH CÔNG 100%!")
    else:
        print(" CÓ TEST CASE THẤT BẠI. VUI LÒNG KIỂM TRA LẠI MÃ NGUỒN!")
    print("=" * 80)

    # Thoát với mã lỗi 0 nếu toàn bộ pass
    sys.exit(0 if passed_count == len(test_suite) else 1)


if __name__ == "__main__":
    main()
