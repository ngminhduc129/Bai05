# /****************/
# 202418872
# Nguyễn Minh Đức
# /****************/

import os
import subprocess
from datetime import datetime

MD_CONTENT = """# BÁO CÁO THỰC HÀNH TUẦN 05 (LAB W05)
## CHỦ ĐỀ: HỆ THỐNG QUẢN LÝ THIẾT BỊ VÀ HỢP ĐỒNG BẢO TRÌ

---

### THÔNG TIN CHUNG
- **Mã sinh viên:** 202418872
- **Họ và tên:** Nguyễn Minh Đức
- **Môn học:** Lập trình hướng đối tượng (OOP)
- **Học kỳ:** 2026.1
- **Kho lưu trữ GitHub (Mã nguồn):** [https://github.com/ngminhduc129/OOP-Bai05-DeviceManagement](https://github.com/ngminhduc129/OOP-Bai05-DeviceManagement)
- **Tệp mã nguồn chính:** `main.py`

---

## 1. PHÂN TÍCH YÊU CẦU NGHIỆP VỤ

### 1.1. Bối cảnh bài toán
Một trường đại học cần xây dựng hệ thống quản lý trang thiết bị phục vụ các phòng thực hành tin học. Hệ thống giải quyết các bài toán nghiệp vụ sau:
1. **Quản lý danh mục thiết bị:** Theo dõi các thông tin định danh, cấu hình và trạng thái hoạt động của từng loại thiết bị.
2. **Dự toán chi phí bảo trì hàng năm:** Mỗi loại thiết bị có đặc thù vận hành và linh kiện hao mòn khác nhau, dẫn tới công thức tính chi phí bảo trì dự kiến khác nhau.
3. **Quản lý kết nối mạng linh hoạt:** Một số thiết bị có năng lực kết nối mạng (máy tính luôn có mạng, một số máy in hỗ trợ mạng, máy chiếu không có mạng). Hệ thống cần quản lý trạng thái online/offline, cấp phát IP mà không làm phức tạp hóa cây kế thừa chung.
4. **Quản lý phòng thực hành (LabRoom):** Phân bổ thiết bị vào các phòng, kiểm tra trùng lặp mã thiết bị, tổng hợp chi phí bảo trì phòng và lọc các thiết bị cần đưa đi bảo dưỡng.

### 1.2. Quy tắc nghiệp vụ chi tiết

#### A. Thiết bị chung (Device)
- **Mã thiết bị (`device_id`):** Định danh duy nhất, không được để trống, chỉ được thiết lập 1 lần khi khởi tạo (read-only).
- **Giá mua (`purchase_price`):** Phải là số dương (> 0).
- **Năm đưa vào sử dụng (`year_of_usage`):** Không được lớn hơn năm hiện tại.
- **Trạng thái hoạt động (`DeviceStatus`):** `Active` (đang hoạt động), `UnderMaintenance` (đang bảo trì), `Retired` (đã thanh lý).

#### B. Các loại thiết bị chuyên biệt
1. **Máy tính (Computer):**
   - Bổ sung thông tin: Dung lượng RAM (GB), loại vi xử lý (CPU), có GPU rời hay không.
   - Năng lực: Luôn có khả năng kết nối mạng (`INetworkable`).
   - Công thức chi phí bảo trì:
     $$\\text{Chi phí} = \\text{Giá mua} \\times 5\\% + (\\text{Giá mua} \\times 2\\% \\text{ nếu có GPU rời}) + (\\text{Giá mua} \\times 1\\% \\text{ nếu tuổi thọ } > 5 \\text{ năm})$$

2. **Máy in (Printer / NetworkPrinter):**
   - Bổ sung thông tin: Loại máy in (`laser` hoặc `phun`), số trang đã in (`pages_printed`), có hỗ trợ cổng mạng (`has_network_support`), chế độ in màu (`is_color`).
   - *Lý do bổ sung thuộc tính `is_color`:* Đề bài yêu cầu cộng thêm 300.000 VNĐ nếu là máy in màu. Trong thực tế, máy in màu sử dụng 4 hộp mực (CMYK) và cụm sấy/đầu phun phức tạp hơn máy in đơn sắc, do đó chi phí bảo dưỡng định kỳ cao hơn rõ rệt.
   - Công thức chi phí bảo trì:
     $$\\text{Chi phí} = (\\text{Giá mua} \\times 4\\%) + (500.000 \\text{ VNĐ nếu } \\text{pages\\_printed} > 100.000) + (300.000 \\text{ VNĐ nếu là máy in màu})$$
   - Mô hình hóa mạng: Tách riêng lớp `NetworkPrinter` kế thừa từ `Printer` và thực thi interface `INetworkable`.

3. **Máy chiếu (Projector):**
   - Bổ sung thông tin: Độ sáng (`brightness_lumens`), số giờ đã sử dụng bóng đèn (`lamp_hours_used`).
   - Phiên bản hiện tại không có yêu cầu kết nối mạng.
   - Công thức chi phí bảo trì:
     $$\\text{Chi phí} = (\\text{Giá mua} \\times 3\\%) + (1.500.000 \\text{ VNĐ nếu } \\text{lamp\\_hours\\_used} > 3.000 \\text{ giờ})$$

#### C. Năng lực kết nối mạng (INetworkable)
- Địa chỉ IP không được rỗng hoặc chứa khoảng trắng.
- Khi đang kết nối (`is_connected = True`), không được phép kết nối lại (ném ngoại lệ).
- Sau khi ngắt kết nối (`disconnect()`), `is_connected` trả về `False` và `ip_address` trả về `None`.

#### D. Phòng thực hành (LabRoom)
- Quan hệ với `Device`: **Kết tập (Aggregation)**.
- Ràng buộc:
  - Không thêm 2 thiết bị có cùng mã vào cùng một phòng.
  - Không chấp nhận đối tượng thiết bị `None`.
  - Tính tổng chi phí bảo trì phòng phải sử dụng tính **Đa hình** (duyệt danh sách và gọi phương thức ảo, không dùng `if/isinstance`).
  - Lọc thiết bị cần bảo dưỡng: Thiết bị đang ở trạng thái `UnderMaintenance` HOẶC có thời gian sử dụng trên 5 năm.

---

## 2. DANH SÁCH LỚP VÀ SƠ ĐỒ QUAN HỆ

### 2.1. Danh sách các thực thể trong hệ thống

| Tên lớp / Interface | Loại | Mô tả trách nhiệm |
|---|---|---|
| `DeviceStatus` | Enum | Định nghĩa 3 trạng thái của thiết bị: `ACTIVE`, `UNDER_MAINTENANCE`, `RETIRED`. |
| `Device` | Abstract Class | Lớp cơ sở trừu tượng chứa các thuộc tính chung (`device_id`, `device_name`, `year_of_usage`, `purchase_price`, `status`) và phương thức trừu tượng `calculate_annual_maintenance_cost()`. |
| `INetworkable` | Interface (ABC) | Định nghĩa giao thức kết nối mạng (`connect`, `disconnect`, `ip_address`, `is_connected`). |
| `Computer` | Concrete Class | Kế thừa `Device` và thực thi `INetworkable`. Đại diện cho máy tính để bàn/trạm. |
| `Printer` | Concrete Class | Kế thừa `Device`. Đại diện cho máy in thông thường (cổng USB). |
| `NetworkPrinter` | Concrete Class | Kế thừa `Printer` và thực thi `INetworkable`. Đại diện cho máy in mạng văn phòng. |
| `Projector` | Concrete Class | Kế thừa `Device`. Đại diện cho máy chiếu phòng học. |
| `LabRoom` | Container Class | Biểu diễn phòng thực hành, kết tập danh sách `Device`, quản lý thêm/xóa/tìm kiếm, tính tổng chi phí và lọc bảo trì. |

### 2.2. Sơ đồ quan hệ lớp (Class Diagram)

```mermaid
classDiagram
    class DeviceStatus {
        <<enumeration>>
        ACTIVE
        UNDER_MAINTENANCE
        RETIRED
    }

    class INetworkable {
        <<interface>>
        +ip_address: Optional[str]
        +is_connected: bool
        +connect(ip_address: str) void
        +disconnect() void
    }

    class Device {
        <<abstract>>
        -_device_id: str
        -_device_name: str
        -_year_of_usage: int
        -_purchase_price: float
        -_status: DeviceStatus
        +device_id: str
        +device_name: str
        +year_of_usage: int
        +purchase_price: float
        +status: DeviceStatus
        +age: int
        +calculate_annual_maintenance_cost()* float
        +__str__() str
    }

    class Computer {
        +ram_size_gb: int
        +processor_type: str
        +has_discrete_gpu: bool
        -_ip_address: Optional[str]
        -_is_connected: bool
        +calculate_annual_maintenance_cost() float
        +connect(ip_address: str) void
        +disconnect() void
    }

    class Printer {
        +printer_type: str
        +pages_printed: int
        +has_network_support: bool
        +is_color: bool
        +calculate_annual_maintenance_cost() float
    }

    class NetworkPrinter {
        -_ip_address: Optional[str]
        -_is_connected: bool
        +connect(ip_address: str) void
        +disconnect() void
    }

    class Projector {
        +brightness_lumens: int
        +lamp_hours_used: int
        +calculate_annual_maintenance_cost() float
    }

    class LabRoom {
        +room_id: str
        +room_name: str
        +capacity: int
        -_devices: List[Device]
        +devices: List[Device]
        +add_device(device: Device) void
        +remove_device(device_id: str) bool
        +find_device(device_id: str) Optional[Device]
        +calculate_annual_maintenance_cost() float
        +get_devices_requiring_maintenance() List[Device]
    }

    Device <|-- Computer : Kế thừa (Inheritance)
    Device <|-- Printer : Kế thừa (Inheritance)
    Device <|-- Projector : Kế thừa (Inheritance)
    Printer <|-- NetworkPrinter : Kế thừa (Inheritance)

    INetworkable <|.. Computer : Cài đặt (Realization)
    INetworkable <|.. NetworkPrinter : Cài đặt (Realization)

    Device --> DeviceStatus : Sử dụng (Association)
    LabRoom o-- Device : Kết tập (Aggregation)
```

---

## 3. TRẢ LỜI CÁC CÂU HỎI THIẾT KẾ & LÝ THUYẾT

### 3.1. Vì sao `Device` là lớp trừu tượng?
1. **Bản chất nghiệp vụ:** Trong thực tế, không có một thực thể vật lý nào chỉ mang tên "thiết bị chung chung". Mọi thiết bị được mua về đều là một đối tượng cụ thể (máy tính Dell, máy in HP, máy chiếu Panasonic,...). Do đó, việc khởi tạo một instance `Device()` trực tiếp là không có ý nghĩa thực tế. Khai báo `Device` là lớp trừu tượng (Abstract Class) nhằm ngăn chặn việc tạo đối tượng vô nghĩa này.
2. **Bản chất kỹ thuật (Polymorphic Foundation):** Mỗi loại thiết bị có công thức tính chi phí bảo trì hoàn toàn khác nhau (máy tính theo GPU và tuổi đời; máy in theo số trang và chế độ in màu; máy chiếu theo tuổi thọ bóng đèn). Ở lớp cha `Device`, không thể cài đặt một công thức tính chung. Việc đặt `calculate_annual_maintenance_cost()` là phương thức thuần ảo (`@abstractmethod`) vừa chuẩn hóa giao diện lập trình bắt buộc các lớp con phải triển khai, vừa tạo nền tảng cho cơ chế đa hình khi gọi từ `LabRoom`.

### 3.2. Vì sao `INetworkable` là interface?
1. **Phân tách khả năng (Capability) khỏi bản chất thực thể (Identity):** Bản chất của một máy tính hay máy in là "thiết bị" (`is-a Device`). Tuy nhiên, "khả năng kết nối mạng" không phải là một loại thiết bị, mà là một **năng lực hành vi** (capability / behavior). 
2. **Tuân thủ nguyên lý phân tách giao diện (ISP - Interface Segregation Principle):** Nếu đưa các thuộc tính mạng (`ip_address`, `connect()`, `disconnect()`) vào lớp cha `Device`, các thiết bị không có mạng như `Projector` hoặc máy in đời cũ sẽ bị ép phải kế thừa các phương thức không dùng tới (gây mã thừa hoặc ném `NotImplementedError`).
3. **Tính tái sử dụng đa hình độc lập cây kế thừa:** Interface cho phép các lớp thuộc các nhánh kế thừa hoàn toàn khác nhau (ví dụ: `Computer`, `NetworkPrinter`, hoặc trong tương lai là `SmartAirConditioner`, `SecurityCamera`) cùng chia sẻ một giao thức mạng chuẩn hóa. Chương trình quản lý mạng chỉ cần làm việc với kiểu `INetworkable` mà không cần quan tâm thiết bị đó là gì.

### 3.3. Tính đa hình được thể hiện ở đâu trong hệ thống?
Tính đa hình (Polymorphism) được thể hiện tại 3 điểm trọng yếu:
1. **Đa hình trong tính chi phí bảo trì (`LabRoom.calculate_annual_maintenance_cost`):**
   - Vòng lặp tính toán:
     ```python
     for device in self._devices:
         total_cost += device.calculate_annual_maintenance_cost()
     ```
   - Tại thời điểm biên dịch / viết code, `device` chỉ được biết đến dưới dạng tham chiếu của lớp cơ sở trừu tượng `Device`. Nhưng tại thời điểm thực thi (Runtime Dynamic Dispatch), Python tự động gọi chính xác phương thức tính chi phí tương ứng của `Computer`, `Printer`, hoặc `Projector`. Mã nguồn hoàn toàn không cần bất kỳ câu lệnh `if-elif` hay kiểm tra kiểu nào, tuân thủ hoàn hảo nguyên lý Mở/Đóng (OCP).
2. **Đa hình thông qua Interface (`INetworkable`):**
   - Trong thao tác quản trị mạng, hệ thống lọc danh sách các thiết bị hỗ trợ mạng:
     ```python
     for net_dev in networkable_devices:
         net_dev.connect(ip)
     ```
   - `net_dev` có thể là một chiếc máy tính (`Computer`) hoặc một chiếc máy in mạng (`NetworkPrinter`). Chúng có cơ chế lưu trữ và cấu hình khác nhau, nhưng đều phản hồi cùng một thông điệp `connect()` và `disconnect()`.
3. **Đa hình thông qua ghi đè chuỗi hiển thị (`__str__`):**
   - Khi in thông tin thiết bị (`print(device)`), hàm `__str__` của từng lớp con được kích hoạt linh hoạt để bổ sung các thông số đặc thù (RAM, CPU, bóng đèn, số trang) vào chuỗi thông tin chung của lớp cha.

### 3.4. Quan hệ giữa `LabRoom` và `Device` là kết tập hay hợp thành?
- **Kết luận:** Mối quan hệ giữa `LabRoom` và `Device` là quan hệ **KẾT TẬP (Aggregation)**, KHÔNG PHẢI là hợp thành (Composition).
- **Giải thích dựa trên vòng đời:**
  - Trong quan hệ **Hợp thành (Composition)**, đối tượng thành phần (Part) phụ thuộc sinh tử vào đối tượng toàn thể (Whole). Nếu Whole bị hủy, Part cũng bị tiêu hủy theo.
  - Trong nghiệp vụ quản lý thiết bị trường đại học:
    + Một thiết bị có thể được mua về và nhập kho lưu trữ trước khi phân bổ vào bất kỳ phòng thực hành nào.
    + Một thiết bị có thể được chuyển từ phòng thực hành này (`LAB-101`) sang phòng khác (`LAB-102`).
    + Nếu một phòng thực hành bị giải thể, đổi mục đích sử dụng hoặc xóa khỏi phần mềm, các thiết bị bên trong không hề bị phá hủy hay xóa bỏ, mà tiếp tục tồn tại để tái phân bổ hoặc thanh lý.
    + Do đó, vòng đời của `Device` hoàn toàn độc lập với vòng đời của `LabRoom`.

### 3.5. Phân tích Trade-off: Lựa chọn mô hình cho máy in có mạng
- **Phương án đã chọn:** Tách lớp `NetworkPrinter` kế thừa từ `Printer` và thực thi interface `INetworkable`.
- **Đoạn phân tích trade-off (4 câu):**
  1. Việc tạo lớp `NetworkPrinter` kế thừa từ `Printer` và implement `INetworkable` phân định rành mạch giữa dòng máy in phổ thông kết nối qua USB và dòng máy in công nghiệp có card mạng riêng biệt, tuân thủ nguyên lý Đơn trách nhiệm (SRP) và Phân tách giao diện (ISP).
  2. Cách tiếp cận này loại bỏ hoàn toàn nguy cơ máy in thường bị ép phải chứa các thuộc tính mạng rỗng hoặc ném ngoại lệ khi gọi phương thức không hỗ trợ.
  3. Tuy nhiên, đánh đổi (trade-off) là hệ thống có thêm một lớp mới trong cây kế thừa; nếu một máy in thường được người dùng gắn thêm card mạng rời sau này (nâng cấp phần cứng tại chỗ), ta phải chuyển đổi kiểu đối tượng thay vì chỉ thay đổi một thuộc tính cấu hình.
  4. Mặc dù phương án dùng Composition (kết tập một thành phần `NetworkCard`) linh hoạt hơn cho việc cắm rút card mạng động, nhưng trong bối cảnh các dòng máy in văn phòng hiện đại thường được sản xuất nguyên khối (tích hợp sẵn chip mạng hoặc không), giải pháp kế thừa `NetworkPrinter` là tối ưu, tường minh và dễ bảo trì nhất.

---

## 4. KẾT QUẢ CHẠY CHƯƠNG TRÌNH VÀ KIỂM THỬ

Toàn bộ 7 thao tác nghiệp vụ theo yêu cầu mục 6 đã được kiểm thử tự động trong hàm `main()` với kết quả như sau:

```text
================================================================================
 HỆ THỐNG QUẢN LÝ THIẾT BỊ VÀ HỢP ĐỒNG BẢO TRÌ PHÒNG THỰC HÀNH
 Sinh viên thực hiện: Nguyễn Minh Đức - MSSV: 202418872
================================================================================

>>> [BƯỚC CHUẨN BỊ]: Khởi tạo các đối tượng kiểm thử...
 Đã khởi tạo thành công 5 thiết bị và 2 phòng thực hành.

--------------------------------------------------------------------------------
THAO TÁC 1: Thêm thiết bị vào từng phòng thực hành
--------------------------------------------------------------------------------
-> Đã thêm [PC001, PR001, PJ001] vào 'Phòng Đồ Họa & Thực Hành AI'
-> Đã thêm [PC002, PR002] vào 'Phòng Tin Học Cơ Sở & Văn Phòng'

--------------------------------------------------------------------------------
THAO TÁC 2: Thử thêm một thiết bị bị trùng mã (Kiểm tra ngoại lệ)
--------------------------------------------------------------------------------
-> Đang thử thêm thiết bị mã trùng 'PC001' vào 'Phòng Đồ Họa & Thực Hành AI'...
 Bắt ngoại lệ thành công (Expected): Lỗi thêm thiết bị: Mã thiết bị 'PC001' đã tồn tại trong phòng 'Phòng Đồ Họa & Thực Hành AI'!

--------------------------------------------------------------------------------
THAO TÁC 3: In danh sách thiết bị trong từng phòng thực hành
--------------------------------------------------------------------------------

===== Phòng: LAB-101 - Phòng Đồ Họa & Thực Hành AI (Sức chứa: 40, Số thiết bị: 3) =====
  1. [Computer] Mã: PC001  | Tên: Dell Precision T3640         | Năm SD: 2019 ( 7 năm) | Giá mua:  25,000,000 VNĐ | Trạng thái: Active           | RAM: 32GB | CPU: Intel Core i7-10700K | GPU rời: Có    | Mạng: Offline
  2. [NetworkPrinter] Mã: PR001  | Tên: HP Color LaserJet M479fdw    | Năm SD: 2021 ( 5 năm) | Giá mua:  14,000,000 VNĐ | Trạng thái: Active           | Loại: Laser  | Số trang: 135,000 | Chế độ: Màu       | Mạng: Offline
  3. [Projector] Mã: PJ001  | Tên: Panasonic PT-VX430           | Năm SD: 2020 ( 6 năm) | Giá mua:  18,000,000 VNĐ | Trạng thái: Active           | Độ sáng: 4500 lumens | Giờ bóng đèn: 3,600h | Mạng: Không hỗ trợ

===== Phòng: LAB-102 - Phòng Tin Học Cơ Sở & Văn Phòng (Sức chứa: 45, Số thiết bị: 2) =====
  1. [Computer] Mã: PC002  | Tên: HP ProDesk 400 G7            | Năm SD: 2023 ( 3 năm) | Giá mua:  16,000,000 VNĐ | Trạng thái: UnderMaintenance | RAM: 16GB | CPU: Intel Core i5-10500 | GPU rời: Không | Mạng: Offline
  2. [Printer] Mã: PR002  | Tên: Canon LBP2900 Classic        | Năm SD: 2022 ( 4 năm) | Giá mua:   4,000,000 VNĐ | Trạng thái: Active           | Loại: Laser  | Số trang:  42,000 | Chế độ: Trắng đen | Mạng: Không cổng mạng

--------------------------------------------------------------------------------
THAO TÁC 4: Tính tổng chi phí bảo trì dự kiến của mỗi phòng (Đa hình)
--------------------------------------------------------------------------------

 Chi tiết tính chi phí bảo trì phòng 'Phòng Đồ Họa & Thực Hành AI':
   - PC001 (Computer):    2,000,000 VNĐ  (25tr * (5% + 2% GPU + 1% (>5 năm)))
   - PR001 (NetworkPrinter):    1,360,000 VNĐ  (14tr * 4% + 500k (>100k trang) + 300k (màu))
   - PJ001 (Projector):    2,040,000 VNĐ  (18tr * 3% + 1.5tr (>3000h bóng đèn))
 => Tổng chi phí phòng LAB-101:      5,400,000 VNĐ

 Chi tiết tính chi phí bảo trì phòng 'Phòng Tin Học Cơ Sở & Văn Phòng':
   - PC002 (Computer):      800,000 VNĐ  (16tr * 5%)
   - PR002 (Printer):      160,000 VNĐ  (4tr * 4%)
 => Tổng chi phí phòng LAB-102:        960,000 VNĐ

>>> TỔNG CHI PHÍ BẢO TRÌ DỰ KIẾN TOÀN TRƯỜNG: 6,360,000 VNĐ

--------------------------------------------------------------------------------
THAO TÁC 5: Liệt kê các thiết bị cần bảo trì (UnderMaintenance HOẶC > 5 năm)
--------------------------------------------------------------------------------

Phòng 'Phòng Đồ Họa & Thực Hành AI' có 2 thiết bị cần bảo trì:
   - [PC001] Dell Precision T3640 -> Lý do: Đã sử dụng 7 năm (> 5 năm)
   - [PJ001] Panasonic PT-VX430 -> Lý do: Đã sử dụng 6 năm (> 5 năm)

Phòng 'Phòng Tin Học Cơ Sở & Văn Phòng' có 1 thiết bị cần bảo trì:
   - [PC002] HP ProDesk 400 G7 -> Lý do: Đang bảo trì (UnderMaintenance)

--------------------------------------------------------------------------------
THAO TÁC 6: Kết nối mạng cho các đối tượng thực thi INetworkable
--------------------------------------------------------------------------------
-> Đang kết nối mạng cho [PC001] với IP 192.168.1.101...
   Kết nối thành công! Trạng thái: is_connected=True, IP=192.168.1.101
-> Đang kết nối mạng cho [PR001] với IP 192.168.1.102...
   Kết nối thành công! Trạng thái: is_connected=True, IP=192.168.1.102
-> Đang kết nối mạng cho [PC002] với IP 192.168.1.103...
   Kết nối thành công! Trạng thái: is_connected=True, IP=192.168.1.103

-> Kiểm thử quy tắc: Không cho phép kết nối lại khi thiết bị đang kết nối...
 Bắt ngoại lệ thành công (Expected): Thiết bị 'PC001' đang kết nối tại 192.168.1.101. Không thể kết nối lại!

--------------------------------------------------------------------------------
THAO TÁC 7: Duyệt các thiết bị mạng thông qua interface INetworkable
--------------------------------------------------------------------------------
Tổng số thiết bị có khả năng mạng: 3
  1. Năng lực: INetworkable | Trạng thái kết nối: ĐANG KẾT NỐI | Địa chỉ IP: 192.168.1.101 | Chi tiết đối tượng: [Computer] Mã: PC001  | Tên: Dell Precision T3640         | Năm SD: 2019 ( 7 năm) | Giá mua:  25,000,000 VNĐ | Trạng thái: Active           | RAM: 32GB | CPU: Intel Core i7-10700K | GPU rời: Có    | Mạng: Online (192.168.1.101)
  2. Năng lực: INetworkable | Trạng thái kết nối: ĐANG KẾT NỐI | Địa chỉ IP: 192.168.1.102 | Chi tiết đối tượng: [NetworkPrinter] Mã: PR001  | Tên: HP Color LaserJet M479fdw    | Năm SD: 2021 ( 5 năm) | Giá mua:  14,000,000 VNĐ | Trạng thái: Active           | Loại: Laser  | Số trang: 135,000 | Chế độ: Màu       | Mạng: Online (192.168.1.102)
  3. Năng lực: INetworkable | Trạng thái kết nối: ĐANG KẾT NỐI | Địa chỉ IP: 192.168.1.103 | Chi tiết đối tượng: [Computer] Mã: PC002  | Tên: HP ProDesk 400 G7            | Năm SD: 2023 ( 3 năm) | Giá mua:  16,000,000 VNĐ | Trạng thái: UnderMaintenance | RAM: 16GB | CPU: Intel Core i5-10500 | GPU rời: Không | Mạng: Online (192.168.1.103)

-> Thử nghiệm ngắt kết nối đối với thiết bị đầu tiên...
   Sau khi disconnect: is_connected = False, ip_address = None
   (Quy tắc: Sau khi ngắt kết nối, is_connected = False và ip_address là None -> Đạt yêu cầu)

================================================================================
 HOÀN THÀNH TẤT CẢ CÁC KIỂM THỬ TỐI THIỂU THEO YÊU CẦU ĐỀ BÀI!
================================================================================
```

---

## 5. NHẬT KÝ LÀM VIỆC, TỰ PHẢN BIỆN VÀ BẰNG CHỨNG SỬ DỤNG AI

Theo quy định thực hành, sinh viên đã tuân thủ nghiêm ngặt quy trình:
1. **Chia nhỏ chức năng và commit lũy tiến:**
   - Commit 1 (`416e0f4`): `feat(core): khoi tao lop truu tuong Device va enum DeviceStatus kem validation`
   - Commit 2 (`203b3ef`): `feat(network): bo sung interface INetworkable bieu dien nang luc ket noi mang`
   - Commit 3 (`f7ce616`): `feat(devices): cai dat cac lop dan xuat Computer, Printer, NetworkPrinter, Projector`
   - Commit 4 (`d537aef`): `feat(room): them lop LabRoom quan ly tap hop thiet bi, da hinh tinh phi bao tri`
   - Commit 5 (`c097f30`): `feat(main): hoan thien kich ban kiem thu toi thieu 7 thao tac va 5 thiet bi`

2. **Thảo luận và Tự phản biện cùng AI:**
   - **Vấn đề phản biện 1: Có nên để Printer thực thi INetworkable với cờ `has_network_support` không?**
     + *Ý kiến ban đầu:* Cho lớp `Printer` thực thi `INetworkable`, nếu máy in không có mạng thì ném ngoại lệ khi gọi `connect()`.
     + *Phản biện của AI & Sinh viên:* Cách này vi phạm nguyên lý Phân tách Interface (ISP) và Liskov Substitution Principle (LSP). Client kỳ vọng mọi đối tượng `INetworkable` đều kết nối được mạng, nếu gọi mà bị crash runtime sẽ gây bất ổn định.
     + *Kết luận giải pháp:* Tách hẳn `NetworkPrinter` kế thừa `Printer, INetworkable`. Máy in thường không cài đặt giao diện mạng, đảm bảo tính trong sáng và an toàn kiểu dữ liệu.
   - **Vấn đề phản biện 2: Tính đa hình trong `CalculateAnnualMaintenanceCost()` của `LabRoom`:**
     + *Phản biện:* Cần đảm bảo tuyệt đối không có cấu trúc `if isinstance(d, Computer)` hay switch-case.
     + *Kết luận:* Đã triển khai duyệt qua `self._devices` và gọi phương thức trừu tượng; các lớp con tự chịu trách nhiệm định nghĩa logic chi phí tương ứng.
   - **Vấn đề phản biện 3: Ràng buộc tính hợp lệ của IP và trạng thái kết nối:**
     + *Phản biện:* Cần kiểm tra ngoại lệ khi người dùng cố tình gọi `connect()` 2 lần liên tiếp hoặc sau khi `disconnect()` thì thuộc tính `ip_address` vẫn còn lưu vết IP cũ.
     + *Kết luận:* Đã cài đặt kiểm tra `if self._is_connected: raise RuntimeError(...)` và khi ngắt kết nối gán triệt để `self._ip_address = None`.
"""

