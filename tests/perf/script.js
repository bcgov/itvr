import { sleep, group } from 'k6'
import http from 'k6/http'
import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js'

const img1 = open('./image-2.5m-1.jpg', 'b');
const img2 = open('./image-2.5m-1.jpg', 'b');

export const options = {
  ext: {
    loadimpact: {
      distribution: { 'amazon:us:ashburn': { loadZone: 'amazon:us:ashburn', percent: 100 } },
      apm: [],
    },
  },
  thresholds: {},
  scenarios: {
    Scenario_1: {
      executor: 'per-vu-iterations',
      vus: 5,
      iterations: 4,
      maxDuration: '2m',
      exec: 'scenario_1',
    },
  },
}

export function scenario_1() {
  let formData, response

  group(
    'Post form',
    function () {

      formData = new FormData()
      formData.boundary = '----WebKitFormBoundaryamNAoA2s30AKqLAn'
      formData.append('sin', '130692544')
      formData.append('first_name', 'Kuan')
      formData.append('last_name', 'Fan')
      formData.append('middle_names', '')
      formData.append('email', 'Kuan.Fan@gov.bc.ca')
      formData.append('address', '1832 Raspberry Row')
      formData.append('city', 'Victoria')
      formData.append('postal_code', 'V8N6K3')
      formData.append('date_of_birth', '1988-01-01')
      formData.append('drivers_licence', '1234567')

      formData.append('doc1', http.file(img1, './image-2.5m-1.jpg', 'image/jpg'))
      formData.append('doc2', http.file(img2, './image-2.5m-2.jpg', 'image/jpg'))

      formData.append('consent_personal', 'true')
      formData.append('consent_tax', 'true')
      formData.append('application_type', 'individual')
      formData.append('spouse_email', '')

      response = http.post(
        'https://itvr-backend-dev-150.apps.silver.devops.gov.bc.ca/api/application-form',
        formData.body(),
        {
          headers: {
            accept: 'application/json, text/plain, */*',
            authorization:
              'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJLVmdsS1VDb3ZSLW5QVjNiMnRQY0hHOGM1eVVia3NnMmtZbGk5c2hfUFlNIn0.eyJleHAiOjE2NTQ2Mzk4MDUsImlhdCI6MTY1NDYzOTUwNSwiYXV0aF90aW1lIjoxNjU0NjM5Mzk4LCJqdGkiOiIxOGNlN2MxMS0zMzBlLTQxOTAtOTI4Ni0yYWY5YjJjZTU1MzUiLCJpc3MiOiJodHRwczovL2Rldi5vaWRjLmdvdi5iYy5jYS9hdXRoL3JlYWxtcy9vbmVzdG9wYXV0aC1iYXNpYyIsImF1ZCI6Iml0dnItMjY3NCIsInN1YiI6ImNjNjBiZmQyLTAzY2ItNDY5MC04ZTg2LWM5NDBjZjgwYzZiMSIsInR5cCI6IkJlYXJlciIsImF6cCI6Iml0dnItMjY3NCIsIm5vbmNlIjoiZjRmMTdkODYtNWEyOC00MDcyLTkzZTctM2JmY2FhNzFkZWY3Iiwic2Vzc2lvbl9zdGF0ZSI6IjQ5ZWIwNTY3LWMwYWYtNDhhNS1iZThmLWVlY2MzNjZiYTQzMiIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9pdHZyLWRldi0xNDguYXBwcy5zaWx2ZXIuZGV2b3BzLmdvdi5iYy5jYSIsImh0dHBzOi8vaXR2ci1kZXYtMTUwLmFwcHMuc2lsdmVyLmRldm9wcy5nb3YuYmMuY2EiLCJodHRwOi8vbG9jYWxob3N0OjMwMDAvKiIsImh0dHBzOi8vaXR2ci1kZXYtMTUwLmFwcHMuc2lsdmVyLmRldm9wcy5nb3YuYmMuY2EvKiIsImh0dHBzOi8vaXR2ci1kZXYtMTAyLmFwcHMuc2lsdmVyLmRldm9wcy5nb3YuYmMuY2EvKiIsImh0dHBzOi8vaXR2ci1kZXYtMTAyLmFwcHMuc2lsdmVyLmRldm9wcy5nb3YuYmMuY2EiLCJodHRwczovL2l0dnItZGV2LTE0OC5hcHBzLnNpbHZlci5kZXZvcHMuZ292LmJjLmNhLyoiLCJodHRwOi8vbG9jYWxob3N0OjMwMDAiLCJodHRwczovL2l0dnItZGV2LmFwcHMuc2lsdmVyLmRldm9wcy5nb3YuYmMuY2EvKiIsImh0dHBzOi8vaXR2ci1kZXYuYXBwcy5zaWx2ZXIuZGV2b3BzLmdvdi5iYy5jYSJdLCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwiaWRlbnRpdHlfcHJvdmlkZXIiOiJiY2VpZC1iYXNpYyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiYmNlaWRfdXNlcmlkIjoiOERCOUYyNUEwMDc3NEIzNEI5NzE2NEFDREJCMUUxOEUiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJuYW9taWFyb0BiY2VpZC1iYXNpYyIsImRpc3BsYXlfbmFtZSI6Ik5hb21pIEFybyIsImVtYWlsIjoibmFvbWkuYXJvQGdvdi5iYy5jYSJ9.KJ-3ih6qfmegJuGe1C1NcdWnFGh_bZI--MbIsY7J6wZd6iIh1k7A9DWXIdq7WNS6m0QFuDBwg8I-POoj6-PwI2Fno6r5mP7uUrBsdtDo8b8DbQYzIOuyJ3EH0UQyPjZ4p_fpNW2SOJMUM-fY7OSlI-xCBZuC2v1mQ9AkXJh_9IIMYHFLaJmgiZ5s2D4xYyfMiETSdb319jpL4vhNjccjmMa1KpmwTI-wHK3W8Vv49qFNo6W8d712dAhZnCD9aBvxfW4hl4X9sOkDUa0j86Jds2XJQssPlC8vv5SNgaDRi-Sc0brmyBtjE_FeVPI3lr_8yBeUwdRHj0Ps7Zi_93xA_w',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryamNAoA2s30AKqLAn',  
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
          },
        }
      )

      //console.log(JSON.stringify(response, null, 2))
      //sleep(2)

    }
  )
}