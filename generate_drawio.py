# /****************/
# 202418872
# Nguyễn Minh Đức
# /****************/

import xml.etree.ElementTree as ET

def create_drawio_xml():
    mxfile = ET.Element("mxfile", {
        "host": "app.diagrams.net",
        "agent": "Mozilla/5.0",
        "version": "24.0.0",
        "type": "device"
    })
    diagram = ET.SubElement(mxfile, "diagram", {
        "id": "OOP_Lab05_ClassDiagram",
        "name": "Class Diagram - Lab W05"
    })
    model = ET.SubElement(diagram, "mxGraphModel", {
        "dx": "1400",
        "dy": "900",
        "grid": "1",
        "gridSize": "10",
        "guides": "1",
        "tooltips": "1",
        "connect": "1",
        "arrows": "1",
        "fold": "1",
        "page": "1",
        "pageScale": "1",
        "pageWidth": "1654",
        "pageHeight": "1169",
        "math": "0",
        "shadow": "0"
    })
    root = ET.SubElement(model, "root")
    
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    # Helper function to create vertex (class box)
    def add_class(cid, label, x, y, w, h, fill="#dae8fc", stroke="#6c8ebf"):
        style = (
            f"swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;"
            f"horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;"
            f"resizeLast=0;collapsible=0;marginBottom=0;html=1;fillColor={fill};strokeColor={stroke};rounded=1;"
        )
        cell = ET.SubElement(root, "mxCell", {
            "id": cid,
            "value": label,
            "style": style,
            "vertex": "1",
            "parent": "1"
        })
        geo = ET.SubElement(cell, "mxGeometry", {
            "x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"
        })
        return cell

    def add_section(sid, pid, text, h=60, is_method=False):
        style = (
            "text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;"
            "spacingLeft=6;spacingRight=6;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;html=1;"
        )
        if is_method:
            style += "fontColor=#1c2833;"
        cell = ET.SubElement(root, "mxCell", {
            "id": sid,
            "value": text,
            "style": style,
            "vertex": "1",
            "parent": pid
        })
        ET.SubElement(cell, "mxGeometry", {
            "y": "30", "width": "100%", "height": str(h), "as": "geometry"
        })
        return cell

    def add_separator(sid, pid):
        style = "line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=inherit;"
        cell = ET.SubElement(root, "mxCell", {
            "id": sid,
            "value": "",
            "style": style,
            "vertex": "1",
            "parent": pid
        })
        ET.SubElement(cell, "mxGeometry", {
            "y": "30", "width": "100%", "height": "8", "as": "geometry"
        })

    def add_edge(eid, source, target, rel_type="inheritance", label=""):
        # Rel types: inheritance, realization, aggregation, association
        if rel_type == "inheritance":
            style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=0;strokeWidth=1.5;strokeColor=#000000;"
        elif rel_type == "realization":
            style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;endArrow=block;endFill=0;strokeWidth=1.5;strokeColor=#0288D1;"
        elif rel_type == "aggregation":
            style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;startArrow=diamond;startFill=0;endArrow=none;strokeWidth=1.5;strokeColor=#2E7D32;"
        elif rel_type == "association":
            style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=open;endFill=0;strokeWidth=1.5;strokeColor=#616161;"
        else:
            style = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#000000;"

        cell = ET.SubElement(root, "mxCell", {
            "id": eid,
            "value": label,
            "style": style,
            "edge": "1",
            "parent": "1",
            "source": source,
            "target": target
        })
        ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
        return cell

    # 1. Interface INetworkable
    add_class("c_net", "&lt;&lt;interface&gt;&gt;&lt;br/&gt;&lt;b&gt;INetworkable&lt;/b&gt;", 180, 50, 260, 150, fill="#e1f5fe", stroke="#0288d1")
    add_section("sec_net_props", "c_net", "+ ip_address: Optional[str]&lt;br/&gt;+ is_connected: bool", 45)
    add_separator("sep_net", "c_net")
    add_section("sec_net_meths", "c_net", "+ connect(ip_address: str): void&lt;br/&gt;+ disconnect(): void", 45, True)

    # 2. Enum DeviceStatus
    add_class("c_status", "&lt;&lt;enumeration&gt;&gt;&lt;br/&gt;&lt;b&gt;DeviceStatus&lt;/b&gt;", 960, 50, 200, 110, fill="#f3e5f5", stroke="#7b1fa2")
    add_section("sec_status_vals", "c_status", "ACTIVE&lt;br/&gt;UNDER_MAINTENANCE&lt;br/&gt;RETIRED", 60)

    # 3. Abstract Class Device
    add_class("c_dev", "&lt;&lt;abstract&gt;&gt;&lt;br/&gt;&lt;b&gt;Device&lt;/b&gt;", 560, 230, 320, 290, fill="#fff2cc", stroke="#d6b656")
    add_section("sec_dev_props", "c_dev", 
        "- _device_id: str&lt;br/&gt;"
        "- _device_name: str&lt;br/&gt;"
        "- _year_of_usage: int&lt;br/&gt;"
        "- _purchase_price: float&lt;br/&gt;"
        "- _status: DeviceStatus&lt;br/&gt;"
        "+ device_id: str {read-only}&lt;br/&gt;"
        "+ age: int {derived}", 125)
    add_separator("sep_dev", "c_dev")
    add_section("sec_dev_meths", "c_dev",
        "+ calculate_annual_maintenance_cost()*: float&lt;br/&gt;"
        "+ __str__(): str", 55, True)

    # 4. Class LabRoom
    add_class("c_room", "&lt;b&gt;LabRoom&lt;/b&gt;", 1040, 250, 300, 250, fill="#d5e8d4", stroke="#82b366")
    add_section("sec_room_props", "c_room",
        "+ room_id: str&lt;br/&gt;"
        "+ room_name: str&lt;br/&gt;"
        "+ capacity: int&lt;br/&gt;"
        "- _devices: List[Device]", 75)
    add_separator("sep_room", "c_room")
    add_section("sec_room_meths", "c_room",
        "+ add_device(device: Device): void&lt;br/&gt;"
        "+ remove_device(device_id: str): bool&lt;br/&gt;"
        "+ find_device(device_id: str): Optional[Device]&lt;br/&gt;"
        "+ calculate_annual_maintenance_cost(): float&lt;br/&gt;"
        "+ get_devices_requiring_maintenance(): List[Device]", 105, True)

    # 5. Class Computer
    add_class("c_pc", "&lt;b&gt;Computer&lt;/b&gt;", 120, 620, 290, 210, fill="#dae8fc", stroke="#6c8ebf")
    add_section("sec_pc_props", "c_pc",
        "+ ram_size_gb: int&lt;br/&gt;"
        "+ processor_type: str&lt;br/&gt;"
        "+ has_discrete_gpu: bool&lt;br/&gt;"
        "- _ip_address: Optional[str]&lt;br/&gt;"
        "- _is_connected: bool", 85)
    add_separator("sep_pc", "c_pc")
    add_section("sec_pc_meths", "c_pc",
        "+ calculate_annual_maintenance_cost(): float&lt;br/&gt;"
        "+ connect(ip_address: str): void&lt;br/&gt;"
        "+ disconnect(): void", 65, True)

    # 6. Class Printer
    add_class("c_pr", "&lt;b&gt;Printer&lt;/b&gt;", 480, 620, 270, 170, fill="#dae8fc", stroke="#6c8ebf")
    add_section("sec_pr_props", "c_pr",
        "+ printer_type: str&lt;br/&gt;"
        "+ pages_printed: int&lt;br/&gt;"
        "+ has_network_support: bool&lt;br/&gt;"
        "+ is_color: bool", 75)
    add_separator("sep_pr", "c_pr")
    add_section("sec_pr_meths", "c_pr",
        "+ calculate_annual_maintenance_cost(): float", 35, True)

    # 7. Class NetworkPrinter
    add_class("c_net_pr", "&lt;b&gt;NetworkPrinter&lt;/b&gt;", 480, 870, 270, 160, fill="#e1f5fe", stroke="#0288d1")
    add_section("sec_npr_props", "c_net_pr",
        "- _ip_address: Optional[str]&lt;br/&gt;"
        "- _is_connected: bool", 45)
    add_separator("sep_npr", "c_net_pr")
    add_section("sec_npr_meths", "c_net_pr",
        "+ connect(ip_address: str): void&lt;br/&gt;"
        "+ disconnect(): void", 45, True)

    # 8. Class Projector
    add_class("c_pj", "&lt;b&gt;Projector&lt;/b&gt;", 820, 620, 270, 160, fill="#dae8fc", stroke="#6c8ebf")
    add_section("sec_pj_props", "c_pj",
        "+ brightness_lumens: int&lt;br/&gt;"
        "+ lamp_hours_used: int", 45)
    add_separator("sep_pj", "c_pj")
    add_section("sec_pj_meths", "c_pj",
        "+ calculate_annual_maintenance_cost(): float", 35, True)

    # Relationships (Edges)
    # Computer inherits Device
    add_edge("e_pc_dev", "c_pc", "c_dev", "inheritance")
    # Printer inherits Device
    add_edge("e_pr_dev", "c_pr", "c_dev", "inheritance")
    # Projector inherits Device
    add_edge("e_pj_dev", "c_pj", "c_dev", "inheritance")
    # NetworkPrinter inherits Printer
    add_edge("e_npr_pr", "c_net_pr", "c_pr", "inheritance")

    # Realization: Computer implements INetworkable
    add_edge("e_pc_net", "c_pc", "c_net", "realization")
    # Realization: NetworkPrinter implements INetworkable
    add_edge("e_npr_net", "c_net_pr", "c_net", "realization")

    # Aggregation: LabRoom aggregates Device
    add_edge("e_room_dev", "c_room", "c_dev", "aggregation", label="1       * (contains)")

    # Association: Device uses DeviceStatus
    add_edge("e_dev_status", "c_dev", "c_status", "association", label="uses")

    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ", level=0)
    tree.write("class_diagram.drawio", encoding="utf-8", xml_declaration=True)
    print(" Da tao thanh cong file class_diagram.drawio")

if __name__ == "__main__":
    create_drawio_xml()