HTML_CONTENT = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo cáo Thực hành Tuần 05 - Lập trình Hướng đối tượng</title>
<style>
  body {
    font-family: "Times New Roman", Times, serif;
    font-size: 13pt;
    line-height: 1.5;
    margin: 40px 60px;
    color: #111;
  }
  h1 {
    font-size: 20pt;
    text-align: center;
    color: #0b3d91;
    margin-bottom: 5px;
    text-transform: uppercase;
  }
  h2 {
    font-size: 15pt;
    color: #1a5276;
    border-bottom: 2px solid #1a5276;
    padding-bottom: 4px;
    margin-top: 25px;
  }
  h3 {
    font-size: 13pt;
    color: #2874a6;
    margin-top: 18px;
  }
  h4 {
    font-size: 12pt;
    font-weight: bold;
    color: #333;
  }
  .info-box {
    background-color: #f4f6f7;
    border-left: 5px solid #0b3d91;
    padding: 12px 18px;
    margin-bottom: 25px;
    font-size: 12pt;
  }
  .info-box p { margin: 4px 0; }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
  }
  th, td {
    border: 1px solid #7f8c8d;
    padding: 8px 10px;
    text-align: left;
    font-size: 11pt;
  }
  th {
    background-color: #eaecee;
    font-weight: bold;
    color: #2c3e50;
  }
  pre, code {
    font-family: "Consolas", "Courier New", monospace;
  }
  pre {
    background-color: #f8f9fa;
    border: 1px solid #d5dbdb;
    padding: 12px;
    border-radius: 4px;
    font-size: 10pt;
    line-height: 1.35;
    overflow-x: auto;
    white-space: pre-wrap;
  }
  p code {
    background-color: #f2f3f4;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 11pt;
  }
  .highlight {
    background-color: #fff9c4;
    padding: 2px 4px;
  }
  ul, ol {
    margin-top: 5px;
    margin-bottom: 10px;
    padding-left: 25px;
  }
  li {
    margin-bottom: 5px;
  }
  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>

