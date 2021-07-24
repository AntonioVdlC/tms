function getObjectValueByKey(obj = {}, key = "") {
  return String(key)
    .split(".")
    .reduce((a, k) => a && a[k], obj);
}

export default getObjectValueByKey;
