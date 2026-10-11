# /****************/
# 202418872
# Nguyễn Minh Đức
# /****************/

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from typing import List, Optional


class DeviceStatus(Enum):
    """Định nghĩa các trạng thái hoạt động của thiết bị."""
    ACTIVE = "Active"
    UNDER_MAINTENANCE = "UnderMaintenance"
    RETIRED = "Retired"


class Device(ABC):
    """
    Lớp trừu tượng đại diện cho một thiết bị chung trong phòng thực hành.
    Chứa các thuộc tính dùng chung và định nghĩa phương thức trừu tượng tính chi phí bảo trì.
    """

    def __init__(
        self,
        device_id: str,
        device_name: str,
        year_of_usage: int,
        purchase_price: float,
        status: DeviceStatus = DeviceStatus.ACTIVE
    ) -> None:
        # Kiểm tra tính hợp lệ của mã thiết bị (không được rỗng)
        if not device_id or not device_id.strip():
            raise ValueError("Mã thiết bị không được rỗng.")

        # Kiểm tra tính hợp lệ của giá mua (phải lớn hơn 0)
        if purchase_price <= 0:
            raise ValueError(f"Giá mua phải lớn hơn 0. Giá hiện tại: {purchase_price}")

        # Kiểm tra tính hợp lệ của năm đưa vào sử dụng (không được lớn hơn năm hiện tại)
        current_year = datetime.now().year
        if year_of_usage > current_year:
            raise ValueError(
                f"Năm đưa vào sử dụng ({year_of_usage}) không được lớn hơn năm hiện tại ({current_year})."
            )

        # Mã thiết bị chỉ được thiết lập khi khởi tạo (read-only thông qua property)
        self._device_id: str = device_id.strip()
        self._device_name: str = device_name.strip()
        self._year_of_usage: int = year_of_usage
        self._purchase_price: float = float(purchase_price)
        self._status: DeviceStatus = status

    @property
    def device_id(self) -> str:
        """Mã thiết bị - chỉ đọc, không thể sửa sau khi khởi tạo."""
        return self._device_id

    @property
    def device_name(self) -> str:
        return self._device_name

    @device_name.setter
    def device_name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Tên thiết bị không được để trống.")
        self._device_name = value.strip()

    @property
    def year_of_usage(self) -> int:
        return self._year_of_usage

    @property
    def purchase_price(self) -> float:
        return self._purchase_price

    @property
    def status(self) -> DeviceStatus:
        return self._status

    @status.setter
    def status(self, new_status: DeviceStatus) -> None:
        if not isinstance(new_status, DeviceStatus):
            raise TypeError("Trạng thái phải thuộc kiểu DeviceStatus.")
        self._status = new_status

    @property
    def age(self) -> int:
        """Số năm đã đưa vào sử dụng."""
        return datetime.now().year - self._year_of_usage

    @abstractmethod
    def calculate_annual_maintenance_cost(self) -> float:
        """Phương thức trừu tượng tính chi phí bảo trì dự kiến trong 1 năm."""
        pass

    def __str__(self) -> str:
        """Biểu diễn thông tin thiết bị dưới dạng chuỗi."""
        return (
            f"[{self.__class__.__name__}] Mã: {self._device_id:<6} | "
            f"Tên: {self._device_name:<28} | "
            f"Năm SD: {self._year_of_usage} ({self.age:2d} năm) | "
            f"Giá mua: {self._purchase_price:>11,.0f} VNĐ | "
            f"Trạng thái: {self._status.value:<16}"
        )


class INetworkable(ABC):
    """
    Interface biểu diễn năng lực kết nối mạng của thiết bị.
    Độc lập với cây kế thừa Device.
    """

    @property
    @abstractmethod
    def ip_address(self) -> Optional[str]:
        """Địa chỉ IP hiện tại của thiết bị (None nếu chưa kết nối)."""
        pass

    @abstractmethod
    def connect(self, ip_address: str) -> None:
        """
        Kết nối thiết bị vào mạng với địa chỉ IP được cấp.
        Yêu cầu:
        - Địa chỉ IP không được rỗng.
        - Không cho phép kết nối lại khi thiết bị đang kết nối.
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """
        Ngắt kết nối mạng.
        Yêu cầu:
        - Sau khi ngắt kết nối, is_connected phải trả về False.
        - Đối tượng không còn địa chỉ IP đang hoạt động sau khi ngắt kết nối.
        """
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Kiểm tra trạng thái kết nối mạng của thiết bị."""
        pass