<h1>BÁO CÁO THỰC HÀNH TUẦN 05 (LAB W05)</h1>
<h3 style="text-align: center; color: #555; margin-top: 0;">CHỦ ĐỀ: HỆ THỐNG QUẢN LÝ THIẾT BỊ VÀ HỢP ĐỒNG BẢO TRÌ</h3>

<div class="info-box">
  <p><strong>Mã sinh viên:</strong> 202418872</p>
  <p><strong>Họ và tên:</strong> Nguyễn Minh Đức</p>
  <p><strong>Môn học:</strong> Lập trình hướng đối tượng (OOP) - Học kỳ: 2026.1</p>
  <p><strong>Kho lưu trữ GitHub:</strong> <a href="https://github.com/ngminhduc129/OOP-Bai05-DeviceManagement">https://github.com/ngminhduc129/OOP-Bai05-DeviceManagement</a></p>
  <p><strong>Tệp mã nguồn đơn nhất:</strong> <code>main.py</code></p>
</div>

<h2>1. PHÂN TÍCH YÊU CẦU NGHIỆP VỤ</h2>

<h3>1.1. Bối cảnh bài toán</h3>
<p>Một trường đại học cần xây dựng hệ thống quản lý trang thiết bị sử dụng trong các phòng thực hành công nghệ thông tin. Hệ thống tập trung giải quyết các mục tiêu:</p>
<ul>
  <li><strong>Mô hình hóa hệ phân cấp kế thừa:</strong> Các thiết bị có đặc tính chung (mã định danh, tên gọi, năm đưa vào sử dụng, đơn giá mua, trạng thái) và đặc tính kỹ thuật riêng biệt theo từng chủng loại (máy tính, máy in, máy chiếu).</li>
  <li><strong>Tính toán chi phí bảo dưỡng định kỳ:</strong> Dự toán chi phí bảo trì dự kiến trong 1 năm dựa trên độ hao mòn cơ học, thời gian sử dụng và cấu hình đặc thù.</li>
  <li><strong>Quản lý năng lực kết nối mạng:</strong> Năng lực mạng là khả năng độc lập không gắn chặt vào toàn bộ chủng loại; cần quản lý địa chỉ IP và trạng thái kết nối độc lập với cây kế thừa cơ sở.</li>
  <li><strong>Tổ chức phòng thực hành:</strong> Quản lý danh mục thiết bị của từng phòng bằng quan hệ kết tập linh hoạt.</li>
