from __future__ import annotations


ROADMAP = [
    {
        "phase": 0,
        "name": "Genesis Runtime",
        "goal": "Create the foundational screw recognition pipeline.",
        "architecture": "Physics -> Vision",
        "features": [
            "Camera, USB industrial camera, RTSP, and image upload runtime",
            "YOLOv8 detection with bounding boxes, multi-object support, and confidence scoring",
            "Base classification for screws, bolts, nuts, and washers",
        ],
        "deliverables": [
            {"component": "Detection API", "status": "in_progress"},
            {"component": "Runtime Engine", "status": "in_progress"},
            {"component": "Web Dashboard", "status": "in_progress"},
            {"component": "Dataset Pipeline", "status": "planned"},
            {"component": "Docker Runtime", "status": "in_progress"},
        ],
    },
    {
        "phase": 1,
        "name": "Semantic Morphology Engine",
        "goal": "Move beyond labels into morphology understanding.",
        "architecture": "Vision -> Semantics",
        "features": [
            "Head topology, threading geometry, shaft proportions, contour signatures, and symmetry patterns",
            "Length, diameter, thread pitch, head depth, and angular geometry estimation",
            "Contour, edge-map, thread, defect heatmap, and segmentation overlays",
        ],
        "deliverables": [
            {"component": "Morphology Runtime", "status": "in_progress"},
            {"component": "Segmentation Engine", "status": "planned"},
            {"component": "Measurement System", "status": "planned"},
            {"component": "Calibration Runtime", "status": "planned"},
        ],
    },
    {
        "phase": 2,
        "name": "Industrial Intelligence Layer",
        "goal": "Understand industrial context and hardware ecosystems.",
        "architecture": "Semantics -> Industrial Context",
        "features": [
            "Compatible hardware, missing components, assembly relationships, and structural dependencies",
            "Hardware knowledge graph: Screw -> Washer -> Plate -> Motor -> Assembly",
            "Automatic counting, stock estimation, warehouse indexing, defect reports, and hardware analytics",
        ],
        "deliverables": [
            {"component": "Inventory Engine", "status": "planned"},
            {"component": "Knowledge Graph", "status": "planned"},
            {"component": "Compatibility Runtime", "status": "planned"},
            {"component": "Industrial Analytics", "status": "planned"},
        ],
    },
    {
        "phase": 3,
        "name": "Edge AI Runtime",
        "goal": "Deploy industrial intelligence directly on edge devices.",
        "architecture": "Industrial Context -> Edge Intelligence",
        "features": [
            "Raspberry Pi, NVIDIA Jetson, industrial PCs, ARM systems, drones, and robotics platforms",
            "TensorRT, ONNX Runtime, quantization, and low-latency pipelines",
            "Offline operation, low-power mode, edge telemetry, and distributed inference",
        ],
        "deliverables": [
            {"component": "Edge Runtime", "status": "planned"},
            {"component": "TensorRT Pipeline", "status": "planned"},
            {"component": "ARM Optimization", "status": "planned"},
            {"component": "Edge Dashboard", "status": "planned"},
        ],
    },
    {
        "phase": 4,
        "name": "Robotics Integration",
        "goal": "Connect ScrewVision to robotic systems.",
        "architecture": "Edge Intelligence -> Robotics",
        "features": [
            "Object localization, grasp-point prediction, hardware sorting, and pick-and-place systems",
            "Missing screw identification, replacement suggestions, guided assembly, and installation verification",
            "ROS2, robotic arms, PLC systems, conveyors, and industrial automation integration",
        ],
        "deliverables": [
            {"component": "ROS2 Connector", "status": "planned"},
            {"component": "Grasp Engine", "status": "planned"},
            {"component": "Sorting Runtime", "status": "planned"},
            {"component": "Repair Assistant", "status": "planned"},
        ],
    },
    {
        "phase": 5,
        "name": "Mechanical Cognition Engine",
        "goal": "Create a runtime capable of reasoning about mechanical systems.",
        "architecture": "Robotics -> Mechanical Cognition",
        "features": [
            "Structural intent, load distribution, failure probability, assembly logic, and maintenance risk",
            "Semantic assemblies, hardware maps, industrial simulations, and maintenance timelines",
        ],
        "deliverables": [
            {"component": "Reasoning Engine", "status": "planned"},
            {"component": "Mechanical Twin Runtime", "status": "planned"},
            {"component": "Failure Prediction", "status": "planned"},
            {"component": "Industrial AI Core", "status": "planned"},
        ],
    },
    {
        "phase": 6,
        "name": "Cybernetic Factory Runtime",
        "goal": "Transform ScrewVision into a distributed industrial cognition platform.",
        "architecture": "Mechanical Cognition -> Autonomy",
        "features": [
            "Multi-camera systems, real-time telemetry, distributed AI nodes, and industrial event streaming",
            "Assembly-line monitoring, defect propagation, operational entropy, and production health",
            "Failure, shortage, structural-instability, and maintenance-window prediction",
        ],
        "deliverables": [
            {"component": "Factory Runtime", "status": "planned"},
            {"component": "Telemetry Mesh", "status": "planned"},
            {"component": "Predictive AI", "status": "planned"},
            {"component": "Cybernetic Dashboard", "status": "planned"},
        ],
    },
]


STACK_EVOLUTION = {
    "detection": "YOLOv8",
    "segmentation": "SAM / YOLO-Seg",
    "geometry": "OpenCV",
    "reasoning": "Graph Neural Networks",
    "runtime": "FastAPI",
    "dashboard": "React + Tailwind",
    "streaming": "WebSockets",
    "robotics": "ROS2",
    "edge": "TensorRT",
    "telemetry": "Kafka / Redis Streams",
}
