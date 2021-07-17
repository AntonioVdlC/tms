const reHex = /^[0-9a-fA-F]{24}$/;

/**
 * Checks if an `id` is an ObjectId (loosely)
 *
 * @param {String} id A potential ObjectId
 * @returns {Boolean}
 */
function isObjectId(id) {
  if (!id || typeof id !== "string") {
    return false;
  }

  return id.length === 12 || (id.length === 24 && reHex.test(id));
}

export default isObjectId;
