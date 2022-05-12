import { useEffect, useRef } from 'react';
import { useKeycloak } from '@react-keycloak/web';

const useCustomKeycloak = ({ customNonce } = {}) => {
  let nonce = customNonce;
  if (!nonce) {
    customNonce = createUUID();
  }
  const { keycloak, initialized } = useKeycloak();
  const origCreateLoginUrl = keycloak.createLoginUrl;
  keycloak.createLoginUrl = (options) => {
    let url = origCreateLoginUrl(options);
    if (!url.includes('&nonce=')) {
      url = url + '&nonce=' + encodeURIComponent(nonce);
    }
    return url;
  };
  return { keycloak, initialized };
};

//----------------------------------------------------------------------------------
//functions in this section are from keycloak-js

function createUUID() {
  var hexDigits = '0123456789abcdef';
  var s = generateRandomString(36, hexDigits).split('');
  s[14] = '4';
  s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1);
  s[8] = s[13] = s[18] = s[23] = '-';
  var uuid = s.join('');
  return uuid;
}

function generateRandomString(len, alphabet) {
  var randomData = generateRandomData(len);
  var chars = new Array(len);
  for (var i = 0; i < len; i++) {
    chars[i] = alphabet.charCodeAt(randomData[i] % alphabet.length);
  }
  return String.fromCharCode.apply(null, chars);
}

function generateRandomData(len) {
  // use web crypto APIs if possible
  var array = null;
  var crypto = window.crypto || window.msCrypto;
  if (crypto && crypto.getRandomValues && window.Uint8Array) {
    array = new Uint8Array(len);
    crypto.getRandomValues(array);
    return array;
  }

  // fallback to Math random
  array = new Array(len);
  for (var j = 0; j < array.length; j++) {
    array[j] = Math.floor(256 * Math.random());
  }
  return array;
}

//----------------------------------------------------------------------------------

export default useCustomKeycloak;
