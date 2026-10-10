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
            f"[{self.__class__.__name__}] Mã: {self._device_id} | "
            f"Tên: {self._device_name} | "
            f"Năm SD: {self._year_of_usage} ({self.age} năm) | "
            f"Giá mua: {self._purchase_price:,.0f} VNĐ | "
            f"Trạng thái: {self._status.value}"
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
