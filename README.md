# Quantum Composer

A physics simulation framework implementing relativistic time dilation calculations based on quantum field density.

## Core Formula

$$\Delta \tau = \tau_0 \cdot \sqrt{1 - \frac{v^2}{c^2} - \frac{2GM}{r \cdot c^2}} = f(\text{Densité de la Toile Quantique})$$

### Components

- **$\Delta \tau$**: Proper time experienced by observer
- **$\tau_0$**: Coordinate time interval
- **$v$**: Velocity of observer
- **$c$**: Speed of light (299,792,458 m/s)
- **$G$**: Gravitational constant (6.674 × 10⁻¹¹ m³/(kg·s²))
- **$M$**: Mass of gravitational source
- **$r$**: Distance from gravitational source
- **Densité de la Toile Quantique**: Quantum web density — a custom parameter modulating the overall time dilation effect

## Physics Background

This combines:
1. **Special Relativity**: Velocity-based time dilation
2. **General Relativity**: Gravitational time dilation
3. **Quantum Field Effects**: Density-dependent modulation

## Structure

- `time_dilation.py` — Core calculations
- `quantum_density.py` — Quantum web density models
- `examples/` — Usage demonstrations
