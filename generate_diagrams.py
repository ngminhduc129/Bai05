# /****************/
# 202418872
# Nguyễn Minh Đức
# /****************/

import os
import xml.sax.saxutils as saxutils

def generate_drawio():
    """Tạo file class_diagram.drawio chuẩn xác 100%, không bị lỗi font hay đè chữ."""
    
    # Định nghĩa các lớp với HTML nội dung chuẩn
    classes = [
        {
            "id": "c_net",
            "title": "«interface»<br/><b>INetworkable</b>",
            "attrs": "+ ip_address: Optional[str]<br/>+ is_connected: bool",
            "meths": "+ connect(ip_address: str): void<br/>+ disconnect(): void",
            "x": 120, "y": 60, "w": 260, "h": 140,
            "fill": "#e1f5fe", "stroke": "#0288d1"
        },
        {
            "id": "c_status",
            "title": "«enumeration»<br/><b>DeviceStatus</b>",
            "attrs": "ACTIVE<br/>UNDER_MAINTENANCE<br/>RETIRED",
            "meths": "",
            "x": 600, "y": 60, "w": 200, "h": 120,
            "fill": "#f3e5f5", "stroke": "#7b1fa2"
        },
        {
            "id": "c_dev",
            "title": "«abstract»<br/><b>Device</b>",
            "attrs": "- _device_id: str<br/>- _device_name: str<br/>- _year_of_usage: int<br/>- _purchase_price: float<br/>- _status: DeviceStatus<br/>+ device_id: str {read-only}<br/>+ age: int {derived}",
            "meths": "+ calculate_annual_maintenance_cost()*: float<br/>+ __str__(): str",
            "x": 540, "y": 250, "w": 320, "h": 240,
            "fill": "#fff2cc", "stroke": "#d6b656"
        },
        {
            "id": "c_room",
            "title": "<b>LabRoom</b>",
            "attrs": "+ room_id: str<br/>+ room_name: str<br/>+ capacity: int<br/>- _devices: List[Device]",
            "meths": "+ add_device(device: Device): void<br/>+ remove_device(device_id: str): bool<br/>+ find_device(device_id: str): Optional[Device]<br/>+ calculate_annual_maintenance_cost(): float<br/>+ get_devices_requiring_maintenance(): List[Device]",
            "x": 1040, "y": 250, "w": 320, "h": 240,
            "fill": "#d5e8d4", "stroke": "#82b366"
        },
        {
            "id": "c_pc",
            "title": "<b>Computer</b>",
            "attrs": "+ ram_size_gb: int<br/>+ processor_type: str<br/>+ has_discrete_gpu: bool<br/>- _ip_address: Optional[str]<br/>- _is_connected: bool",
            "meths": "+ calculate_annual_maintenance_cost(): float<br/>+ connect(ip_address: str): void<br/>+ disconnect(): void",
            "x": 100, "y": 600, "w": 280, "h": 210,
            "fill": "#dae8fc", "stroke": "#6c8ebf"
        },
        {
            "id": "c_pr",
            "title": "<b>Printer</b>",
            "attrs": "+ printer_type: str<br/>+ pages_printed: int<br/>+ has_network_support: bool<br/>+ is_color: bool",
            "meths": "+ calculate_annual_maintenance_cost(): float",
            "x": 460, "y": 600, "w": 270, "h": 170,
            "fill": "#dae8fc", "stroke": "#6c8ebf"
        },
        {
            "id": "c_net_pr",
            "title": "<b>NetworkPrinter</b>",
            "attrs": "- _ip_address: Optional[str]<br/>- _is_connected: bool",
            "meths": "+ connect(ip_address: str): void<br/>+ disconnect(): void",
            "x": 460, "y": 860, "w": 270, "h": 150,
            "fill": "#e1f5fe", "stroke": "#0288d1"
        },
        {
            "id": "c_pj",
            "title": "<b>Projector</b>",
            "attrs": "+ brightness_lumens: int<br/>+ lamp_hours_used: int",
            "meths": "+ calculate_annual_maintenance_cost(): float",
            "x": 800, "y": 600, "w": 270, "h": 160,
            "fill": "#dae8fc", "stroke": "#6c8ebf"
        }
    ]

    cells_xml = []
    
    # 0 & 1 layer roots
    cells_xml.append('<mxCell id="0" />')
    cells_xml.append('<mxCell id="1" parent="0" />')

    for c in classes:
        # Build HTML content inside cell
        content = f'<div style="text-align: center; font-weight: normal; margin-bottom: 6px;">{c["title"]}</div><hr size="1" style="border: 0; border-top: 1px solid {c["stroke"]}; margin: 4px 0;"/><div style="text-align: left; font-size: 11px; line-height: 1.4; padding: 0 4px;">{c["attrs"]}</div>'
        if c["meths"]:
            content += f'<hr size="1" style="border: 0; border-top: 1px solid {c["stroke"]}; margin: 4px 0;"/><div style="text-align: left; font-size: 11px; line-height: 1.4; padding: 0 4px;">{c["meths"]}</div>'
        
        escaped_val = saxutils.escape(content, {'"': '&quot;'})
        style = f"html=1;whiteSpace=wrap;rounded=1;verticalAlign=top;align=left;spacing=6;fillColor={c['fill']};strokeColor={c['stroke']};strokeWidth=1.5;fontFamily=Segoe UI,Helvetica,Arial;fontSize=12;shadow=0;"
        cell_str = f'<mxCell id="{c["id"]}" value="{escaped_val}" style="{style}" vertex="1" parent="1">\n  <mxGeometry x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" as="geometry" />\n</mxCell>'
        cells_xml.append(cell_str)

    # Thêm các liên kết (Edges) với routing rõ ràng
    edges = [
        # Computer -> Device (Inheritance)
        {
            "id": "e_pc_dev",
            "src": "c_pc", "tgt": "c_dev",
            "style": "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=0;strokeWidth=1.5;strokeColor=#333333;entryX=0.25;entryY=1;entryDx=0;entryDy=0;",
            "label": ""
        },
        # Printer -> Device (Inheritance)
        {
            "id": "e_pr_dev",
            "src": "c_pr", "tgt": "c_dev",
            "style": "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=0;strokeWidth=1.5;strokeColor=#333333;entryX=0.5;entryY=1;entryDx=0;entryDy=0;",
            "label": ""
        },
        # Projector -> Device (Inheritance)
        {
            "id": "e_pj_dev",
            "src": "c_pj", "tgt": "c_dev",
            "style": "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=0;strokeWidth=1.5;strokeColor=#333333;entryX=0.75;entryY=1;entryDx=0;entryDy=0;",
            "label": ""
        },
        # NetworkPrinter -> Printer (Inheritance)
        {
            "id": "e_npr_pr",
            "src": "c_net_pr", "tgt": "c_pr",
            "style": "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=0;strokeWidth=1.5;strokeColor=#333333;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;",
            "label": ""
        },
        # Computer ..> INetworkable (Realization)
        {
            "id": "e_pc_net",
            "src": "c_pc", "tgt": "c_net",
            "style": "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;dashed=1;endArrow=block;endFill=0;strokeWidth=1.5;strokeColor=#0288D1;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;",
            "label": ""
        },
        # NetworkPrinter ..> INetworkable (Realization vòng qua bên trái)
        {
            "id": "e_npr_net",
            "src": "c_net_pr", "tgt": "c_net",
            "style": "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;dashed=1;endArrow=block;endFill=0;strokeWidth=1.5;strokeColor=#0288D1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
            "label": ""
        },
        # LabRoom o-- Device (Aggregation)
        {
            "id": "e_room_dev",
            "src": "c_room", "tgt": "c_dev",
            "style": "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;startArrow=diamond;startFill=0;endArrow=none;strokeWidth=1.5;strokeColor=#2E7D32;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;",
            "label": "1       * (contains)"
        },
        # Device --> DeviceStatus (Association)
        {
            "id": "e_dev_status",
            "src": "c_dev", "tgt": "c_status",
            "style": "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=open;endFill=0;strokeWidth=1.5;strokeColor=#7B1FA2;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;",
            "label": "uses"
        }
    ]

    for e in edges:
        lbl_escaped = saxutils.escape(e["label"])
        edge_str = f'<mxCell id="{e["id"]}" value="{lbl_escaped}" style="{e["style"]}" edge="1" parent="1" source="{e["src"]}" target="{e["tgt"]}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        cells_xml.append(edge_str)

    cells_joined = "\n      ".join(cells_xml)
    
    drawio_content = f"""<mxfile host="app.diagrams.net" modified="2026-10-11T06:00:00.000Z" agent="Mozilla/5.0" version="24.0.0">
  <diagram id="OOP_Lab05_ClassDiagram" name="Class Diagram - Lab W05">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">
      <root>
      {cells_joined}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""

    with open("class_diagram.drawio", "w", encoding="utf-8") as f:
        f.write(drawio_content)
    print(" Đã tạo thành công file class_diagram.drawio chuẩn!")

def generate_svg():
    """Tạo file class_diagram.svg sắc nét để xem trực tiếp hoặc chèn Word."""
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1450 1080" width="1450" height="1080" style="background:#ffffff; font-family:'Segoe UI', Helvetica, Arial, sans-serif;">
  <defs>
    <!-- Markers -->
    <!-- Triangle closed for Inheritance -->
    <marker id="arrow-inherit" viewBox="0 0 14 14" refX="14" refY="7" markerWidth="12" markerHeight="12" orient="auto">
      <polygon points="0,0 14,7 0,14" fill="#ffffff" stroke="#222222" stroke-width="1.5" />
    </marker>
    <!-- Triangle closed for Realization (Blue) -->
    <marker id="arrow-realize" viewBox="0 0 14 14" refX="14" refY="7" markerWidth="12" markerHeight="12" orient="auto">
      <polygon points="0,0 14,7 0,14" fill="#ffffff" stroke="#0288D1" stroke-width="1.5" />
    </marker>
    <!-- Diamond for Aggregation (Green) -->
    <marker id="diamond-agg" viewBox="0 0 18 10" refX="0" refY="5" markerWidth="18" markerHeight="10" orient="auto">
      <polygon points="0,5 9,0 18,5 9,10" fill="#ffffff" stroke="#2E7D32" stroke-width="1.5" />
    </marker>
    <!-- Open arrow for Association (Purple) -->
    <marker id="arrow-assoc" viewBox="0 0 12 12" refX="12" refY="6" markerWidth="10" markerHeight="10" orient="auto">
      <polyline points="2,2 10,6 2,10" fill="none" stroke="#7B1FA2" stroke-width="1.5" />
    </marker>
    
    <!-- Shadow filter -->
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.12"/>
    </filter>
  </defs>

  <!-- Title Banner -->
  <rect x="30" y="15" width="1390" height="40" rx="6" fill="#0b3d91"/>
  <text x="725" y="41" text-anchor="middle" fill="#ffffff" font-size="18" font-weight="bold">CLASS DIAGRAM - HỆ THỐNG QUẢN LÝ THIẾT BỊ VÀ BẢO TRÌ (LAB W05)</text>

  <!-- RELATION LINES (Draw below classes) -->
  
  <!-- 1. Realization: Computer ..> INetworkable (Straight vertical dashed) -->
  <path d="M 240 600 L 240 212" fill="none" stroke="#0288D1" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow-realize)"/>
  
  <!-- 2. Realization: NetworkPrinter ..> INetworkable (Around the left) -->
  <path d="M 460 935 L 45 935 L 45 130 L 108 130" fill="none" stroke="#0288D1" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow-realize)"/>

  <!-- 3. Inheritance: NetworkPrinter -> Printer -->
  <path d="M 595 860 L 595 782" fill="none" stroke="#333333" stroke-width="2" marker-end="url(#arrow-inherit)"/>

  <!-- 4. Inheritance: Printer -> Device -->
  <path d="M 595 600 L 595 540 L 700 540 L 700 502" fill="none" stroke="#333333" stroke-width="2" marker-end="url(#arrow-inherit)"/>

  <!-- 5. Inheritance: Computer -> Device -->
  <path d="M 320 600 L 320 540 L 650 540 L 650 502" fill="none" stroke="#333333" stroke-width="2" marker-end="url(#arrow-inherit)"/>

  <!-- 6. Inheritance: Projector -> Device -->
  <path d="M 935 600 L 935 540 L 750 540 L 750 502" fill="none" stroke="#333333" stroke-width="2" marker-end="url(#arrow-inherit)"/>

  <!-- 7. Aggregation: LabRoom o-- Device -->
  <path d="M 1040 370 L 872 370" fill="none" stroke="#2E7D32" stroke-width="2" marker-start="url(#diamond-agg)"/>
  <text x="955" y="360" text-anchor="middle" font-size="12" font-weight="bold" fill="#2E7D32">1        * (contains)</text>

  <!-- 8. Association: Device --> DeviceStatus -->
  <path d="M 700 250 L 700 192" fill="none" stroke="#7B1FA2" stroke-width="2" marker-end="url(#arrow-assoc)"/>
  <text x="715" y="220" font-size="12" font-weight="bold" fill="#7B1FA2">uses</text>


  <!-- CLASS BOXES -->

  <!-- 1. Interface INetworkable -->
  <g filter="url(#shadow)">
    <rect x="120" y="70" width="260" height="135" rx="8" fill="#e1f5fe" stroke="#0288d1" stroke-width="2"/>
    <text x="250" y="93" text-anchor="middle" font-size="12" fill="#0277bd">&lt;&lt;interface&gt;&gt;</text>
    <text x="250" y="110" text-anchor="middle" font-size="15" font-weight="bold" fill="#01579b">INetworkable</text>
    <line x1="120" y1="120" x2="380" y2="120" stroke="#0288d1" stroke-width="1"/>
    <text x="132" y="138" font-size="12" fill="#212121">+ ip_address: Optional[str]</text>
    <text x="132" y="156" font-size="12" fill="#212121">+ is_connected: bool</text>
    <line x1="120" y1="165" x2="380" y2="165" stroke="#0288d1" stroke-width="1"/>
    <text x="132" y="183" font-size="12" fill="#212121">+ connect(ip_address: str): void</text>
    <text x="132" y="198" font-size="12" fill="#212121">+ disconnect(): void</text>
  </g>

  <!-- 2. Enum DeviceStatus -->
  <g filter="url(#shadow)">
    <rect x="600" y="70" width="200" height="115" rx="8" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
    <text x="700" y="93" text-anchor="middle" font-size="12" fill="#6a1b9a">&lt;&lt;enumeration&gt;&gt;</text>
    <text x="700" y="110" text-anchor="middle" font-size="15" font-weight="bold" fill="#4a148c">DeviceStatus</text>
    <line x1="600" y1="120" x2="800" y2="120" stroke="#7b1fa2" stroke-width="1"/>
    <text x="615" y="140" font-size="12" font-weight="bold" fill="#311b92">ACTIVE</text>
    <text x="615" y="158" font-size="12" font-weight="bold" fill="#311b92">UNDER_MAINTENANCE</text>
    <text x="615" y="176" font-size="12" font-weight="bold" fill="#311b92">RETIRED</text>
  </g>

  <!-- 3. Abstract Class Device -->
  <g filter="url(#shadow)">
    <rect x="540" y="250" width="320" height="245" rx="8" fill="#fff9c4" stroke="#fbc02d" stroke-width="2"/>
    <text x="700" y="273" text-anchor="middle" font-size="12" fill="#f57f17">&lt;&lt;abstract&gt;&gt;</text>
    <text x="700" y="291" text-anchor="middle" font-size="16" font-weight="bold" fill="#e65100">Device</text>
    <line x1="540" y1="300" x2="860" y2="300" stroke="#fbc02d" stroke-width="1"/>
    <text x="552" y="318" font-size="12" fill="#212121">- _device_id: str</text>
    <text x="552" y="336" font-size="12" fill="#212121">- _device_name: str</text>
    <text x="552" y="354" font-size="12" fill="#212121">- _year_of_usage: int</text>
    <text x="552" y="372" font-size="12" fill="#212121">- _purchase_price: float</text>
    <text x="552" y="390" font-size="12" fill="#212121">- _status: DeviceStatus</text>
    <text x="552" y="408" font-size="12" fill="#212121">+ device_id: str {read-only}</text>
    <text x="552" y="426" font-size="12" fill="#212121">+ age: int {derived}</text>
    <line x1="540" y1="435" x2="860" y2="435" stroke="#fbc02d" stroke-width="1"/>
    <text x="552" y="454" font-size="12" font-style="italic" font-weight="bold" fill="#bf360c">+ calculate_annual_maintenance_cost()*: float</text>
    <text x="552" y="474" font-size="12" fill="#212121">+ __str__(): str</text>
  </g>

  <!-- 4. Class LabRoom -->
  <g filter="url(#shadow)">
    <rect x="1040" y="250" width="330" height="245" rx="8" fill="#e8f5e9" stroke="#43a047" stroke-width="2"/>
    <text x="1205" y="285" text-anchor="middle" font-size="16" font-weight="bold" fill="#1b5e20">LabRoom</text>
    <line x1="1040" y1="300" x2="1370" y2="300" stroke="#43a047" stroke-width="1"/>
    <text x="1052" y="320" font-size="12" fill="#212121">+ room_id: str</text>
    <text x="1052" y="338" font-size="12" fill="#212121">+ room_name: str</text>
    <text x="1052" y="356" font-size="12" fill="#212121">+ capacity: int</text>
    <text x="1052" y="374" font-size="12" fill="#212121">- _devices: List[Device]</text>
    <line x1="1040" y1="385" x2="1370" y2="385" stroke="#43a047" stroke-width="1"/>
    <text x="1052" y="405" font-size="12" fill="#212121">+ add_device(device: Device): void</text>
    <text x="1052" y="423" font-size="12" fill="#212121">+ remove_device(device_id: str): bool</text>
    <text x="1052" y="441" font-size="12" fill="#212121">+ find_device(device_id: str): Optional[Device]</text>
    <text x="1052" y="459" font-size="12" fill="#212121">+ calculate_annual_maintenance_cost(): float</text>
    <text x="1052" y="477" font-size="12" fill="#212121">+ get_devices_requiring_maintenance(): List[Device]</text>
  </g>

  <!-- 5. Class Computer -->
  <g filter="url(#shadow)">
    <rect x="100" y="600" width="280" height="210" rx="8" fill="#e8eaf6" stroke="#3f51b5" stroke-width="2"/>
    <text x="240" y="630" text-anchor="middle" font-size="16" font-weight="bold" fill="#1a237e">Computer</text>
    <line x1="100" y1="645" x2="380" y2="645" stroke="#3f51b5" stroke-width="1"/>
    <text x="112" y="665" font-size="12" fill="#212121">+ ram_size_gb: int</text>
    <text x="112" y="683" font-size="12" fill="#212121">+ processor_type: str</text>
    <text x="112" y="701" font-size="12" fill="#212121">+ has_discrete_gpu: bool</text>
    <text x="112" y="719" font-size="12" fill="#212121">- _ip_address: Optional[str]</text>
    <text x="112" y="737" font-size="12" fill="#212121">- _is_connected: bool</text>
    <line x1="100" y1="748" x2="380" y2="748" stroke="#3f51b5" stroke-width="1"/>
    <text x="112" y="768" font-size="12" fill="#212121">+ calculate_annual_maintenance_cost(): float</text>
    <text x="112" y="786" font-size="12" fill="#212121">+ connect(ip_address: str): void</text>
    <text x="112" y="802" font-size="12" fill="#212121">+ disconnect(): void</text>
  </g>

  <!-- 6. Class Printer -->
  <g filter="url(#shadow)">
    <rect x="460" y="600" width="270" height="170" rx="8" fill="#e8eaf6" stroke="#3f51b5" stroke-width="2"/>
    <text x="595" y="630" text-anchor="middle" font-size="16" font-weight="bold" fill="#1a237e">Printer</text>
    <line x1="460" y1="645" x2="730" y2="645" stroke="#3f51b5" stroke-width="1"/>
    <text x="472" y="665" font-size="12" fill="#212121">+ printer_type: str</text>
    <text x="472" y="683" font-size="12" fill="#212121">+ pages_printed: int</text>
    <text x="472" y="701" font-size="12" fill="#212121">+ has_network_support: bool</text>
    <text x="472" y="719" font-size="12" fill="#212121">+ is_color: bool</text>
    <line x1="460" y1="730" x2="730" y2="730" stroke="#3f51b5" stroke-width="1"/>
    <text x="472" y="752" font-size="12" fill="#212121">+ calculate_annual_maintenance_cost(): float</text>
  </g>

  <!-- 7. Class NetworkPrinter -->
  <g filter="url(#shadow)">
    <rect x="460" y="860" width="270" height="150" rx="8" fill="#e1f5fe" stroke="#0288d1" stroke-width="2"/>
    <text x="595" y="888" text-anchor="middle" font-size="16" font-weight="bold" fill="#01579b">NetworkPrinter</text>
    <line x1="460" y1="900" x2="730" y2="900" stroke="#0288d1" stroke-width="1"/>
    <text x="472" y="922" font-size="12" fill="#212121">- _ip_address: Optional[str]</text>
    <text x="472" y="940" font-size="12" fill="#212121">- _is_connected: bool</text>
    <line x1="460" y1="952" x2="730" y2="952" stroke="#0288d1" stroke-width="1"/>
    <text x="472" y="974" font-size="12" fill="#212121">+ connect(ip_address: str): void</text>
    <text x="472" y="992" font-size="12" fill="#212121">+ disconnect(): void</text>
  </g>

  <!-- 8. Class Projector -->
  <g filter="url(#shadow)">
    <rect x="800" y="600" width="270" height="160" rx="8" fill="#e8eaf6" stroke="#3f51b5" stroke-width="2"/>
    <text x="935" y="630" text-anchor="middle" font-size="16" font-weight="bold" fill="#1a237e">Projector</text>
    <line x1="800" y1="645" x2="1070" y2="645" stroke="#3f51b5" stroke-width="1"/>
    <text x="812" y="667" font-size="12" fill="#212121">+ brightness_lumens: int</text>
    <text x="812" y="687" font-size="12" fill="#212121">+ lamp_hours_used: int</text>
    <line x1="800" y1="702" x2="1070" y2="702" stroke="#3f51b5" stroke-width="1"/>
    <text x="812" y="728" font-size="12" fill="#212121">+ calculate_annual_maintenance_cost(): float</text>
  </g>

</svg>
"""
    with open("class_diagram.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(" Đã tạo thành công file class_diagram.svg sắc nét!")

if __name__ == "__main__":
    generate_drawio()
    generate_svg()
