# Signal timing (seconds)
MIN_G, MAX_G = 10, 60
YELLOW, ALL_RED = 3, 2
MAX_WAIT = 120          # starvation cap: max red time for any lane
SAT_FLOW = 0.5          # vehicles discharged per second of green

# Vision
ROI = (0.0, 0.4, 1.0, 1.0)   # x1,y1,x2,y2 as frame fractions (lower part of frame)
VEHICLE_CLASSES = (2, 3, 5, 7)  # COCO: car, motorcycle, bus, truck
DETECTION_CONFIDENCE = 0.25
DETECTION_SAMPLE_INTERVAL_SECONDS = 1

# Genetic algorithm
POP, GENS = 30, 50
ELITE, TOURN_K = 2, 3
MUT_RATE, MUT_STEP = 0.1, 5

# Fuzzy
MAX_VEH = 20            # vehicles treated as density = 1.0
