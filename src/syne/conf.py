# Height of unit patterns and number of child units
UNIT_INPUT_HEIGHT = 4

# Width of unit patterns and number of possible impulses in input
UNIT_INPUT_WIDTH = 256

# Max number of patterns in this unit and input width for higher level unit
UNIT_OUTPUT_WIDTH = 256

# If message's average activity less than this value, this message goes to incubator,
# else patterns can learn from this message
UNIT_ACTIVATION_THRESHOLD = 0.4

# Weight limits for patterns in Store
UNIT_MAX_PATTERN_WEIGHT = 1000
UNIT_MIN_PATTERN_WEIGHT = -1000

# New patterns are always added with weight = 0.
# This setting allows to add new patterns with weight below the average
UNIT_AVERAGE_PATTERN_WEIGHT = 400

# How much pattern get from message which it fits,
# learning_intensity = pattern_activity * LEARNING_FACTOR
UNIT_LEARNING_FACTOR = 0.1

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
