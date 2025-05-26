% ---------- Plant Facts ----------
plant(tulsi, "Holy Basil", loamy, full_sun, yes, 
    "A sacred plant in India used for its medicinal properties.", 
    "Needs plenty of sunlight and moderate watering.").

plant(aloe_vera, "Aloe Vera", sandy, full_sun, yes,
    "Succulent plant known for its soothing gel used in skin treatments.",
    "Water once every three weeks and keep in warm sunlight.").

plant(snake_plant, "Snake Plant", loamy, partial_shade, no,
    "Low-maintenance indoor plant that purifies air.",
    "Water occasionally and keep in indirect light.").

plant(peace_lily, "Peace Lily", loamy, shade, no,
    "Beautiful indoor plant with white flowers.",
    "Keep soil moist and place in low light.").

plant(mint, "Mint", sandy, partial_shade, yes,
    "Aromatic herb used in cooking and beverages.",
    "Grows well in pots and needs regular watering.").

plant(bamboo_palm, "Bamboo Palm", loamy, shade, no,
    "Air-purifying plant ideal for offices and indoors.",
    "Keep in shade and water frequently.").

suitable_plant(Soil, Sunlight, Name, CommonName) :-
    plant(Name, CommonName, Soil, Sunlight, _, _, _, _).


edible_plant(Name, CommonName) :-
    plant(Name, CommonName, _, _, yes, _, _, _).





