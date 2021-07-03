function capitalise([first, ...rest], locale = navigator.language) {
  return first.toLocaleUpperCase(locale) + rest.join("");
}

export default capitalise;