class Computer(Device, INetworkable):
    """
    Lớp Máy tính kế thừa Device và thực thi interface INetworkable.
    Máy tính luôn có khả năng kết nối mạng.
    """

    def __init__(
        self,
        device_id: str,
        device_name: str,
        year_of_usage: int,
        purchase_price: float,
        ram_size_gb: int,
        processor_type: str,
        has_discrete_gpu: bool,
        status: DeviceStatus = DeviceStatus.ACTIVE
    ) -> None:
        super().__init__(device_id, device_name, year_of_usage, purchase_price, status)

        if ram_size_gb <= 0:
            raise ValueError("Dung lượng RAM phải lớn hơn 0 GB.")
        if not processor_type or not processor_type.strip():
            raise ValueError("Loại bộ xử lý không được để trống.")

        self.ram_size_gb: int = ram_size_gb
        self.processor_type: str = processor_type.strip()
        self.has_discrete_gpu: bool = has_discrete_gpu

        # Các thuộc tính phục vụ kết nối mạng (INetworkable)
        self._ip_address: Optional[str] = None
        self._is_connected: bool = False

    # --- Triển khai INetworkable ---
    @property
    def ip_address(self) -> Optional[str]:
        return self._ip_address

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    def connect(self, ip_address: str) -> None:
        if not ip_address or not ip_address.strip():
            raise ValueError("Địa chỉ IP không được rỗng.")
        if self._is_connected:
            raise RuntimeError(
                f"Thiết bị '{self.device_id}' đang kết nối tại {self._ip_address}. Không thể kết nối lại!"
            )
        self._ip_address = ip_address.strip()
        self._is_connected = True

    def disconnect(self) -> None:
        self._ip_address = None
        self._is_connected = False

    # --- Triển khai tính chi phí bảo trì ---
    def calculate_annual_maintenance_cost(self) -> float:
        """
        Chi phí bảo trì máy tính:
        - 5% giá mua cơ bản.
        - Cộng thêm 2% giá mua nếu có GPU rời.
        - Nếu thiết bị đã sử dụng trên 5 năm (> 5), cộng thêm 1% giá mua.
        """
        rate = 0.05
        if self.has_discrete_gpu:
            rate += 0.02
        if self.age > 5:
            rate += 0.01
        return self._purchase_price * rate

    def __str__(self) -> str:
        net_info = f"Online ({self._ip_address})" if self._is_connected else "Offline"
        return (
            f"{super().__str__()} | RAM: {self.ram_size_gb:2d}GB | CPU: {self.processor_type:<18} | "
            f"GPU rời: {'Có' if self.has_discrete_gpu else 'Không':<5} | Mạng: {net_info}"
        )


class Printer(Device):
    """
    Lớp Máy in kế thừa Device.
    Đại diện cho máy in thông thường (không có kết nối mạng trực tiếp).
    """

    def __init__(
        self,
        device_id: str,
        device_name: str,
        year_of_usage: int,
        purchase_price: float,
        printer_type: str,
        pages_printed: int,
        has_network_support: bool = False,
        is_color: bool = False,
        status: DeviceStatus = DeviceStatus.ACTIVE
    ) -> None:
        super().__init__(device_id, device_name, year_of_usage, purchase_price, status)

        if not printer_type or printer_type.strip().lower() not in ["laser", "phun", "inkjet"]:
            raise ValueError("Loại máy in phải là 'laser' hoặc 'phun'.")
        if pages_printed < 0:
            raise ValueError("Số trang đã in không được âm.")

        self.printer_type: str = printer_type.strip().lower()
        self.pages_printed: int = pages_printed
        self.has_network_support: bool = has_network_support
        # Thuộc tính bổ sung có giải thích: máy in màu có chi phí mực và cụm sấy/đầu phun bảo dưỡng cao hơn
        self.is_color: bool = is_color

    def calculate_annual_maintenance_cost(self) -> float:
        """
        Chi phí bảo trì máy in:
        - 4% giá mua.
        - Cộng thêm 500.000 đồng nếu số trang đã in > 100.000.
        - Cộng thêm 300.000 đồng nếu là máy in màu.
        """
        cost = self._purchase_price * 0.04
        if self.pages_printed > 100_000:
            cost += 500_000.0
        if self.is_color:
            cost += 300_000.0
        return cost

    def __str__(self) -> str:
        color_str = "Màu" if self.is_color else "Trắng đen"
        net_str = "Hỗ trợ cổng mạng" if self.has_network_support else "Không cổng mạng"
        return (
            f"{super().__str__()} | Loại: {self.printer_type.capitalize():<6} | "
            f"Số trang: {self.pages_printed:>7,} | Chế độ: {color_str:<9} | Mạng: {net_str}"
        )


