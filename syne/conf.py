
# If message's average activity less than this value, this message goes to incubator
UNIT_ACTIVE_SIGNAL_ACTIVITY = 0.4

# Width of unit patterns and number of child units
UNIT_INPUT_WIDTH = 4

# Height of unit patterns and number of possible impulses in input
UNIT_INPUT_HEIGHT = 256

# If activity of impulse greater then this value, incubator counts it as active
INCUBATOR_IMPULSE_ACTIVITY_THRESHOLD = 0.5

# Create patterns while best sample have at least this weight
INCUBATOR_READY_SAMPLE_WEIGHT = 5

# Samples have None instead of some impulses, filter samples that have many of None
INCUBATOR_MIN_SAMPLE_IMPULSES = 2

# When incubator creates pattern, set this value to base sample impulses
INCUBATOR_NEW_PATTERN_IMPULSE_WEIGHT = 0.7

# When incubator creates pattern, all samples that have this similarity with base sample will be
# added to pattern
INCUBATOR_NEW_PATTERN_SIMILAR_SAMPLES_ACTIVITY = 0.6
