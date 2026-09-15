"""
Quantum Composer: Time Dilation Calculator
Implements: Δτ = τ₀ · √(1 - v²/c² - 2GM/rc²)
"""

import math
from dataclasses import dataclass
from typing import Tuple

# Physical Constants (SI units)
SPEED_OF_LIGHT = 299_792_458  # m/s
GRAVITATIONAL_CONSTANT = 6.674e-11  # m³/(kg·s²)
PHOTON_VELOCITY = SPEED_OF_LIGHT  # m/s


@dataclass
class RelativisticObject:
    """Represents an object in spacetime with relativistic properties."""
    velocity: float  # m/s
    mass_source: float  # kg (gravitational source mass)
    distance_from_source: float  # m
    coordinate_time: float  # seconds (τ₀)
    
    def validate(self) -> bool:
        """Validate physical parameters."""
        if self.velocity > SPEED_OF_LIGHT:
            raise ValueError(f"Velocity {self.velocity} exceeds speed of light")
        if self.distance_from_source <= 0:
            raise ValueError("Distance must be positive")
        if self.coordinate_time < 0:
            raise ValueError("Coordinate time cannot be negative")
        return True


class TimeDilation:
    """Calculates proper time (Δτ) using relativistic factors."""
    
    @staticmethod
    def einstein_factor(velocity: float) -> float:
        """
        Calculate Special Relativity factor: √(1 - v²/c²)
        
        Args:
            velocity: Velocity in m/s
            
        Returns:
            Einstein factor (1.0 for stationary, approaches 0 as v→c)
        """
        if velocity > SPEED_OF_LIGHT:
            raise ValueError(f"Velocity exceeds c: {velocity}")
        
        v_squared_over_c_squared = (velocity / SPEED_OF_LIGHT) ** 2
        return math.sqrt(1 - v_squared_over_c_squared)
    
    @staticmethod
    def schwarzschild_factor(mass_source: float, distance: float) -> float:
        """
        Calculate General Relativity factor: √(1 - 2GM/rc²)
        
        Args:
            mass_source: Mass of gravitational source in kg
            distance: Distance from source in m
            
        Returns:
            Schwarzschild factor (represents gravitational time dilation)
        """
        if distance <= 0:
            raise ValueError("Distance must be positive")
        
        c_squared = SPEED_OF_LIGHT ** 2
        schwarzschild_radius_term = (2 * GRAVITATIONAL_CONSTANT * mass_source) / (distance * c_squared)
        
        if schwarzschild_radius_term >= 1:
            raise ValueError(f"Inside event horizon: 2GM/rc² = {schwarzschild_radius_term}")
        
        return schwarzschild_radius_term
    
    @staticmethod
    def combined_time_dilation(
        coordinate_time: float,
        velocity: float,
        mass_source: float,
        distance: float
    ) -> float:
        """
        Calculate proper time with both relativistic effects:
        Δτ = τ₀ · √(1 - v²/c² - 2GM/rc²)
        
        Args:
            coordinate_time: Coordinate time interval τ₀ in seconds
            velocity: Velocity v in m/s
            mass_source: Gravitational source mass M in kg
            distance: Distance from source r in m
            
        Returns:
            Proper time Δτ in seconds
        """
        c_squared = SPEED_OF_LIGHT ** 2
        
        # Special Relativity term
        sr_term = (velocity / SPEED_OF_LIGHT) ** 2
        
        # General Relativity term
        gr_term = (2 * GRAVITATIONAL_CONSTANT * mass_source) / (distance * c_squared)
        
        combined_term = 1 - sr_term - gr_term
        
        if combined_term < 0:
            raise ValueError(
                f"Cannot calculate time dilation: combined term is negative ({combined_term}). "
                f"Object is in extreme spacetime curvature."
            )
        
        proper_time = coordinate_time * math.sqrt(combined_term)
        return proper_time
    
    @staticmethod
    def photon_case() -> Tuple[float, str]:
        """
        Special case: Photon traveling at light speed.
        For a photon: v = c, so Δτ = 0
        
        Returns:
            Tuple of (proper_time, description)
        """
        # For photon: v = c makes v²/c² = 1
        # The SR term becomes 1, so 1 - 1 = 0 before GR term
        proper_time = 0.0
        description = (
            "For a photon (v = c): Δτ = 0\n"
            "Time does not exist for the photon.\n"
            "From emission to absorption: instantaneous in the photon's frame."
        )
        return proper_time, description


