import { useEffect, useRef } from 'react';
import axios from 'axios';
import useCustomKeycloak from './keycloakHook';

const baseURL = process.env.REACT_APP_API_BASE;

const useAxios = (opts = {}) => {
  const axiosInstance = useRef();
  const { keycloak, initialized } = useCustomKeycloak();
  const kcToken = keycloak.token;

  useEffect(() => {
    axiosInstance.current = axios.create({
      baseURL,
      ...opts,
      headers: {
        Authorization: initialized ? `Bearer ${kcToken}` : undefined
      }
    });

    return () => {
      axiosInstance.current = undefined;
    };
  }, [opts, initialized, kcToken]);

  return axiosInstance;
};

export default useAxios;
