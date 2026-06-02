# Industrial Use Cases

ScrewVision is not only a detector. It is an inspection runtime for repetitive mechanical quality-control workflows.

## Core Factory Problems

### 1. Missing Screw Detection

Detect whether an expected screw, bolt, or fastener is absent from an assembly image.

**Value:** prevents incomplete assemblies from leaving the line.

### 2. Wrong Screw Type

Classify whether the visible fastener matches the expected type for the station.

Examples:

- Phillips vs hex
- silver vs black oxide
- short vs long
- countersunk vs pan head

**Value:** reduces mixed-part errors.

### 3. Damaged Head Inspection

Score visible wear or deformation on the screw head.

Possible signals:

- stripped slot
- rounded hex socket
- excessive scratches
- impact deformation
- corrosion

**Value:** flags parts likely to fail during service or rework.

### 4. Geometry and Morphology Analysis

Estimate visual features from image contours.

Metrics:

- bounding box
- aspect ratio
- contour area
- elongation
- head/body proportion
- orientation

**Value:** useful before custom AI weights exist.

### 5. Assembly Verification

Use a camera station to confirm that every expected fastener appears in the correct region.

Pipeline:

```txt
camera → detect → match expected zones → score → log → pass/review/fail
```

### 6. Packaging and Counting

Count fasteners before bagging, boxing, or shipping.

**Value:** prevents underfilled kits and inventory mismatch.

### 7. Rework Bench Assistant

Support technicians who inspect returned parts or failed assemblies.

Flow:

```txt
upload image → detect screw → inspect morphology → quality score → export evidence
```

## Inspection Results

ScrewVision should express output in simple operational states:

```txt
PASS
REVIEW
FAIL
```

A factory operator should not need to understand computer vision internals.

## Evidence Model

Every result should be explainable through observable data:

- detection confidence
- bounding box
- morphology metrics
- quality score
- inspection rule
- timestamp
- image reference

## Example Industrial Output

```json
{
  "station": "assembly-line-a3",
  "part_id": "M3x12_pan_head",
  "inspection_result": "REVIEW",
  "quality_score": 0.67,
  "reason": "visible head wear and low morphology confidence",
  "next_action": "manual inspection"
}
```

## Product Positioning

Use this language:

> Industrial machine vision runtime for screw recognition, quality scoring, and factory inspection workflows.

Avoid this language:

> AI that magically understands screws.

## Long-Term Vision

ScrewVision can evolve into a cybernetic factory inspection layer:

```txt
camera → vision runtime → quality score → telemetry → dashboard → robot/operator action
```
