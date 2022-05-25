import { useEffect, useRef } from 'react';
import axios from 'axios';
import { useKeycloak } from '@react-keycloak/web';
import { API_BASE } from '../config';

const useAxios = (opts = {}) => {
  const axiosInstance = useRef();
  const { keycloak, initialized } = useKeycloak();
  const kcToken = keycloak.token;

  useEffect(() => {
    axiosInstance.current = axios.create({
      baseURL: API_BASE,
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
