export const isSINValid = (sin) => {
  if (!sin || sin.length !== 9) {
    return false;
  }
  const regex = /^\d+$/;
  if (!regex.test(sin)) {
    return false;
  }
  const products = [];
  const fixedNumbers = [1, 2, 1, 2, 1, 2, 1, 2, 1];
  for (let i = 0; i < 9; i++) {
    const sinChar = sin.charAt(i);
    const product = fixedNumbers[i] * parseInt(sinChar);
    if (product >= 10) {
      const productString = product.toString();
      products[i] =
        parseInt(productString.charAt(0)) + parseInt(productString.charAt(1));
    } else {
      products[i] = product;
    }
  }
  const result = products.reduce((prev, current) => {
    return prev + current;
  });
  if (result % 10 !== 0) {
    return false;
  }
  return true;
};

export const isAgeValid = (dob, lowerBound, upperBound) => {
  if (!dob) {
    return false;
  }
  dob = dob.toISOString().slice(0, 10);
  const dobSplit = dob.split('-');
  const dobYear = parseInt(dobSplit[0]);
  const dobMonthIndex = parseInt(dobSplit[1]) - 1;
  const dobDay = parseInt(dobSplit[2]);
  const today = new Date();
  let age = today.getFullYear() - dobYear;
  if (
    today.getMonth() < dobMonthIndex ||
    (today.getMonth() == dobMonthIndex && today.getDate() < dobDay)
  ) {
    age = age - 1;
  }
  if (lowerBound && age < lowerBound) {
    return false;
  }
  if (upperBound && age > upperBound) {
    return false;
  }
  return true;
};

export const getDateWithYearOffset = (date, offset) => {
  return new Date(date.getFullYear() + offset, date.getMonth(), date.getDate());
};

export const getLastDayOfMonth = (date) => {
  return new Date(date.getFullYear(), date.getMonth() + 1, 0);
};

export const getFirstDayOfMonth = (date) => {
  return new Date(date.getFullYear(), date.getMonth(), 1);
};
