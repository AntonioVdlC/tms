import stringCode from "@/utils/string-code";

const _colors = [
  "#334155",
  "#1E293B",
  "#0F172A",
  "#374151",
  "#1F2937",
  "#111827",
  "#3F3F46",
  "#27272A",
  "#18181B",
  "#404040",
  "#262626",
  "#171717",
  "#44403C",
  "#292524",
  "#1C1917",
  "#B91C1C",
  "#991B1B",
  "#7F1D1D",
  "#C2410C",
  "#9A3412",
  "#7C2D12",
  "#B45309",
  "#92400E",
  "#78350F",
  "#A16207",
  "#854D0E",
  "#713F12",
  "#4D7C0F",
  "#3F6212",
  "#365314",
  "#15803D",
  "#166534",
  "#14532D",
  "#047857",
  "#065F46",
  "#064E3B",
  "#0F766E",
  "#115E59",
  "#134E4A",
  "#0E7490",
  "#155E75",
  "#164E63",
  "#0369A1",
  "#075985",
  "#0C4A6E",
  "#1D4ED8",
  "#1E40AF",
  "#1E3A8A",
  "#4338CA",
  "#3730A3",
  "#312E81",
  "#6D28D9",
  "#5B21B6",
  "#4C1D95",
  "#7E22CE",
  "#6B21A8",
  "#581C87",
  "#A21CAF",
  "#86198F",
  "#701A75",
  "#BE185D",
  "#9D174D",
  "#831843",
  "#BE123C",
  "#9F1239",
  "#881337",
];

/**
 * Generates a color given a string
 *
 * @param {String} str Character (or string)
 * @returns {String}
 */
function generateColor(str) {
  const _colorIndex = Math.floor(stringCode(str) % _colors.length);
  const color = _colors[_colorIndex];

  return color;
}

export default generateColor;
