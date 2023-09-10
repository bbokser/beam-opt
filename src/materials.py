titanium = {
    # Annealed Grade 5 Titanium
    # https://www.makeitfrom.com/material-properties/Annealed-Grade-5-Titanium
    "E_flex": 110e9,  # Pa
    "E_comp": 110e9,  # Pa
    "shear_str": 600e6,  # Pa
    "flex_str": 910e6,  # Pa
    "density": 4430,  # g/cc -> kg/m3
    "thickness_min": 0.0004064  # 0.016" = 0.4064 mm
}

cfrp = {
    # CFRP Tube from Dragonplate, 0/90
    # e.g. https://dragonplate.com/carbon-fiber-roll-wrapped-twill-tube-2-id-x-96-thin-wall-gloss-finish
    # https://www.toraycma.com/wp-content/uploads/M55J-Technical-Data-Sheet-1.pdf.pdf
    "E_flex": 132e9,  # flexural modulus in 0 degrees
    "E_comp": 10e9,  # compressive modulus in 90 degrees
    "shear_str": 102e6,  # flexural strength in 90 degrees
    "flex_str": 1745e6,  # flexural strength in 0 degrees
    "density": 1522,  # kg/m3
    "thickness_min": 0.000762
}

aluminum = {
    # Aluminum 7075-T6
    # https://www.makeitfrom.com/material-properties/7075-T6-Aluminum
    "E_flex": 70e9,  # Pa
    "E_comp": 70e9,
    "shear_str": 330e6,  # Pa
    "flex_str": 480e6,  # Pa
    "density": 2710,  # kg/m3
    "thickness_min": 0.0004064  # 0.016" = 0.4064 mm
}