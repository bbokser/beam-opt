titanium = {
    # Annealed Grade 5 Titanium
    # https://www.makeitfrom.com/material-properties/Annealed-Grade-5-Titanium
    "E": 110e9,  # Pa
    "shear_str": 600e6,  # Pa
    "yield_str": 910e6,  # Pa
    "density": 4430,  # g/cc -> kg/m3
    "SF": 2,  # safety factor
    "min_thickness": 0.0004064  # 0.016" = 0.4064 mm
}

cfrp = {
    # CFRP Tube from Dragonplate, 0/90
    # e.g. https://dragonplate.com/carbon-fiber-roll-wrapped-twill-tube-2-id-x-96-thin-wall-gloss-finish
    # http://www.performance-composites.com/carbonfibre/mechanicalproperties_2.asp
    "E": 5.171059e11,  # Pa
    "shear_str": 90e6,  # Pa
    "yield_str": 600e6,  # Pa # actually just UTS
    "density": 1522,  # kg/m3
    "SF": 4,  # safety factor
    "min_thickness": 0.000762
}

aluminum = {
    # Aluminum 7075-T6
    # https://www.makeitfrom.com/material-properties/7075-T6-Aluminum
    "E": 70e9,  # Pa
    "shear_str": 330e6,  # Pa
    "yield_str": 480e6,  # Pa # actually just UTS
    "density": 2710,  # kg/m3
    "SF": 2,  # safety factor
    "min_thickness": 0.0004064  # 0.016" = 0.4064 mm
}