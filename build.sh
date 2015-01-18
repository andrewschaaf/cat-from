CC_ARGS="-std=c99 -O3"

mkdir -p build &&
  $CC $CC_ARGS -o build/cat-from cat-from.c &&
  echo "Built."