</ul>

<h3>1.2. Quy tắc nghiệp vụ chi tiết</h3>
<ul>
  <li><strong>Lớp trừu tượng Device:</strong>
    <ul>
      <li>Mã thiết bị không được rỗng, chỉ được gán khi khởi tạo (read-only).</li>
      <li>Giá mua phải lớn hơn 0.</li>
      <li>Năm đưa vào sử dụng không được lớn hơn năm hiện tại.</li>
      <li>Cung cấp phương thức trừu tượng tính chi phí bảo trì dự kiến trong một năm.</li>
      <li>Ghi đè phương thức biểu diễn chuỗi thông tin.</li>
    </ul>
  </li>
  <li><strong>Các loại thiết bị dẫn xuất:</strong>
    <ul>
      <li><strong>Máy tính (Computer):</strong> Bổ sung RAM, CPU, GPU rời. Có năng lực kết nối mạng (<code>INetworkable</code>). Chi phí bảo trì = 5% giá mua + (2% nếu có GPU rời) + (1% nếu đã dùng trên 5 năm).</li>
      <li><strong>Máy in (Printer / NetworkPrinter):</strong> Bổ sung loại máy (laser/phun), số trang đã in, có hỗ trợ mạng hay không, và thuộc tính bổ sung <code>is_color</code> (máy in màu). Chi phí bảo trì = 4% giá mua + (500.000 VNĐ nếu in &gt; 100.000 trang) + (300.000 VNĐ nếu là máy in màu).</li>
      <li><strong>Máy chiếu (Projector):</strong> Bổ sung độ sáng (lumen), số giờ bóng đèn đã chạy. Chi phí bảo trì = 3% giá mua + (1.500.000 VNĐ nếu bóng đèn dùng &gt; 3.000 giờ).</li>
    </ul>
  </li>
  <li><strong>Năng lực mạng (INetworkable):</strong>
    <ul>
      <li>Địa chỉ IP không được rỗng.</li>
      <li>Không cho phép kết nối lại khi thiết bị đang ở trạng thái kết nối.</li>
      <li>Sau khi ngắt kết nối, <code>is_connected</code> trả về <code>false</code> và thiết bị không còn lưu vết IP hoạt động.</li>
    </ul>
  </li>
  <li><strong>Phòng thực hành (LabRoom):</strong>
    <ul>
      <li>Quan hệ kết tập (Aggregation) chứa danh sách <code>Device</code>.</li>
      <li>Không thêm hai thiết bị trùng mã vào cùng một phòng.</li>
      <li>Không chấp nhận thiết bị <code>null/None</code>.</li>
      <li>Phương thức tính tổng chi phí bảo trì phải dùng <strong>Đa hình</strong>, tuyệt đối không dùng <code>if/switch/isinstance</code> để xét loại đối tượng.</li>
      <li>Lọc thiết bị cần bảo trì: Trạng thái <code>UnderMaintenance</code> HOẶC thời gian sử dụng &gt; 5 năm.</li>
    </ul>
  </li>
