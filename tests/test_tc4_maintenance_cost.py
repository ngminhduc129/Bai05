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
    print("TEST CASE 4: TÍNH CHI PHÍ BẢO TRÌ DỰ KIẾN (TÍNH ĐA HÌNH)")
    print("=" * 70)

    # 1. Máy tính 1: 25 triệu, có GPU rời (+2%), mua năm 2019 (> 5 năm -> +1%), cơ bản 5%
    # Tổng tỷ lệ: 5% + 2% + 1% = 8% => 25.000.000 * 0.08 = 2.000.000 VNĐ
    pc1 = Computer("PC001", "Dell Precision", 2019, 25_000_000.0, 32, "i7", True)
    cost_pc1 = pc1.calculate_annual_maintenance_cost()
    assert abs(cost_pc1 - 2_000_000.0) < 1e-3, f"Chi phí PC1 sai: {cost_pc1} != 2,000,000"
    print(f"-> PC1 (Có GPU rời, > 5 năm): {cost_pc1:,.0f} VNĐ (Kỳ vọng: 2,000,000 VNĐ) [Đúng]")

    # 2. Máy tính 2: 16 triệu, không GPU, mua năm 2023 (<= 5 năm), cơ bản 5%
    # Tổng: 16.000.000 * 0.05 = 800.000 VNĐ
    pc2 = Computer("PC002", "HP ProDesk", 2023, 16_000_000.0, 16, "i5", False)
    cost_pc2 = pc2.calculate_annual_maintenance_cost()
    assert abs(cost_pc2 - 800_000.0) < 1e-3, f"Chi phí PC2 sai: {cost_pc2} != 800,000"
    print(f"-> PC2 (Không GPU, <= 5 năm): {cost_pc2:,.0f} VNĐ (Kỳ vọng: 800,000 VNĐ) [Đúng]")

    # 3. Máy in 1: 14 triệu, cơ bản 4% = 560.000 VNĐ. In 135.000 trang (> 100k -> +500k), Máy in màu (+300k)
    # Tổng: 560.000 + 500.000 + 300.000 = 1.360.000 VNĐ
    pr1 = NetworkPrinter("PR001", "HP Color MFP", 2021, 14_000_000.0, "laser", 135_000, is_color=True)
    cost_pr1 = pr1.calculate_annual_maintenance_cost()
    assert abs(cost_pr1 - 1_360_000.0) < 1e-3, f"Chi phí PR1 sai: {cost_pr1} != 1,360,000"
    print(f"-> PR1 (Máy in màu, > 100k trang): {cost_pr1:,.0f} VNĐ (Kỳ vọng: 1,360,000 VNĐ) [Đúng]")

    # 4. Máy in 2: 4 triệu, cơ bản 4% = 160.000 VNĐ. In 42.000 trang (<= 100k), Trắng đen (không màu)
    # Tổng: 160.000 VNĐ
    pr2 = Printer("PR002", "Canon LBP2900", 2022, 4_000_000.0, "laser", 42_000, is_color=False)
    cost_pr2 = pr2.calculate_annual_maintenance_cost()
    assert abs(cost_pr2 - 160_000.0) < 1e-3, f"Chi phí PR2 sai: {cost_pr2} != 160,000"
    print(f"-> PR2 (Trắng đen, <= 100k trang): {cost_pr2:,.0f} VNĐ (Kỳ vọng: 160,000 VNĐ) [Đúng]")

    # 5. Máy chiếu: 18 triệu, cơ bản 3% = 540.000 VNĐ. Bóng đèn dùng 3.600 giờ (> 3.000h -> +1.500.000 VNĐ)
    # Tổng: 540.000 + 1.500.000 = 2.040.000 VNĐ
    pj1 = Projector("PJ001", "Panasonic VX430", 2020, 18_000_000.0, 4500, lamp_hours_used=3600)
    cost_pj1 = pj1.calculate_annual_maintenance_cost()
    assert abs(cost_pj1 - 2_040_000.0) < 1e-3, f"Chi phí PJ1 sai: {cost_pj1} != 2,040,000"
    print(f"-> PJ1 (Bóng đèn > 3.000 giờ): {cost_pj1:,.0f} VNĐ (Kỳ vọng: 2,040,000 VNĐ) [Đúng]")

    # 6. Kiểm thử tính ĐA HÌNH trong LabRoom
    room = LabRoom("LAB-101", "Phòng Đồ Họa & AI", 40)
    room.add_device(pc1)
    room.add_device(pr1)
    room.add_device(pj1)

    # Tổng kỳ vọng: 2.000.000 + 1.360.000 + 2.040.000 = 5.400.000 VNĐ
    room_total = room.calculate_annual_maintenance_cost()
    expected_room_total = 2_000_000.0 + 1_360_000.0 + 2_040_000.0
    assert abs(room_total - expected_room_total) < 1e-3, f"Tổng chi phí phòng sai: {room_total} != {expected_room_total}"
    print(f"\n=> TỔNG CHI PHÍ PHÒNG LAB-101 (ĐA HÌNH): {room_total:,.0f} VNĐ (Kỳ vọng: {expected_room_total:,.0f} VNĐ) [Đúng]")

    print("\n=> TEST CASE 4: PASSED (Tất cả assertions đều hợp lệ)")
    return True


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
