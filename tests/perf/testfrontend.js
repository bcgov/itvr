import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2ms', target: 20 },
    { duration: '20s', target: 0 },
  ],
};

export default function () {
  const res = http.get('https://itvr-dev-148.apps.silver.devops.gov.bc.ca/');
  //check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(1);
}