# WALL-B Robot Assembly Guide

This guide provides step-by-step instructions for assembling your WALL-B biped robot. The assembly process is divided into logical sections: tools, parts preparation, and each major body section.

## Table of Contents

- [Required Tools](#required-tools)
- [3D Printed Parts Checklist](#3d-printed-parts-checklist)
- [Hardware and Fasteners](#hardware-and-fasteners)
- [Leg Assembly](#leg-assembly)
- [Body/Torso Assembly](#bodytorso-assembly)
- [Arm Assembly](#arm-assembly)
- [Head Assembly](#head-assembly)
- [Wiring](#wiring)
- [Final Assembly](#final-assembly)

---

## Required Tools

### Essential Tools

| Tool | Purpose | Notes |
| --- | --- | --- |
| Phillips Screwdriver Set | Assembling frame and servo mounts | Sizes: PH0, PH1, PH2 |
| Hex Key Set (Metric) | Securing set screws and bolts | Sizes: 1.5mm, 2mm, 2.5mm, 3mm, 4mm |
| Soldering Iron | PCB connections and wire joints | 60W recommended, with fine tip |
| Wire Strippers | Preparing servo and power wires | 20-30 AWG range |
| Multimeter | Testing connections and voltages | With continuity tester |
| Pliers Set | Holding small parts and bending | Needle-nose and standard |
| Calipers | Measuring servo horns and clearances | Digital preferred |
| Heat Gun | Shrink tubing and cable management | Or lighter as alternative |
|檀 |檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀檀 | --- | --- |
| Hobby Knife | Trimming 3D printed parts | With extra blades |
| 3D Printer | Printing structural parts | 0.2mm layer height recommended |

### Optional Tools

| Tool | Purpose | Notes |
| --- | --- | --- |
| Third Hand | Holding parts during assembly | With magnifying glass |
| Dremel Tool | Grinding and finishing parts | With sanding attachments |
| Hotend Cleaner | Removing 3D print imperfections | Or hobby knife |

---

## 3D Printed Parts Checklist

All STL files are located in the `hardware/cad/` directory. Print these parts before starting assembly.

### Leg Parts (per leg - print 2x)

| Part File | Quantity | Material | Notes |
| --- | --- | --- | --- |
| hip_bracket.stl | 1 | PETG or ABS | High-stress part |
| thigh_link.stl | 1 | PETG or ABS | Structural member |
| knee_joint.stl | 1 | PETG or ABS | Load-bearing joint |
| shin_link.stl | 1 | PETG or ABS | Lower leg structure |
| ankle_bracket.stl | 1 | PETG or ABS | Ankle joint mount |
| foot_plate.stl | 1 | PETG | Contact surface |

### Torso Parts

| Part File | Quantity | Material | Notes |
| --- | --- | --- | --- |
| torso_frame_top.stl | 1 | PETG or ABS | Upper body frame |
| torso_frame_bottom.stl | 1 | PETG or ABS | Lower body frame |
| torso_side_panel_left.stl | 1 | PETG | Left body panel |
| torso_side_panel_right.stl | 1 | PETG | Right body panel |
| hip_connector.stl | 2 | PETG | Hip joint connection |

### Arm Parts (per arm - print 2x)

| Part File | Quantity | Material | Notes |
| --- | --- | --- | --- |
| shoulder_bracket.stl | 1 | PETG | Shoulder joint mount |
| upper_arm.stl | 1 | PETG | Upper arm link |
| elbow_joint.stl | 1 | PETG | Elbow joint |
| forearm.stl | 1 | PETG | Lower arm structure |
| hand_mount.stl | 1 | PETG | Hand attachment |

### Head Parts

| Part File | Quantity | Material | Notes |
| --- | --- | --- | --- |
| head_base.stl | 1 | PETG | Main head structure |
| head_front.stl | 1 | PETG | Face plate |
| neck_joint.stl | 2 | PETG | Neck joints |
| neck_column.stl | 1 | PETG | Neck connector |
| camera_mount.stl | 1 | PETG | Camera holder |

### Recommended Print Settings

| Setting | Value |
| --- | --- |
| Layer Height | 0.2mm |
| Infill | 40-60% |
| Walls | 3-4 perimeters |
| Material | PETG (recommended) or ABS |
| Bed Temperature | 80-85°C (PETG) |
| Nozzle Temperature | 230-250°C (PETG) |
| Build Plate Adhesion | Brim or Raft |

---

## Hardware and Fasteners

### Fasteners Required

| Type | Size | Quantity | Purpose |
| --- | --- | --- | --- |
| M3 Socket Head Screw | 6mm | 40 | General mounting |
| M3 Socket Head Screw | 8mm | 30 | Servo mounting |
| M3 Socket Head Screw | 10mm | 20 | Bracket mounting |
| M3 Socket Head Screw | 12mm | 15 | Joint assembly |
| M3 Hex Nut | - | 35 | Nut inserts |
| M3 Flat Washer | - | 25 | Distribution |
| M2.5 Socket Head Screw | 6mm | 20 | PCB mounting |
| M4 Socket Head Screw | 10mm | 8 | Major joints |
| M4 Hex Nut | - | 8 | M4 inserts |
| M2 Self-Tapping Screw | 6mm | 12 | Cable clips |

### Bearings Required

| Type | Quantity | Purpose |
| --- | --- | --- |
| 625ZZ Bearing | 8 | Leg joints |
| 688ZZ Bearing | 4 | Ankle joints |
| 683ZZ Bearing | 4 | Hip joints |

### Servos Required

| Type | Quantity | Location |
| --- | --- | --- |
| SG5010 Digital Servo | 12 | Legs (6 per leg) |
| MG92B High-Torque Servo | 8 | Arms and Neck |
| SG90 Micro Servo | 2 | Head pan-tilt |

---

## Leg Assembly

Assembly Time: Approximately 2-3 hours per leg

### Step 1: Hip Joint Assembly

1. **Install bearings in hip bracket:**
   - Press two 683ZZ bearings into the hip bracket's bearing seats
   - Ensure bearings are seated flush and rotate freely
   - Apply a small amount of lubricant if needed

2. **Attach hip servo:**
   - Mount SG5010 servo to the hip bracket using M3x8mm screws
   - Align servo horn with the bearing center
   - Torque screws to 0.3-0.4 Nm

3. **Connect thigh link:**
   - Attach thigh link to hip bracket using M4x10mm screws
   - Insert bearing between joint surfaces
   - Verify smooth rotation through full range

### Step 2: Knee Joint Assembly

1. **Install knee bearing:**
   - Press 625ZZ bearing into knee joint part
   - Apply pressure to outer race only

2. **Attach knee servo:**
   - Mount SG5010 servo to thigh link lower mount
   - Connect knee joint linkage to servo horn
   - Secure with servo horn screw

3. **Connect shin link:**
   - Attach shin link to knee joint using M3x12mm screws
   - Insert bearing between joint surfaces
   - Check for binding and adjust if necessary

### Step 3: Ankle Joint Assembly

1. **Install ankle bearings:**
   - Press 688ZZ bearings into ankle bracket
   - Two bearings per ankle (medial and lateral)

2. **Attach ankle servo:**
   - Mount SG5010 servo to shin link lower mount
   - Connect ankle bracket to servo horn

3. **Attach foot plate:**
   - Mount foot plate to ankle bracket using M3x6mm screws
   - Ensure foot is perpendicular to leg when servo is centered

### Step 4: Leg Verification

1. **Power test (without full load):**
   - Connect leg servos to Arduino Mega one at a time
   - Verify each servo responds to commands
   - Check for any unusual sounds or binding

2. **Range of motion test:**
   - Manually move leg through full range of each joint
   - Verify no interference between parts
   - Adjust cable routing if needed

---

## Body/Torso Assembly

Assembly Time: Approximately 2 hours

### Step 1: Frame Assembly

1. **Connect torso frames:**
   - Align torso frame top and bottom using alignment pins
   - Secure with M3x10mm screws through side mounting holes
   - Install hex nuts in pre-molded inserts

2. **Attach hip connectors:**
   - Mount hip connectors to torso frame bottom
   - Use M3x8mm screws and verify alignment
   - These will connect to leg hip brackets

3. **Install side panels:**
   - Attach left and right side panels to frame
   - Use M3x6mm screws
   - Leave slight gap for cable routing

### Step 2: Electronics Mounting

1. **Arduino Mega mount:**
   - Install Arduino Mega 2560 in designated position
   - Use M2.5x6mm screws through mounting holes
   - Connect to power distribution board

2. **Raspberry Pi 5 mount:**
   - Install Raspberry Pi 5 using standoffs
   - Connect GPIO header to Arduino (for serial communication)
   - Attach CSI camera cable

3. **Power distribution:**
   - Mount XL4015 buck converters
   - Install power switch
   - Connect battery input wires

### Step 3: Internal Wiring Preparation

1. **Route servo cables:**
   - Run servo cables through cable management channels
   - Use zip ties to secure cables
   - Maintain service loops for maintenance access

2. **Install MPU6050:**
   - Mount IMU sensor in center of torso
   - Align with robot's forward direction
   - Connect to Arduino I2C pins (SDA/SCL)

---

## Arm Assembly

Assembly Time: Approximately 1.5 hours per arm

### Step 1: Shoulder Assembly

1. **Attach shoulder bracket:**
   - Mount shoulder bracket to torso side panel
   - Use M3x10mm screws
   - Verify bracket is level and perpendicular

2. **Install shoulder servo:**
   - Mount MG92B servo to shoulder bracket
   - Connect servo horn to upper arm link
   - Secure with servo horn screw

### Step 2: Upper Arm and Elbow

1. **Connect upper arm:**
   - Attach upper arm link to shoulder servo horn
   - Install bearing at elbow pivot point
   - Verify rotation range

2. **Attach elbow servo:**
   - Mount elbow servo to upper arm
   - Connect forearm to elbow servo horn
   - Check for interference with body

### Step 3: Hand Mount

1. **Attach hand mount:**
   - Mount hand mount to forearm
   - Install any end-effector hardware
   - Leave space for finger servos (optional)

---

## Head Assembly

Assembly Time: Approximately 1 hour

### Step 1: Neck Assembly

1. **Install neck joints:**
   - Mount two neck joints to torso frame top
   - Use M3x8mm screws
   - Insert bearings in joint pivots

2. **Connect neck column:**
   - Attach neck column between joints
   - Install neck servo for tilt motion
   - Verify head can tilt forward and back

### Step 2: Head Base Assembly

1. **Mount head servo:**
   - Install pan servo in head base
   - Connect to neck column
   - Test rotation through full range

2. **Attach head pan-tilt:**
   - Mount SG90 servos for camera pan-tilt
   - Install camera mount to servo horns
   - Verify camera field of view

### Step 3: Final Head Components

1. **Install Neopixel Jewel:**
   - Mount Adafruit Neopixel Jewel in eye position
   - Connect data and power wires
   - Route wires through head cable channel

2. **Attach head front:**
   - Secure head front panel to head base
   - Cut openings for eyes and camera
   - Optional: Add transparent eye covers

---

## Wiring

### Power Distribution

| Component | Voltage | Connection |
| --- | --- | --- |
| Raspberry Pi 5 | 5V | XL4015 Buck from 12V |
| Arduino Mega | 7-12V | Direct from battery or Buck |
| Servos | 6-7.4V | XL4015 Buck from 12V |
| IMX500 Camera | 5V | From Pi USB-C |
| Neopixel | 5V | From Pi GPIO or Buck |

### Safety Precautions

1. **Before wiring:**
   - Disconnect all power sources
   - Verify all wire gauges are appropriate
   - Use proper connectors and insulation

2. **Power-on checklist:**
   - Check for shorts with multimeter
   - Verify voltage levels before connecting loads
   - Monitor for unusual heat or sounds

### Recommended Wire Colors

| Function | Color | Notes |
| --- | --- | --- |
| 12V Battery Positive | Red | Heavy gauge |
| 12V Battery Negative | Black | Heavy gauge |
| 5V Logic | Red | 22 AWG |
| Ground (logic) | Black | 22 AWG |
| Servo Signal | White or Yellow | 22 AWG |
| I2C (SDA/SCL) | Green/Blue | 22 AWG |

---

## Final Assembly

### Step 1: Leg Attachment

1. **Connect legs to torso:**
   - Align hip brackets with hip connectors
   - Insert M4 pivot screws through joints
   - Install bearing and secure with locking nut

2. **Connect servo cables:**
   - Route leg servo cables through torso
   - Connect to Arduino Mega PWM pins
   - Label each cable for identification

### Step 2: Arm Attachment

1. **Mount arms to shoulders:**
   - Align shoulder brackets with torso mounts
   - Secure with M3x10mm screws
   - Connect arm servo cables

### Step 3: Head Attachment

1. **Connect neck:**
   - Route neck and head cables through neck column
   - Connect to Arduino and Raspberry Pi
   - Attach head assembly to neck joints

### Step 4: Final Checks

1. **Mechanical check:**
   - Verify all screws are tightened
   - Check for any loose parts
   - Ensure full range of motion without interference

2. **Electrical check:**
   - Verify all connections are secure
   - Test power-on sequence
   - Check servo responses

---

## Next Steps

After completing assembly, proceed to the [Electronics Setup Guide](/docs/electronics.md) for detailed wiring information, then the [Software Setup Guide](/docs/software.md) to install the required software.

For troubleshooting common issues, see the [Troubleshooting Guide](/docs/troubleshooting.md).

---

## Support

If you encounter any issues during assembly:

1. Check the [Troubleshooting Guide](/docs/troubleshooting.md) for common solutions
2. Search existing [GitHub Issues](https://github.com/faxxxan/WALL-B/issues) for similar problems
3. Create a new issue with detailed photos and description