class NetworkPrinter(Printer, INetworkable):
    """
    Máy in hỗ trợ kết nối mạng (NetworkPrinter).
    Kế thừa Printer và thực thi interface INetworkable.
    Đây là thiết kế mô hình hóa cho yêu cầu 'chỉ một số máy in có khả năng mạng'
    theo nguyên lý phân tách interface (ISP).
    """

    def __init__(
        self,
        device_id: str,
        device_name: str,
        year_of_usage: int,
        purchase_price: float,
        printer_type: str,
        pages_printed: int,
        is_color: bool = False,
        status: DeviceStatus = DeviceStatus.ACTIVE
    ) -> None:
        # has_network_support luôn là True đối với NetworkPrinter
        super().__init__(
            device_id=device_id,
            device_name=device_name,
            year_of_usage=year_of_usage,
            purchase_price=purchase_price,
            printer_type=printer_type,
            pages_printed=pages_printed,
            has_network_support=True,
            is_color=is_color,
            status=status
        )
        self._ip_address: Optional[str] = None
        self._is_connected: bool = False

    # --- Triển khai INetworkable ---
    @property
    def ip_address(self) -> Optional[str]:
        return self._ip_address

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    def connect(self, ip_address: str) -> None:
        if not ip_address or not ip_address.strip():
            raise ValueError("Địa chỉ IP không được rỗng.")
        if self._is_connected:
            raise RuntimeError(
                f"Máy in mạng '{self.device_id}' đang kết nối tại {self._ip_address}. Không thể kết nối lại!"
            )
        self._ip_address = ip_address.strip()
        self._is_connected = True

    def disconnect(self) -> None:
        self._ip_address = None
        self._is_connected = False

    def __str__(self) -> str:
        net_status = f"Online ({self._ip_address})" if self._is_connected else "Offline"
        color_str = "Màu" if self.is_color else "Trắng đen"
        return (
            f"[{self.__class__.__name__}] Mã: {self._device_id:<6} | "
            f"Tên: {self._device_name:<28} | "
            f"Năm SD: {self._year_of_usage} ({self.age:2d} năm) | "
            f"Giá mua: {self._purchase_price:>11,.0f} VNĐ | "
            f"Trạng thái: {self._status.value:<16} | "
            f"Loại: {self.printer_type.capitalize():<6} | "
            f"Số trang: {self.pages_printed:>7,} | Chế độ: {color_str:<9} | Mạng: {net_status}"
        )


class Projector(Device):
    """
    Lớp Máy chiếu kế thừa Device.
    Không có yêu cầu kết nối mạng trong phiên bản hiện tại.
    """

    def __init__(
        self,
        device_id: str,
        device_name: str,
        year_of_usage: int,
        purchase_price: float,
        brightness_lumens: int,
        lamp_hours_used: int,
        status: DeviceStatus = DeviceStatus.ACTIVE
    ) -> None:
        super().__init__(device_id, device_name, year_of_usage, purchase_price, status)

        if brightness_lumens <= 0:
            raise ValueError("Độ sáng (lumen) phải lớn hơn 0.")
        if lamp_hours_used < 0:
            raise ValueError("Số giờ sử dụng bóng đèn không được âm.")

        self.brightness_lumens: int = brightness_lumens
        self.lamp_hours_used: int = lamp_hours_used

    def calculate_annual_maintenance_cost(self) -> float:
        """
        Chi phí bảo trì máy chiếu:
        - 3% giá mua.
        - Cộng thêm 1.500.000 đồng nếu bóng đèn đã sử dụng trên 3.000 giờ (> 3000).
        """
        cost = self._purchase_price * 0.03
        if self.lamp_hours_used > 3_000:
            cost += 1_500_000.0
        return cost

    def __str__(self) -> str:
        return (
            f"{super().__str__()} | Độ sáng: {self.brightness_lumens:4d} lumens | "
            f"Giờ bóng đèn: {self.lamp_hours_used:>5,}h | Mạng: Không hỗ trợ"
        )