</ul>

<div class="page-break"></div>
<h2>2. DANH SÁCH LỚP VÀ SƠ ĐỒ QUAN HỆ</h2>

<h3>2.1. Bảng danh sách các lớp trong hệ thống</h3>
<table>
  <thead>
    <tr>
      <th style="width: 18%;">Tên lớp / Interface</th>
      <th style="width: 15%;">Loại cấu trúc</th>
      <th>Vai trò và trách nhiệm chính</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>DeviceStatus</code></td>
      <td>Enum</td>
      <td>Định nghĩa các trạng thái hoạt động: <code>Active</code>, <code>UnderMaintenance</code>, <code>Retired</code>.</td>
    </tr>
    <tr>
      <td><code>Device</code></td>
      <td>Abstract Class</td>
      <td>Lớp cơ sở trừu tượng chứa các thuộc tính dùng chung và định nghĩa phương thức thuần ảo <code>calculate_annual_maintenance_cost()</code>.</td>
    </tr>
    <tr>
      <td><code>INetworkable</code></td>
      <td>Interface (ABC)</td>
      <td>Giao diện biểu diễn năng lực kết nối mạng (<code>ip_address</code>, <code>is_connected</code>, <code>connect</code>, <code>disconnect</code>).</td>
    </tr>
    <tr>
      <td><code>Computer</code></td>
      <td>Concrete Class</td>
      <td>Kế thừa <code>Device</code> và thực thi <code>INetworkable</code>. Đại diện cho máy tính để bàn.</td>
    </tr>
    <tr>
      <td><code>Printer</code></td>
      <td>Concrete Class</td>
      <td>Kế thừa <code>Device</code>. Đại diện cho máy in thông thường qua cáp USB.</td>
    </tr>
    <tr>
      <td><code>NetworkPrinter</code></td>
      <td>Concrete Class</td>
      <td>Kế thừa <code>Printer</code> và thực thi <code>INetworkable</code>. Đại diện cho máy in mạng văn phòng.</td>
    </tr>
    <tr>
      <td><code>Projector</code></td>
      <td>Concrete Class</td>
      <td>Kế thừa <code>Device</code>. Đại diện cho máy chiếu phòng học.</td>
    </tr>
    <tr>
      <td><code>LabRoom</code></td>
      <td>Container Class</td>
      <td>Đại diện phòng thực hành, kết tập danh sách thiết bị, cài đặt các nghiệp vụ quản lý, tính chi phí đa hình và lọc bảo trì.</td>
    </tr>
  </tbody>
</table>

