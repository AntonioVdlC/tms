function stringCode(str) {
  const string = String(str);
  const code = [...string].reduce((code, char) => code + char.charCodeAt(0), 0);

  return code;
}

export default stringCode;
