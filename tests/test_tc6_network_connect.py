# /****************/
# 202418872
# Nguyễn Minh Đức
# /****************/

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Computer, NetworkPrinter, INetworkable


def run_test() -> bool:
    print("=" * 70)
    print("TEST CASE 6: QUY TẮC KẾT NỐI VÀ NGẮT KẾT NỐI MẠNG (INETWORKABLE)")
    print("=" * 70)

    # 1. Khởi tạo đối tượng thực thi INetworkable
    comp = Computer("PC001", "Dell OptiPlex", 2022, 15_000_000.0, 16, "i5", False)
    net_pr = NetworkPrinter("PR001", "HP Color MFP", 2023, 12_000_000.0, "laser", 30_000, True)

    assert isinstance(comp, INetworkable), "Computer phải là instance của INetworkable"
    assert isinstance(net_pr, INetworkable), "NetworkPrinter phải là instance của INetworkable"

    # Trạng thái ban đầu
    assert comp.is_connected is False, "Ban đầu Computer phải chưa kết nối (False)"
    assert comp.ip_address is None, "Ban đầu IP của Computer phải là None"
    print("-> Trạng thái ban đầu: is_connected = False, ip_address = None [Đúng]")

    # 2. Kết nối hợp lệ
    comp.connect("192.168.1.50")
    assert comp.is_connected is True, "Sau connect, is_connected phải là True"
    assert comp.ip_address == "192.168.1.50", "IP lưu trữ phải đúng với IP đã gán"
    print(f"-> Kết nối thành công Computer với IP: {comp.ip_address} (is_connected = {comp.is_connected}) [Đúng]")

    # 3. Thử kết nối lại khi đang online -> Bắt RuntimeError
    reconnect_failed = False
    try:
        comp.connect("192.168.1.99")
    except RuntimeError as ex:
        reconnect_failed = True
        print(f"-> Thử kết nối lại khi đang online: Bắt ngoại lệ đúng ({ex})")
    assert reconnect_failed, "Thất bại: Cho phép kết nối lại khi thiết bị đang kết nối!"

    # 4. Thử kết nối với IP rỗng -> Bắt ValueError
    net_pr_empty_ip = False
    try:
        net_pr.connect("   ")
    except ValueError as ex:
        net_pr_empty_ip = True
        print(f"-> Thử kết nối với IP rỗng: Bắt ngoại lệ đúng ({ex})")
    assert net_pr_empty_ip, "Thất bại: Cho phép kết nối với địa chỉ IP rỗng!"

    # 5. Ngắt kết nối (disconnect)
    comp.disconnect()
    assert comp.is_connected is False, "Sau disconnect(), is_connected phải trả về False"
    assert comp.ip_address is None, "Sau disconnect(), ip_address phải là None (không còn lưu vết)"
    print("-> Ngắt kết nối: is_connected = False, ip_address = None [Đúng]")

    # 6. Cho phép kết nối lại sau khi đã disconnect
    comp.connect("192.168.1.100")
    assert comp.is_connected is True and comp.ip_address == "192.168.1.100", "Phải cho phép kết nối lại sau khi đã ngắt"
    print(f"-> Kết nối lại sau khi ngắt: Thành công với IP mới {comp.ip_address} [Đúng]")

    print("\n=> TEST CASE 6: PASSED (Tất cả assertions đều hợp lệ)")
    return True


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