<h3>2.2. Sơ đồ quan hệ lớp (UML Class Diagram)</h3>
<pre>
   +-------------------------------------------------------------+
   |                       &lt;&lt;interface&gt;&gt;                         |
   |                       INetworkable                          |
   |-------------------------------------------------------------|
   | + ip_address: Optional[str] {read-only}                     |
   | + is_connected: bool {read-only}                            |
   | + connect(ip_address: str): void                            |
   | + disconnect(): void                                        |
   +-------------------------------------------------------------+
                  ^                               ^
                  |                               |
       (Cài đặt interface)             (Cài đặt interface)
                  |                               |
                  |                +--------------+--------------+
                  |                |        NetworkPrinter       |
                  |                +-----------------------------+
                  |                               ^
                  |                               | (Kế thừa)
                  |                +--------------+--------------+
                  |                |            Printer          |
                  |                +-----------------------------+
                  |                               ^
                  |                               |
+-----------------+---------------+               |
|            Computer             |               |
+---------------------------------+               |
                  ^                               |
                  | (Kế thừa)                     | (Kế thừa)
                  +---------------+---------------+
                                  |
   +------------------------------+------------------------------+
   |                        &lt;&lt;abstract&gt;&gt;                         |
   |                           Device                            |
   |-------------------------------------------------------------|
   | - _device_id: str {read-only}                               |
   | - _device_name: str                                         |
   | - _year_of_usage: int                                       |
   | - _purchase_price: float                                    |
   | - _status: DeviceStatus                                     |
   |-------------------------------------------------------------|
   | + calculate_annual_maintenance_cost()*: float                |
   | + __str__(): str                                            |
   +-------------------------------------------------------------+
                  ^                               ^
                  |                               |
                  | (Kế thừa)                     | (Kết tập - Aggregation)
                  |                               o
   +--------------+---------------+     +-------------------------+
   |          Projector           |     |         LabRoom         |
   +------------------------------+     +-------------------------+
</pre>

<div class="page-break"></div>
<h2>3. TRẢ LỜI CÂU HỎI THIẾT KẾ &amp; LÝ THUYẾT CHUYÊN SÂU</h2>

<h3>3.1. Vì sao <code>Device</code> là lớp trừu tượng?</h3>
<p><strong>1. Phù hợp với bản chất mô hình hóa thế giới thực:</strong> Trong thực tế phòng Lab, chúng ta chỉ bắt gặp các thiết bị cụ thể như máy tính Dell, máy in Laser HP hay máy chiếu Panasonic. Không tồn tại một vật thể vật lý nào chỉ là "thiết bị chung chung". Lớp trừu tượng ngăn chặn việc lập trình viên khởi tạo trực tiếp một đối tượng <code>Device()</code> mơ hồ, đảm bảo tính chặt chẽ của miền nghiệp vụ.</p>
<p><strong>2. Cung cấp khuôn mẫu giao diện (Contract) cho Đa hình:</strong> Mọi thiết bị đều phát sinh chi phí bảo trì hàng năm, nhưng công thức tính của máy tính (theo linh kiện GPU rời, tuổi đời), máy in (theo số trang in, hộp mực màu), máy chiếu (theo số giờ bóng đèn) là hoàn toàn khác biệt. Ở lớp <code>Device</code> không thể có bất kỳ cài đặt mặc định nào hợp lý. Do đó, phương thức <code>calculate_annual_maintenance_cost()</code> bắt buộc phải là phương thức thuần ảo (abstract method). Nó đóng vai trò như một giao ước để tất cả các lớp dẫn xuất phải ghi đè, cho phép lớp <code>LabRoom</code> tính toán chi phí đồng nhất mà không cần quan tâm chi tiết bên dưới.</p>

<h3>3.2. Vì sao <code>INetworkable</code> là interface?</h3>
<p><strong>1. Tách biệt Năng lực (Capability) khỏi Bản chất (Identity):</strong> Trong thiết kế hướng đối tượng, kế thừa lớp (<code>Device</code>) thể hiện quan hệ <em>"là một"</em> (is-a). Trong khi đó, khả năng kết nối mạng không phải là bản chất phân loại thiết bị, mà là một <strong>năng lực hành vi</strong> (capability / role) mà một thiết bị có thể có hoặc không.</p>
<p><strong>2. Tuân thủ nguyên lý phân tách giao diện (Interface Segregation Principle - ISP):</strong> Không phải thiết bị nào cũng có card mạng (ví dụ máy chiếu hiện tại, hoặc máy in cổng USB truyền thống). Nếu đưa các phương thức mạng vào lớp cha <code>Device</code>, các lớp con không có mạng sẽ bị ép phải thừa kế những phương thức vô nghĩa, dẫn đến việc phải ném ngoại lệ hoặc cài đặt rỗng. Interface giúp cô lập hoàn toàn năng lực mạng, lớp nào có nhu cầu mới cài đặt.</p>
<p><strong>3. Cho phép đa hình giữa các nhánh kế thừa độc lập:</strong> Interface cho phép các đối tượng thuộc các nhánh cây kế thừa khác nhau (hoặc các thiết bị thông minh khác sau này như Router, Smart Camera) có thể được xử lý đồng nhất bởi hệ thống quản trị mạng thông qua giao diện chung <code>INetworkable</code>.</p>

<h3>3.3. Tính đa hình được thể hiện ở đâu?</h3>
<p>Tính đa hình (Polymorphism) là trung tâm của bài toán, thể hiện ở 3 khía cạnh cụ thể:</p>
<ol>
  <li><strong>Đa hình trong tính tổng chi phí bảo trì của phòng (Dynamic Method Dispatch):</strong><br>
  Trong lớp <code>LabRoom</code>, phương thức <code>calculate_annual_maintenance_cost()</code> chỉ chứa một vòng lặp:
  <pre>total_cost = sum(device.calculate_annual_maintenance_cost() for device in self._devices)</pre>
  Biến <code>device</code> được xem như kiểu <code>Device</code> tổng quát. Khi chương trình chạy, môi trường thực thi sẽ tự động gọi phương thức của <code>Computer</code>, <code>Printer</code>, <code>NetworkPrinter</code>, hay <code>Projector</code> tương ứng với kiểu thực tế của đối tượng. Mã nguồn không cần bất kỳ câu lệnh <code>if/isinstance</code> nào, tuân thủ nguyên lý Mở/Đóng (Open/Closed Principle).</li>
  <li><strong>Đa hình thông qua Interface (Interface-based Polymorphism):</strong><br>
  Trong thao tác quản lý mạng (Thao tác 6 &amp; 7), chương trình duyệt qua danh sách các đối tượng thực thi <code>INetworkable</code>:
  <pre>for net_dev in networkable_devices:
    net_dev.connect(ip)</pre>
  Hệ thống giao tiếp với cả Máy tính (`Computer`) và Máy in mạng (`NetworkPrinter`) chỉ thông qua giao diện <code>INetworkable</code>, hoàn toàn độc lập với việc đối tượng đó thuộc lớp thiết bị nào.</li>
  <li><strong>Đa hình trong hiển thị thông tin (`__str__` override):</strong><br>
  Phương thức <code>__str__()</code> được từng lớp dẫn xuất ghi đè để bổ sung các thuộc tính chuyên biệt, tự động thích ứng khi gọi hàm <code>print(device)</code>.</li>
</ol>

