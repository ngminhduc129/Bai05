# /****************/
# 202418872
# Nguyễn Minh Đức
# /****************/

import sys
import os
from typing import List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import (
    Device,
    Computer,
    Printer,
    NetworkPrinter,
    Projector,
    INetworkable
)


def run_test() -> bool:
    print("=" * 70)
    print("TEST CASE 7: DUYỆT THIẾT BỊ MẠNG THÔNG QUA INTERFACE INETWORKABLE")
    print("=" * 70)

    # 1. Tạo tập hợp thiết bị hỗn hợp thuộc nhiều lớp khác nhau
    devices: List[Device] = [
        Computer("PC001", "Dell Precision", 2021, 25_000_000.0, 32, "i7", True),
        Printer("PR001", "Canon LBP2900 (USB)", 2022, 4_000_000.0, "laser", 30_000),      # Không có mạng
        NetworkPrinter("PR002", "HP Color MFP (Network)", 2023, 14_000_000.0, "laser", 80_000, True),  # Có mạng
        Projector("PJ001", "Panasonic VX430", 2020, 18_000_000.0, 4500, 2000),             # Không có mạng
        Computer("PC002", "HP ProDesk", 2023, 16_000_000.0, 16, "i5", False)             # Có mạng
    ]

    print(f"Tổng số thiết bị trong danh sách: {len(devices)}")

    # 2. Lọc các thiết bị có năng lực mạng (thực thi INetworkable)
    networkable_list: List[INetworkable] = [
        d for d in devices if isinstance(d, INetworkable)
    ]

    # Kỳ vọng: Có đúng 3 thiết bị hỗ trợ mạng (PC001, PR002, PC002)
    assert len(networkable_list) == 3, f"Kỳ vọng 3 thiết bị mạng, thực tế tìm thấy: {len(networkable_list)}"
    print(f"Số thiết bị có năng lực kết nối mạng tìm thấy: {len(networkable_list)} (Đúng)")

    # 3. Duyệt và cấp phát mạng thông qua giao thức INetworkable
    ip_subnet = "192.168.1."
    for idx, net_device in enumerate(networkable_list, 101):
        assigned_ip = f"{ip_subnet}{idx}"
        # Gọi phương thức connect thông qua interface INetworkable
        net_device.connect(assigned_ip)
        assert net_device.is_connected is True, "Thiết bị phải ở trạng thái kết nối"
        assert net_device.ip_address == assigned_ip, f"IP phải là {assigned_ip}"
        
        # Lấy thông tin đối tượng mà không phụ thuộc vào việc nó là Computer hay NetworkPrinter
        dev_obj = net_device  # Tham chiếu kiểu INetworkable
        name = getattr(dev_obj, "device_name", "Thiết bị mạng")
        print(f"  [INetworkable] Cấp IP {net_device.ip_address} thành công cho '{name}' (is_connected={net_device.is_connected})")

    # 4. Kiểm tra các thiết bị không có mạng thì không thực thi INetworkable
    usb_printer = devices[1]
    projector = devices[3]
    assert not isinstance(usb_printer, INetworkable), "Printer thông thường không được thực thi INetworkable"
    assert not isinstance(projector, INetworkable), "Projector không được thực thi INetworkable"
    print("-> Xác nhận Printer USB và Projector hoàn toàn độc lập với interface mạng (ISP chuẩn) [Đúng]")

    # 5. Ngắt kết nối toàn bộ thiết bị mạng
    for net_device in networkable_list:
        net_device.disconnect()
        assert net_device.is_connected is False, "Sau khi ngắt, is_connected phải là False"
        assert net_device.ip_address is None, "Sau khi ngắt, ip_address phải là None"
    print("-> Đã ngắt kết nối và giải phóng IP toàn bộ thiết bị mạng thành công.")

    print("\n=> TEST CASE 7: PASSED (Tất cả assertions đều hợp lệ)")
    return True


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
