import getObjectValueByKey from "@/utils/get-object-value-by-key";

function alphabetically(key, direction = "asc") {
  const sign = direction === "desc" ? -1 : 1;

  return function (a, b) {
    const aVal = String(getObjectValueByKey(a, key)).toLowerCase();
    const bVal = String(getObjectValueByKey(b, key)).toLowerCase();

    return aVal < bVal ? -1 * sign : aVal > bVal ? 1 * sign : 0;
  };
}

export { alphabetically };