<h3>3.4. Quan hệ giữa <code>LabRoom</code> và <code>Device</code> là kết tập hay hợp thành?</h3>
<p><strong>Kết luận:</strong> Quan hệ giữa <code>LabRoom</code> và <code>Device</code> là <strong>KẾT TẬP (Aggregation)</strong>.</p>
<p><strong>Giải thích dựa trên vòng đời đối tượng:</strong></p>
<ul>
  <li>Trong quan hệ <strong>Hợp thành (Composition)</strong>, đối tượng thành phần phụ thuộc sinh tử vào đối tượng toàn thể. Khi đối tượng toàn thể bị hủy thì các thành phần con cũng bị hủy theo.</li>
  <li>Trong bài toán quản lý thiết bị trường đại học:
    <ul>
      <li>Thiết bị có thể tồn tại độc lập trong kho trước khi được bàn giao vào bất kỳ phòng thực hành nào.</li>
      <li>Một thiết bị có thể được điều chuyển linh hoạt từ phòng này sang phòng khác.</li>
      <li>Nếu một phòng thực hành bị giải thể, đóng cửa hoặc xóa khỏi hệ thống, các thiết bị bên trong <strong>không hề bị tiêu hủy</strong> mà vẫn tiếp tục tồn tại để phục vụ phòng khác hoặc chờ thanh lý.</li>
      <li>Do đó, vòng đời của <code>Device</code> hoàn toàn độc lập với vòng đời của <code>LabRoom</code>, đúng với định nghĩa của quan hệ Kết tập.</li>
    </ul>
  </li>
</ul>

<h3>3.5. Phân tích Trade-off: Lựa chọn mô hình cho máy in có mạng</h3>
<p><strong>Phương án lựa chọn:</strong> Tách lớp <code>NetworkPrinter</code> kế thừa từ <code>Printer</code> và thực thi <code>INetworkable</code>.</p>
<p><strong>Đoạn phân tích trade-off (4 câu):</strong></p>
<ol>
  <li>Việc tách lớp <code>NetworkPrinter</code> kế thừa từ <code>Printer</code> và cài đặt <code>INetworkable</code> giúp phân tách rành mạch giữa máy in thông thường và máy in có mạng, tuân thủ nghiêm ngặt nguyên lý Phân tách giao diện (ISP) và Liskov Substitution (LSP).</li>
  <li>Phương án này loại bỏ triệt để nguy cơ lớp máy in thường phải chứa mã thừa hoặc ném ngoại lệ khi người dùng gọi các hàm mạng không hỗ trợ.</li>
  <li>Tuy nhiên, sự đánh đổi (trade-off) là làm gia tăng số lượng lớp trong cây kế thừa; nếu trong tương lai máy in thường được cắm thêm card mạng rời tại chỗ, ta phải tạo mới đối tượng <code>NetworkPrinter</code> thay vì chỉ thay đổi cờ trạng thái.</li>
  <li>Mặc dù phương án dùng Composition (kết tập một đối tượng <code>NetworkCard</code>) có độ linh hoạt cao hơn khi tháo lắp phần cứng động, nhưng trong thực tế các dòng máy in văn phòng đều được sản xuất nguyên khối (tích hợp sẵn chip mạng hoặc không), do đó phương án kế thừa <code>NetworkPrinter</code> là mô hình trực quan, tự nhiên và tối ưu nhất.</li>
</ol>

<div class="page-break"></div>
<h2>4. KẾT QUẢ CHẠY CHƯƠNG TRÌNH KIỂM THỬ</h2>
<p>Chương trình <code>main.py</code> đã thực thi đầy đủ 7 thao tác kiểm thử tối thiểu với dữ liệu mẫu theo yêu cầu mục 6:</p>
<pre>
================================================================================
 HỆ THỐNG QUẢN LÝ THIẾT BỊ VÀ HỢP ĐỒNG BẢO TRÌ PHÒNG THỰC HÀNH
 Sinh viên thực hiện: Nguyễn Minh Đức - MSSV: 202418872
================================================================================

>>> [BƯỚC CHUẨN BỊ]: Khởi tạo các đối tượng kiểm thử...
 Đã khởi tạo thành công 5 thiết bị và 2 phòng thực hành.

--------------------------------------------------------------------------------
THAO TÁC 1: Thêm thiết bị vào từng phòng thực hành
--------------------------------------------------------------------------------
-> Đã thêm [PC001, PR001, PJ001] vào 'Phòng Đồ Họa & Thực Hành AI'
-> Đã thêm [PC002, PR002] vào 'Phòng Tin Học Cơ Sở & Văn Phòng'

--------------------------------------------------------------------------------
THAO TÁC 2: Thử thêm một thiết bị bị trùng mã (Kiểm tra ngoại lệ)
--------------------------------------------------------------------------------
-> Đang thử thêm thiết bị mã trùng 'PC001' vào 'Phòng Đồ Họa & Thực Hành AI'...
 Bắt ngoại lệ thành công (Expected): Lỗi thêm thiết bị: Mã thiết bị 'PC001' đã tồn tại trong phòng 'Phòng Đồ Họa & Thực Hành AI'!

--------------------------------------------------------------------------------
THAO TÁC 3: In danh sách thiết bị trong từng phòng thực hành
--------------------------------------------------------------------------------

===== Phòng: LAB-101 - Phòng Đồ Họa & Thực Hành AI (Sức chứa: 40, Số thiết bị: 3) =====
  1. [Computer] Mã: PC001  | Tên: Dell Precision T3640         | Năm SD: 2019 ( 7 năm) | Giá mua:  25,000,000 VNĐ | Trạng thái: Active           | RAM: 32GB | CPU: Intel Core i7-10700K | GPU rời: Có    | Mạng: Offline
  2. [NetworkPrinter] Mã: PR001  | Tên: HP Color LaserJet M479fdw    | Năm SD: 2021 ( 5 năm) | Giá mua:  14,000,000 VNĐ | Trạng thái: Active           | Loại: Laser  | Số trang: 135,000 | Chế độ: Màu       | Mạng: Offline
  3. [Projector] Mã: PJ001  | Tên: Panasonic PT-VX430           | Năm SD: 2020 ( 6 năm) | Giá mua:  18,000,000 VNĐ | Trạng thái: Active           | Độ sáng: 4500 lumens | Giờ bóng đèn: 3,600h | Mạng: Không hỗ trợ

===== Phòng: LAB-102 - Phòng Tin Học Cơ Sở & Văn Phòng (Sức chứa: 45, Số thiết bị: 2) =====
  1. [Computer] Mã: PC002  | Tên: HP ProDesk 400 G7            | Năm SD: 2023 ( 3 năm) | Giá mua:  16,000,000 VNĐ | Trạng thái: UnderMaintenance | RAM: 16GB | CPU: Intel Core i5-10500 | GPU rời: Không | Mạng: Offline
  2. [Printer] Mã: PR002  | Tên: Canon LBP2900 Classic        | Năm SD: 2022 ( 4 năm) | Giá mua:   4,000,000 VNĐ | Trạng thái: Active           | Loại: Laser  | Số trang:  42,000 | Chế độ: Trắng đen | Mạng: Không cổng mạng

--------------------------------------------------------------------------------
THAO TÁC 4: Tính tổng chi phí bảo trì dự kiến của mỗi phòng (Đa hình)
--------------------------------------------------------------------------------

 Chi tiết tính chi phí bảo trì phòng 'Phòng Đồ Họa & Thực Hành AI':
   - PC001 (Computer):    2,000,000 VNĐ  (25tr * (5% + 2% GPU + 1% (>5 năm)))
   - PR001 (NetworkPrinter):    1,360,000 VNĐ  (14tr * 4% + 500k (>100k trang) + 300k (màu))
   - PJ001 (Projector):    2,040,000 VNĐ  (18tr * 3% + 1.5tr (>3000h bóng đèn))
 => Tổng chi phí phòng LAB-101:      5,400,000 VNĐ

 Chi tiết tính chi phí bảo trì phòng 'Phòng Tin Học Cơ Sở & Văn Phòng':
   - PC002 (Computer):      800,000 VNĐ  (16tr * 5%)
   - PR002 (Printer):      160,000 VNĐ  (4tr * 4%)
 => Tổng chi phí phòng LAB-102:        960,000 VNĐ

>>> TỔNG CHI PHÍ BẢO TRÌ DỰ KIẾN TOÀN TRƯỜNG: 6,360,000 VNĐ