class PhysicsValidator:
    """Validates physical scenarios against known limits."""
    
    @staticmethod
    def schwarzschild_radius(mass: float) -> float:
        """Calculate Schwarzschild radius (event horizon) for given mass."""
        c_squared = SPEED_OF_LIGHT ** 2
        return (2 * GRAVITATIONAL_CONSTANT * mass) / c_squared
    
    @staticmethod
    def is_inside_event_horizon(mass: float, distance: float) -> bool:
        """Check if a distance is inside the event horizon."""
        rs = PhysicsValidator.schwarzschild_radius(mass)
        return distance < rs
    
    @staticmethod
    def gravitational_time_dilation_at_surface(mass: float) -> float:
        """Calculate time dilation factor at surface of massive object."""
        radius = PhysicsValidator.schwarzschild_radius(mass)
        # At surface, distance ≈ 2*Rs for rough approximation
        distance = radius * 3  # Safe distance
        gr_factor = TimeDilation.schwarzschild_factor(mass, distance)
        return 1 - gr_factor


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("QUANTUM COMPOSER: Time Dilation Calculations")
    print("=" * 70)
    
    # Example 1: Stationary observer at Earth's surface
    print("\n[EXAMPLE 1] Observer at Earth's surface (stationary)")
    earth_mass = 5.972e24  # kg
    earth_radius = 6.371e6  # m
    tau_0 = 1.0  # 1 second
    
    dt_earth = TimeDilation.combined_time_dilation(
        coordinate_time=tau_0,
        velocity=0,  # stationary
        mass_source=earth_mass,
        distance=earth_radius
    )
    print(f"τ₀ = {tau_0} s")
    print(f"Δτ = {dt_earth:.15f} s")
    print(f"Time dilation factor: {dt_earth / tau_0:.12e}")
    
    # Example 2: Near a neutron star
    print("\n[EXAMPLE 2] Observer near neutron star surface")
    neutron_star_mass = 2.8e30  # kg (~1.4 solar masses)
    neutron_star_radius = 10_000  # m (10 km)
    
    dt_neutron = TimeDilation.combined_time_dilation(
        coordinate_time=tau_0,
        velocity=0,
        mass_source=neutron_star_mass,
        distance=neutron_star_radius
    )
    print(f"Neutron star mass: {neutron_star_mass:.2e} kg")
    print(f"Distance from center: {neutron_star_radius} m")
    print(f"Δτ = {dt_neutron:.15f} s")
    print(f"Time dilation factor: {dt_neutron / tau_0:.6f}")
    print(f"Time runs {(1 - dt_neutron/tau_0)*100:.2f}% slower")
    
    # Example 3: Photon case
    print("\n[EXAMPLE 3] PHOTON (v = c)")
    proper_time, photon_desc = TimeDilation.photon_case()
    print(f"Proper time Δτ: {proper_time}")
    print(photon_desc)
    
    # Example 4: High-speed spacecraft
    print("\n[EXAMPLE 4] Spacecraft at 0.1c (10% light speed) at Earth")
    spacecraft_velocity = 0.1 * SPEED_OF_LIGHT
    
    dt_spacecraft = TimeDilation.combined_time_dilation(
        coordinate_time=tau_0,
        velocity=spacecraft_velocity,
        mass_source=earth_mass,
        distance=earth_radius
    )
    print(f"Velocity: {spacecraft_velocity:.2e} m/s (0.1c)")
    print(f"Δτ = {dt_spacecraft:.15f} s")
    print(f"Time dilation factor: {dt_spacecraft / tau_0:.8f}")
    print(f"After 1 year of travel, crew ages {dt_spacecraft / tau_0 * 365.25:.2f} days")