class LabRoom:
    """
    Lớp LabRoom biểu diễn phòng thực hành.
    Thể hiện quan hệ KẾT TẬP (Aggregation) với Device:
    - Phòng chứa danh sách các thiết bị.
    - Thiết bị có thể tồn tại độc lập mà không nhất thiết phải thuộc về phòng nào.
    - Nếu phòng bị xóa, thiết bị vẫn tiếp tục tồn tại.
    """

    def __init__(self, room_id: str, room_name: str, capacity: int) -> None:
        if not room_id or not room_id.strip():
            raise ValueError("Mã phòng không được để trống.")
        if not room_name or not room_name.strip():
            raise ValueError("Tên phòng không được để trống.")
        if capacity <= 0:
            raise ValueError("Sức chứa phòng phải lớn hơn 0.")

        self.room_id: str = room_id.strip()
        self.room_name: str = room_name.strip()
        self.capacity: int = capacity
        self._devices: List[Device] = []

    @property
    def devices(self) -> List[Device]:
        """Trả về bản sao danh sách thiết bị để đảm bảo tính đóng gói."""
        return list(self._devices)

    def add_device(self, device: Device) -> None:
        """
        Thêm thiết bị vào phòng.
        Quy tắc:
        1. Không chấp nhận đối tượng thiết bị null/None.
        2. Không thêm hai thiết bị có cùng mã vào một phòng.
        """
        if device is None:
            raise TypeError("Không chấp nhận đối tượng thiết bị null (None).")
        if not isinstance(device, Device):
            raise TypeError("Đối tượng phải kế thừa từ lớp Device.")

        # Kiểm tra trùng mã thiết bị trong phòng
        if any(d.device_id == device.device_id for d in self._devices):
            raise ValueError(
                f"Lỗi thêm thiết bị: Mã thiết bị '{device.device_id}' đã tồn tại trong phòng '{self.room_name}'!"
            )

        self._devices.append(device)

    def remove_device(self, device_id: str) -> bool:
        """Xóa thiết bị khỏi phòng theo mã thiết bị."""
        if not device_id:
            return False
        for i, device in enumerate(self._devices):
            if device.device_id == device_id.strip():
                del self._devices[i]
                return True
        return False

    def find_device(self, device_id: str) -> Optional[Device]:
        """Tìm thiết bị theo mã trong phòng."""
        if not device_id:
            return None
        target_id = device_id.strip()
        for device in self._devices:
            if device.device_id == target_id:
                return device
        return None

    def calculate_annual_maintenance_cost(self) -> float:
        """
        Tính tổng chi phí bảo trì dự kiến trong 1 năm của tất cả thiết bị trong phòng.
        Quy tắc:
        - Phải sử dụng tính ĐA HÌNH (Polymorphism).
        - Tuyệt đối không kiểm tra lần lượt bằng if hoặc switch/isinstance để xét loại thiết bị.
        """
        total_cost = 0.0
        for device in self._devices:
            # Gọi phương thức ảo/trừu tượng thông qua tham chiếu lớp cơ sở Device
            total_cost += device.calculate_annual_maintenance_cost()
        return total_cost

    def get_devices_requiring_maintenance(self) -> List[Device]:
        """
        Lọc danh sách các thiết bị cần bảo trì:
        - Đang ở trạng thái UnderMaintenance; HOẶC
        - Có thời gian sử dụng trên 5 năm (> 5 năm).
        """
        result = []
        for device in self._devices:
            if device.status == DeviceStatus.UNDER_MAINTENANCE or device.age > 5:
                result.append(device)
        return result

    def __str__(self) -> str:
        return f"Phòng: {self.room_id} - {self.room_name} (Sức chứa: {self.capacity}, Số thiết bị: {len(self._devices)})"