--------------------------------------------------------------------------------
THAO TÁC 5: Liệt kê các thiết bị cần bảo trì (UnderMaintenance HOẶC > 5 năm)
--------------------------------------------------------------------------------

Phòng 'Phòng Đồ Họa & Thực Hành AI' có 2 thiết bị cần bảo trì:
   - [PC001] Dell Precision T3640 -> Lý do: Đã sử dụng 7 năm (> 5 năm)
   - [PJ001] Panasonic PT-VX430 -> Lý do: Đã sử dụng 6 năm (> 5 năm)

Phòng 'Phòng Tin Học Cơ Sở & Văn Phòng' có 1 thiết bị cần bảo trì:
   - [PC002] HP ProDesk 400 G7 -> Lý do: Đang bảo trì (UnderMaintenance)

--------------------------------------------------------------------------------
THAO TÁC 6: Kết nối mạng cho các đối tượng thực thi INetworkable
--------------------------------------------------------------------------------
-> Đang kết nối mạng cho [PC001] với IP 192.168.1.101...
   Kết nối thành công! Trạng thái: is_connected=True, IP=192.168.1.101
-> Đang kết nối mạng cho [PR001] với IP 192.168.1.102...
   Kết nối thành công! Trạng thái: is_connected=True, IP=192.168.1.102
-> Đang kết nối mạng cho [PC002] với IP 192.168.1.103...
   Kết nối thành công! Trạng thái: is_connected=True, IP=192.168.1.103

-> Kiểm thử quy tắc: Không cho phép kết nối lại khi thiết bị đang kết nối...
 Bắt ngoại lệ thành công (Expected): Thiết bị 'PC001' đang kết nối tại 192.168.1.101. Không thể kết nối lại!

--------------------------------------------------------------------------------
THAO TÁC 7: Duyệt các thiết bị mạng thông qua interface INetworkable
--------------------------------------------------------------------------------
Tổng số thiết bị có khả năng mạng: 3
  1. Năng lực: INetworkable | Trạng thái kết nối: ĐANG KẾT NỐI | Địa chỉ IP: 192.168.1.101 | Chi tiết đối tượng: [Computer] Mã: PC001  | Tên: Dell Precision T3640         | Năm SD: 2019 ( 7 năm) | Giá mua:  25,000,000 VNĐ | Trạng thái: Active           | RAM: 32GB | CPU: Intel Core i7-10700K | GPU rời: Có    | Mạng: Online (192.168.1.101)
  2. Năng lực: INetworkable | Trạng thái kết nối: ĐANG KẾT NỐI | Địa chỉ IP: 192.168.1.102 | Chi tiết đối tượng: [NetworkPrinter] Mã: PR001  | Tên: HP Color LaserJet M479fdw    | Năm SD: 2021 ( 5 năm) | Giá mua:  14,000,000 VNĐ | Trạng thái: Active           | Loại: Laser  | Số trang: 135,000 | Chế độ: Màu       | Mạng: Online (192.168.1.102)
  3. Năng lực: INetworkable | Trạng thái kết nối: ĐANG KẾT NỐI | Địa chỉ IP: 192.168.1.103 | Chi tiết đối tượng: [Computer] Mã: PC002  | Tên: HP ProDesk 400 G7            | Năm SD: 2023 ( 3 năm) | Giá mua:  16,000,000 VNĐ | Trạng thái: UnderMaintenance | RAM: 16GB | CPU: Intel Core i5-10500 | GPU rời: Không | Mạng: Online (192.168.1.103)

-> Thử nghiệm ngắt kết nối đối với thiết bị đầu tiên...
   Sau khi disconnect: is_connected = False, ip_address = None
   (Quy tắc: Sau khi ngắt kết nối, is_connected = False và ip_address là None -> Đạt yêu cầu)

================================================================================
 HOÀN THÀNH TẤT CẢ CÁC KIỂM THỬ TỐI THIỂU THEO YÊU CẦU ĐỀ BÀI!
================================================================================
</pre>

<div class="page-break"></div>
<h2>5. BẰNG CHỨNG SỬ DỤNG AI &amp; NHẬT KÝ COMMIT</h2>
<p>Sinh viên đã thực hiện nghiêm túc quy trình làm bài:</p>
<ol>
  <li><strong>Lịch sử Git Commit lũy tiến theo từng chức năng:</strong>
    <ul>
      <li><code>416e0f4</code> - <em>feat(core): khoi tao lop truu tuong Device va enum DeviceStatus kem validation</em></li>
      <li><code>203b3ef</code> - <em>feat(network): bo sung interface INetworkable bieu dien nang luc ket noi mang</em></li>
      <li><code>f7ce616</code> - <em>feat(devices): cai dat cac lop dan xuat Computer, Printer, NetworkPrinter, Projector</em></li>
      <li><code>d537aef</code> - <em>feat(room): them lop LabRoom quan ly tap hop thiet bi, da hinh tinh phi bao tri</em></li>
      <li><code>c097f30</code> - <em>feat(main): hoan thien kich ban kiem thu toi thieu 7 thao tac va 5 thiet bi</em></li>
    </ul>
  </li>
  <li><strong>Quá trình thảo luận và phản biện cùng AI:</strong>
    <ul>
      <li><strong>Chủ đề 1: Mô hình hóa máy in có khả năng mạng:</strong> Đã tranh luận giữa việc gán cờ trong lớp <code>Printer</code> và việc tạo lớp con <code>NetworkPrinter</code>. AI và sinh viên đã thống nhất giải pháp tạo <code>NetworkPrinter</code> nhằm bảo vệ nguyên lý ISP.</li>
      <li><strong>Chủ đề 2: Tính đa hình trong tính toán bảo trì:</strong> Đã rà soát để đảm bảo trong toàn bộ code của <code>LabRoom</code> không sử dụng kiểm tra kiểu cụ thể bằng <code>if isinstance(...)</code>, đảm bảo tính đa hình thuần túy.</li>
      <li><strong>Chủ đề 3: Phân tích vòng đời đối tượng LabRoom và Device:</strong> Đã chứng minh được đây là quan hệ Aggregation thông qua thực tế thiết bị có vòng đời độc lập với phòng thực hành.</li>
    </ul>
  </li>
</ol>

</body>
</html>
"""

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(base_dir, "BaoCao_Lab_W05.md")
    html_file = os.path.join(base_dir, "BaoCao_Lab_W05.html")
    docx_file = os.path.join(base_dir, "BaoCao_Lab_W05.docx")
    pdf_file = os.path.join(base_dir, "BaoCao_Lab_W05.pdf")

    print("1. Đang ghi file Markdown BaoCao_Lab_W05.md...")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(MD_CONTENT)

    print("2. Đang ghi file HTML BaoCao_Lab_W05.html...")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)

    html_p = html_file.replace('\\', '/')
    docx_p = docx_file.replace('\\', '/')
    pdf_p = pdf_file.replace('\\', '/')

    print("3. Đang chuyển đổi HTML sang DOCX và PDF qua Word Application...")
    ps_script = f"""
    $htmlPath = "{html_p}"
    $docxPath = "{docx_p}"
    $pdfPath = "{pdf_p}"

    try {{
        $word = New-Object -ComObject Word.Application
        $word.Visible = $false
        $doc = $word.Documents.Open($htmlPath)
        
        # Save as docx (Format 16 = wdFormatXMLDocument)
        $doc.SaveAs2($docxPath, 16)
        Write-Host " Đã lưu DOCX: $docxPath"

        # Save as pdf (Format 17 = wdFormatPDF)
        $doc.SaveAs2($pdfPath, 17)
        Write-Host " Đã lưu PDF: $pdfPath"

        $doc.Close()
        $word.Quit()
        Write-Host " Hoàn tất chuyển đổi Word & PDF thành công!"
    }} catch {{
        Write-Host " Lỗi trong quá trình chuyển đổi qua Word: $_"
    }}
    """

    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print(res.stderr)

    print("Hoàn tất tạo các file báo cáo!")

if __name__ == "__main__":
    main()
