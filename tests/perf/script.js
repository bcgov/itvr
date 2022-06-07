// Scenario: Scenario_1 (executor: constant-vus)

import { sleep, group } from 'k6'
import http from 'k6/http'

import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js'

export const options = {
  thresholds: {},
  scenarios: {
    Scenario_1: {
      executor: 'per-vu-iterations',
      vus: 1,
      iterations: 1,
      exec: 'scenario_1',
    },
  },
}

export function scenario_1() {
  let formData, response

  group('Landing Page', function () {
    response = http.get('https://itvr-test.apps.silver.devops.gov.bc.ca/', {
      headers: {
        'upgrade-insecure-requests': '1',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
      },
    })
  })

  group(
    'Login Page',
    function () {
      response = http.get(
        'https://test.oidc.gov.bc.ca/auth/realms/onestopauth-basic/protocol/openid-connect/auth?client_id=itvr-2674&redirect_uri=https%3A%2F%2Fitvr-test.apps.silver.devops.gov.bc.ca%2Fform&state=7e86d84b-aea7-4415-8626-bfeeaf6acce3&response_mode=fragment&response_type=code&scope=openid&nonce=d506f4e2-104b-41fd-804d-24056b671419&kc_idp_hint=bceid-basic&code_challenge=hUuZ96h_rMDmyG8rCiq1BfPF9ZpV5K2QzNrbcL5TWyk&code_challenge_method=S256',
        {
          headers: {
            'upgrade-insecure-requests': '1',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
          },
        }
      )
      console.log(JSON.stringify(response, null, 2))
    }
  )

  // group('page_3 - https://sfstest7.gov.bc.ca/affwebservices/public/saml2sso', function () {
  //   response = http.post(
  //     'https://sfstest7.gov.bc.ca/affwebservices/public/saml2sso',
  //     {
  //       SAMLRequest:
  //         'PHNhbWxwOkF1dGhuUmVxdWVzdCB4bWxuczpzYW1scD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOnByb3RvY29sIiB4bWxucz0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiIgQXNzZXJ0aW9uQ29uc3VtZXJTZXJ2aWNlVVJMPSJodHRwczovL3Rlc3Qub2lkYy5nb3YuYmMuY2EvYXV0aC9yZWFsbXMvX2JjZWlkYmFzaWMvYnJva2VyL19iY2VpZGJhc2ljL2VuZHBvaW50IiBEZXN0aW5hdGlvbj0iaHR0cHM6Ly9zZnN0ZXN0Ny5nb3YuYmMuY2EvYWZmd2Vic2VydmljZXMvcHVibGljL3NhbWwyc3NvIiBGb3JjZUF1dGhuPSJ0cnVlIiBJRD0iSURfNWYzMmJjNDEtOTRiNC00Zjc4LWFhNjAtMDUyYmE4NGYwMzVmIiBJc1Bhc3NpdmU9ImZhbHNlIiBJc3N1ZUluc3RhbnQ9IjIwMjItMDYtMDNUMjE6MTY6MTQuMTgzWiIgUHJvdG9jb2xCaW5kaW5nPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YmluZGluZ3M6SFRUUC1QT1NUIiBWZXJzaW9uPSIyLjAiPjxzYW1sOklzc3VlciB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj5odHRwczovL3Rlc3Qub2lkYy5nb3YuYmMuY2EvYXV0aC9yZWFsbXMvX2JjZWlkYmFzaWM8L3NhbWw6SXNzdWVyPjxzYW1scDpOYW1lSURQb2xpY3kgQWxsb3dDcmVhdGU9InRydWUiIEZvcm1hdD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOm5hbWVpZC1mb3JtYXQ6cGVyc2lzdGVudCIvPjwvc2FtbHA6QXV0aG5SZXF1ZXN0Pg==',
  //       RelayState:
  //         'U2UGgfFHmYv_fkwWItOSHja7fFq94_A8uiEXaE5cJM4.qqTsjZ-E6SQ.https://test.oidc.gov.bc.ca/auth/realms/onestopauth-basic',
  //     },
  //     {
  //       headers: {
  //         'content-type': 'application/x-www-form-urlencoded',
  //         origin: 'null',
  //         'upgrade-insecure-requests': '1',
  //         'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  //         'sec-ch-ua-mobile': '?0',
  //         'sec-ch-ua-platform': '"macOS"',
  //       },
  //     }
  //   )
  //   sleep(3)
  // })

  // group('page_4 - https://logontest7.gov.bc.ca/clp-cgi/preLogon.cgi', function () {
  //   response = http.post(
  //     'https://logontest7.gov.bc.ca/clp-cgi/preLogon.cgi',
  //     {
  //       instance: 'instance_capBceid',
  //       user: 'naomiaro',
  //       password: 'Keycloak1',
  //     },
  //     {
  //       headers: {
  //         'content-type': 'application/x-www-form-urlencoded',
  //         origin: 'https://logontest7.gov.bc.ca',
  //         'upgrade-insecure-requests': '1',
  //         'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  //         'sec-ch-ua-mobile': '?0',
  //         'sec-ch-ua-platform': '"macOS"',
  //       },
  //     }
  //   )
  //   sleep(0.7)
  // })

  // group('page_5 - https://logontest7.gov.bc.ca/clp-cgi/cap07/logon.fcc', function () {
  //   response = http.post(
  //     'https://logontest7.gov.bc.ca/clp-cgi/cap07/logon.fcc',
  //     {
  //       SMENC: 'ISO-8859-1',
  //       SMLOCALE: 'US-EN',
  //       target: '/clp-cgi/cap07/private/postLogon.cgi',
  //       smauthreason: '0',
  //       smagentname: '',
  //       user: 'naomiaro',
  //       password: 'Keycloak1',
  //     },
  //     {
  //       headers: {
  //         'content-type': 'application/x-www-form-urlencoded',
  //         origin: 'https://logontest7.gov.bc.ca',
  //         'upgrade-insecure-requests': '1',
  //         'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  //         'sec-ch-ua-mobile': '?0',
  //         'sec-ch-ua-platform': '"macOS"',
  //       },
  //     }
  //   )
  //   sleep(0.6)
  // })

  // group(
  //   'page_6 - https://sfstest7.gov.bc.ca/affwebservices/redirectjsp/testpathfinder-basicbceid/redirect.jsp?SAMLTRANSACTIONID=226d9745-93f075c0-74cec648-d88ec367-8ed5505a-2c5&SMPORTALURL=https%3A%2F%2Fsfstest7.gov.bc.ca%2Faffwebservices%2Fpublic%2Fsaml2sso',
  //   function () {
  //     response = http.get(
  //       'https://sfstest7.gov.bc.ca/affwebservices/redirectjsp/testpathfinder-basicbceid/redirect.jsp?SAMLTRANSACTIONID=226d9745-93f075c0-74cec648-d88ec367-8ed5505a-2c5&SMPORTALURL=https%3A%2F%2Fsfstest7.gov.bc.ca%2Faffwebservices%2Fpublic%2Fsaml2sso',
  //       {
  //         headers: {
  //           'upgrade-insecure-requests': '1',
  //           'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  //           'sec-ch-ua-mobile': '?0',
  //           'sec-ch-ua-platform': '"macOS"',
  //         },
  //       }
  //     )
  //   }
  // )

  // group(
  //   'page_7 - https://test.oidc.gov.bc.ca/auth/realms/_bceidbasic/broker/_bceidbasic/endpoint',
  //   function () {
  //     response = http.post(
  //       'https://test.oidc.gov.bc.ca/auth/realms/_bceidbasic/broker/_bceidbasic/endpoint',
  //       {
  //         RelayState:
  //           'U2UGgfFHmYv_fkwWItOSHja7fFq94_A8uiEXaE5cJM4.qqTsjZ-E6SQ.https://test.oidc.gov.bc.ca/auth/realms/onestopauth-basic',
  //         SAMLResponse:
  //           'PFJlc3BvbnNlIHhtbG5zPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIERlc3RpbmF0aW9uPSJodHRwczovL3Rlc3Qub2lkYy5nb3YuYmMuY2EvYXV0aC9yZWFsbXMvX2JjZWlkYmFzaWMvYnJva2VyL19iY2VpZGJhc2ljL2VuZHBvaW50IiBJRD0iX2E4OGVhMzhhZTU0ZWI1MmZiMWRlNTRjMDcyNmRkNzdhNjkzMSIgSW5SZXNwb25zZVRvPSJJRF81ZjMyYmM0MS05NGI0LTRmNzgtYWE2MC0wNTJiYTg0ZjAzNWYiIElzc3VlSW5zdGFudD0iMjAyMi0wNi0wM1QyMToxNjoxOVoiIFZlcnNpb249IjIuMCI+DQogICAgPG5zMTpJc3N1ZXIgeG1sbnM6bnMxPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OmVudGl0eSI+dXJuOmNhOmJjOmdvdjpzZnN0ZXN0OnRlc3RwYXRoZmluZGVyOmJhc2ljPC9uczE6SXNzdWVyPg0KICAgIDxTdGF0dXM+DQogICAgICAgIDxTdGF0dXNDb2RlIFZhbHVlPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6c3RhdHVzOlN1Y2Nlc3MiLz4NCiAgICA8L1N0YXR1cz4NCiAgICA8bnMyOkFzc2VydGlvbiB4bWxuczpuczI9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSJfMGUwZWZhMGE5ZDk4ZTU3NDFjOWMyMTczYmE5OWFkMDk0MjEzIiBJc3N1ZUluc3RhbnQ9IjIwMjItMDYtMDNUMjE6MTY6MTlaIiBWZXJzaW9uPSIyLjAiPg0KICAgICAgICA8bnMyOklzc3VlciBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OmVudGl0eSI+dXJuOmNhOmJjOmdvdjpzZnN0ZXN0OnRlc3RwYXRoZmluZGVyOmJhc2ljPC9uczI6SXNzdWVyPjxkczpTaWduYXR1cmUgeG1sbnM6ZHM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvMDkveG1sZHNpZyMiPg0KPGRzOlNpZ25lZEluZm8+DQo8ZHM6Q2Fub25pY2FsaXphdGlvbk1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvMTAveG1sLWV4Yy1jMTRuIyIvPg0KPGRzOlNpZ25hdHVyZU1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvMDQveG1sZHNpZy1tb3JlI3JzYS1zaGEyNTYiLz4NCjxkczpSZWZlcmVuY2UgVVJJPSIjXzBlMGVmYTBhOWQ5OGU1NzQxYzljMjE3M2JhOTlhZDA5NDIxMyI+DQo8ZHM6VHJhbnNmb3Jtcz4NCjxkczpUcmFuc2Zvcm0gQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLzA5L3htbGRzaWcjZW52ZWxvcGVkLXNpZ25hdHVyZSIvPg0KPGRzOlRyYW5zZm9ybSBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvMTAveG1sLWV4Yy1jMTRuIyIvPg0KPC9kczpUcmFuc2Zvcm1zPg0KPGRzOkRpZ2VzdE1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvMDQveG1sZW5jI3NoYTI1NiIvPg0KPGRzOkRpZ2VzdFZhbHVlPjlvZEFucnd0OGJPYWIramZ0QjlNaDEyRzh0TFBaMUVma3loTERCTXl4VHM9PC9kczpEaWdlc3RWYWx1ZT4NCjwvZHM6UmVmZXJlbmNlPg0KPC9kczpTaWduZWRJbmZvPg0KPGRzOlNpZ25hdHVyZVZhbHVlPg0KUXZRak9NRVE0UWtIQkVTWmI1UXZkM1dRaTQwMFFDUTAwV0s2ck80djF4MFRIL00xaDZnYnlmSmZCQUxzQzVUWm1MZW5yYVhLZG0zcA0KaGdrV09xQW9uaTdxT3VyY1NIT2pIRi8vcUJOZTdRUmV3aVBYQ0s0MytPWk13K1dxK3pFSjhPS3JXUFh4ZmhFNlZaek5GRzVkZDRFSw0KeElHd1k4aDRCUy9yRFZWbmdHVW1yNy8wSk4zOVM4NFdITnIzK1R4a0xZNEdDSCt2M09xWXJCMDhBOC9acUUxRm1BMDZuN1JMdDk3aw0KN3N2QlhkbThOQUNKN1Jxc1FwRlk2WDFwbytWdVhiUHMrcGRXd3hPMm9rTVcrVU9PWWh2anlKTW80aC9zb1EzVEgyTjJMV1RhR1hmaw0KNlo0a1htMEpCYTNpUU5QZjhBN2NtUDlUR3FWZml1M0h5cllMV2c9PQ0KPC9kczpTaWduYXR1cmVWYWx1ZT4NCjxkczpLZXlJbmZvPg0KPGRzOlg1MDlEYXRhPg0KPGRzOlg1MDlDZXJ0aWZpY2F0ZT4NCk1JSUVDekNDQXZNQ0NRQ2RvV040WHRVSTZUQU5CZ2txaGtpRzl3MEJBUXNGQURDQnlqRUxNQWtHQTFVRUJoTUNRMEV4R1RBWEJnTlYNCkJBZ1RFRUp5YVhScGMyZ2dRMjlzZFcxaWFXRXhFVEFQQmdOVkJBY1RDRlpwWTNSdmNtbGhNVGN3TlFZRFZRUUtFeTVIYjNabGNtNXQNClpXNTBJRzltSUhSb1pTQlFjbTkyYVc1alpTQnZaaUJDY21sMGFYTm9JRU52YkhWdFltbGhNUTh3RFFZRFZRUUxFd1pUUmxNdFEwRXgNCklqQWdCZ05WQkFNVEdWTkdVeUJEWlhKMGFXWnBZMkYwWlNCQmRYUm9iM0pwZEhreEh6QWRCZ2txaGtpRzl3MEJDUUVXRUZkVVUxZEINClRVQm5iM1l1WW1NdVkyRXdIaGNOTVRNd05EQTFNakkxTmpVM1doY05Nek13TkRBMU1qSTFOalUzV2pDQnd6RUxNQWtHQTFVRUJoTUMNClEwRXhHVEFYQmdOVkJBZ1RFRUp5YVhScGMyZ2dRMjlzZFcxaWFXRXhFVEFQQmdOVkJBY1RDRlpwWTNSdmNtbGhNVGN3TlFZRFZRUUsNCkV5NUhiM1psY201dFpXNTBJRzltSUhSb1pTQlFjbTkyYVc1alpTQnZaaUJDY21sMGFYTm9JRU52YkhWdFltbGhNUXd3Q2dZRFZRUUwNCkV3TlRSbE14SGpBY0JnTlZCQU1URlhObWN5MXpabk4wWlhOMExtZHZkaTVpWXk1allURWZNQjBHQ1NxR1NJYjNEUUVKQVJZUVYxUlQNClYwRk5RR2R2ZGk1aVl5NWpZVENDQVNJd0RRWUpLb1pJaHZjTkFRRUJCUUFEZ2dFUEFEQ0NBUW9DZ2dFQkFKdzVFMDQ1amxKK3NiU2cNCk5ma3Z5SkEzKzI3S1JCbUFscStNVVJvUjNPU2lXYzIwTVdkdDVwS3hkUlVxMmZZeHJRanRydFB1R3Fra0VHYWVJMGlOWndSSW5ieTYNCkh1NnViQ3dmMVE3ZlRsVzc4bHMrQ2pOa1lOVUMzL3d1QzNtbjFRbmc4VTBsZFE3dFFVNGNQT3F3TEl2U2lKZGlKWnJtRjhSRHBwb2QNClljSGhiaWo3N3Q2dGlIVkN4UVlncXhOY3V0M2d3bnhWcjI0MTZ5V0hYVnFxcGNjS0xUaUkvSm9lQ2I1b0kyVVVDcmRldnlXZDRINXENCk5abHk0aEw1UEJDWVk0VHVwVWF5amhiV2Z4Sks0VVdjRHY3T09hK3V4cTRrWW5HZXhEcHFDYlc2YnZjSGJrNDdQNVJBWkl2Z3ZuR28NCkJnU2ZvaDM3enhRL0ZwNlZFNGlXQXVjQ0F3RUFBVEFOQmdrcWhraUc5dzBCQVFzRkFBT0NBUUVBYmRralE5dUhwdmRrU2VJR09uZngNCnU0Vm5mM2pHTzR5bzgrQnJub0dhTEM4aTJDV21Wb2RpOUdPdTNIM2pyR3ZzU296N242QzJBK3ZJdkR4dkE3dHdqd0xBcXVaVlFKbkINCkNwTUttd2xQQ0FDQXdaK0VsYjRyMnFNbXhhMkZtMEllWXozeDJCV1lPQVR0aWM4MWZGemhKOFFrV0J1d2I5K2RKKzBsL0dHUWY5cE8NCjJxaUlxVUVkMm9JVVZEeHFXUll6aFBlemVqcGZWakJzVFBYWTV4UWhkQlVLSE1yMFpwU1U5a01vSnpjTTFuNmxKSDdwRkhaQlVLTjcNCjkyaG9FNTVPbEszTFFMVW9oKzNXNEROL1lWS2tEczZrSHI0b0w2dXo5ajJXODRIVVBYNURMbUZGaUorTHBTMDUyVkJ0WWNoangyQnQNCjBGUHNISko0QzBGMHI1RzRvdz09DQo8L2RzOlg1MDlDZXJ0aWZpY2F0ZT4NCjwvZHM6WDUwOURhdGE+DQo8L2RzOktleUluZm8+DQo8L2RzOlNpZ25hdHVyZT4NCiAgICAgICAgPG5zMjpTdWJqZWN0Pg0KICAgICAgICAgICAgPG5zMjpOYW1lSUQgRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDpwZXJzaXN0ZW50Ij44REI5RjI1QTAwNzc0QjM0Qjk3MTY0QUNEQkIxRTE4RTwvbnMyOk5hbWVJRD4NCiAgICAgICAgICAgIDxuczI6U3ViamVjdENvbmZpcm1hdGlvbiBNZXRob2Q9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpjbTpiZWFyZXIiPg0KICAgICAgICAgICAgICAgIDxuczI6U3ViamVjdENvbmZpcm1hdGlvbkRhdGEgSW5SZXNwb25zZVRvPSJJRF81ZjMyYmM0MS05NGI0LTRmNzgtYWE2MC0wNTJiYTg0ZjAzNWYiIE5vdE9uT3JBZnRlcj0iMjAyMi0wNi0wM1QyMToxNzo0OVoiIFJlY2lwaWVudD0iaHR0cHM6Ly90ZXN0Lm9pZGMuZ292LmJjLmNhL2F1dGgvcmVhbG1zL19iY2VpZGJhc2ljL2Jyb2tlci9fYmNlaWRiYXNpYy9lbmRwb2ludCIvPg0KICAgICAgICAgICAgPC9uczI6U3ViamVjdENvbmZpcm1hdGlvbj4NCiAgICAgICAgPC9uczI6U3ViamVjdD4NCiAgICAgICAgPG5zMjpDb25kaXRpb25zIE5vdEJlZm9yZT0iMjAyMi0wNi0wM1QyMToxNTo0OVoiIE5vdE9uT3JBZnRlcj0iMjAyMi0wNi0wM1QyMToxNzo0OVoiPg0KICAgICAgICAgICAgPG5zMjpBdWRpZW5jZVJlc3RyaWN0aW9uPg0KICAgICAgICAgICAgICAgIDxuczI6QXVkaWVuY2U+aHR0cHM6Ly90ZXN0Lm9pZGMuZ292LmJjLmNhL2F1dGgvcmVhbG1zL19iY2VpZGJhc2ljPC9uczI6QXVkaWVuY2U+DQogICAgICAgICAgICA8L25zMjpBdWRpZW5jZVJlc3RyaWN0aW9uPg0KICAgICAgICA8L25zMjpDb25kaXRpb25zPg0KICAgICAgICA8bnMyOkF1dGhuU3RhdGVtZW50IEF1dGhuSW5zdGFudD0iMjAyMi0wNi0wM1QyMDozMDo1OVoiIFNlc3Npb25JbmRleD0iQitHR2pycmMrMkswc1RzUk1oV0kzaDRFeEhjPTRBM3FNZz09IiBTZXNzaW9uTm90T25PckFmdGVyPSIyMDIyLTA2LTAzVDIxOjE3OjQ5WiI+DQogICAgICAgICAgICA8bnMyOkF1dGhuQ29udGV4dD4NCiAgICAgICAgICAgICAgICA8bnMyOkF1dGhuQ29udGV4dENsYXNzUmVmPnVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphYzpjbGFzc2VzOlBhc3N3b3JkPC9uczI6QXV0aG5Db250ZXh0Q2xhc3NSZWY+DQogICAgICAgICAgICA8L25zMjpBdXRobkNvbnRleHQ+DQogICAgICAgIDwvbnMyOkF1dGhuU3RhdGVtZW50Pg0KICAgICAgICA8bnMyOkF0dHJpYnV0ZVN0YXRlbWVudD4NCiAgICAgICAgICAgIDxuczI6QXR0cmlidXRlIE5hbWU9ImRpc3BsYXlOYW1lIiBOYW1lRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXR0cm5hbWUtZm9ybWF0OnVuc3BlY2lmaWVkIj4NCiAgICAgICAgICAgICAgICA8bnMyOkF0dHJpYnV0ZVZhbHVlPk5hb21pIEFybzwvbnMyOkF0dHJpYnV0ZVZhbHVlPg0KICAgICAgICAgICAgPC9uczI6QXR0cmlidXRlPg0KICAgICAgICAgICAgPG5zMjpBdHRyaWJ1dGUgTmFtZT0iZW1haWwiIE5hbWVGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphdHRybmFtZS1mb3JtYXQ6dW5zcGVjaWZpZWQiPg0KICAgICAgICAgICAgICAgIDxuczI6QXR0cmlidXRlVmFsdWU+bmFvbWkuYXJvQGdvdi5iYy5jYTwvbnMyOkF0dHJpYnV0ZVZhbHVlPg0KICAgICAgICAgICAgPC9uczI6QXR0cmlidXRlPg0KICAgICAgICAgICAgPG5zMjpBdHRyaWJ1dGUgTmFtZT0idXNlcmlkZW50aWZpZXIiIE5hbWVGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphdHRybmFtZS1mb3JtYXQ6dW5zcGVjaWZpZWQiPg0KICAgICAgICAgICAgICAgIDxuczI6QXR0cmlidXRlVmFsdWU+OERCOUYyNUEwMDc3NEIzNEI5NzE2NEFDREJCMUUxOEU8L25zMjpBdHRyaWJ1dGVWYWx1ZT4NCiAgICAgICAgICAgIDwvbnMyOkF0dHJpYnV0ZT4NCiAgICAgICAgICAgIDxuczI6QXR0cmlidXRlIE5hbWU9InVzZXJuYW1lIiBOYW1lRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXR0cm5hbWUtZm9ybWF0OnVuc3BlY2lmaWVkIj4NCiAgICAgICAgICAgICAgICA8bnMyOkF0dHJpYnV0ZVZhbHVlPm5hb21pYXJvPC9uczI6QXR0cmlidXRlVmFsdWU+DQogICAgICAgICAgICA8L25zMjpBdHRyaWJ1dGU+DQogICAgICAgIDwvbnMyOkF0dHJpYnV0ZVN0YXRlbWVudD4NCiAgICA8L25zMjpBc3NlcnRpb24+DQo8L1Jlc3BvbnNlPg==',
  //       },
  //       {
  //         headers: {
  //           'content-type': 'application/x-www-form-urlencoded',
  //           origin: 'https://sfstest7.gov.bc.ca',
  //           'upgrade-insecure-requests': '1',
  //           'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  //           'sec-ch-ua-mobile': '?0',
  //           'sec-ch-ua-platform': '"macOS"',
  //         },
  //       }
  //     )

  //     response = http.get(
  //       'https://test.oidc.gov.bc.ca/auth/realms/onestopauth-basic/protocol/openid-connect/3p-cookies/step1.html',
  //       {
  //         headers: {
  //           'upgrade-insecure-requests': '1',
  //           'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  //           'sec-ch-ua-mobile': '?0',
  //           'sec-ch-ua-platform': '"macOS"',
  //         },
  //       }
  //     )

  //     response = http.get(
  //       'https://test.oidc.gov.bc.ca/auth/realms/onestopauth-basic/protocol/openid-connect/3p-cookies/step2.html',
  //       {
  //         headers: {
  //           'upgrade-insecure-requests': '1',
  //           'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  //           'sec-ch-ua-mobile': '?0',
  //           'sec-ch-ua-platform': '"macOS"',
  //         },
  //       }
  //     )

  //     response = http.get(
  //       'https://test.oidc.gov.bc.ca/auth/realms/onestopauth-basic/protocol/openid-connect/login-status-iframe.html',
  //       {
  //         headers: {
  //           'upgrade-insecure-requests': '1',
  //           'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  //           'sec-ch-ua-mobile': '?0',
  //           'sec-ch-ua-platform': '"macOS"',
  //         },
  //       }
  //     )

  //     response = http.post(
  //       'https://test.oidc.gov.bc.ca/auth/realms/onestopauth-basic/protocol/openid-connect/token',
  //       {
  //         code:
  //           '294e5287-5f9d-44a2-b6c0-394673c42f34.e0972fa3-1dcd-40ea-abda-12ce82e1456d.f408a5f6-eb70-45cb-a74d-419ac1b6bb51',
  //         grant_type: 'authorization_code',
  //         client_id: 'itvr-2674',
  //         redirect_uri: 'https://itvr-test.apps.silver.devops.gov.bc.ca/form',
  //         code_verifier:
  //           'AhDfOXYQqOlOozWhs6sywe6ZLQEi1aIrHP2GMf90pdRrgutRUS50OHGEjbjnsn7HXQV26ufyAqryr6SBKHFwvgIiItgCijoI',
  //       },
  //       {
  //         headers: {
  //           'content-type': 'application/x-www-form-urlencoded',
  //           'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  //           'sec-ch-ua-mobile': '?0',
  //           'sec-ch-ua-platform': '"macOS"',
  //         },
  //       }
  //     )
  //     sleep(5.1)

  //     response = http.get(
  //       'https://test.oidc.gov.bc.ca/auth/realms/onestopauth-basic/protocol/openid-connect/login-status-iframe.html/init?client_id=itvr-2674&origin=https%3A%2F%2Fitvr-test.apps.silver.devops.gov.bc.ca',
  //       {
  //         headers: {
  //           'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  //           'sec-ch-ua-mobile': '?0',
  //           'sec-ch-ua-platform': '"macOS"',
  //         },
  //       }
  //     )
  //     sleep(41.6)

  //     formData = new FormData()
  //     formData.boundary = '----WebKitFormBoundaryXtR3B061PayWnNKZ'
  //     formData.append('sin', '130692544')
  //     formData.append('first_name', 'Kuan')
  //     formData.append('last_name', 'Fan')
  //     formData.append('middle_names', '')
  //     formData.append('email', 'Kuan.Fan@gov.bc.ca')
  //     formData.append('address', '1832 Raspberry Row')
  //     formData.append('city', 'Victoria')
  //     formData.append('postal_code', 'V8N6K3')
  //     formData.append('date_of_birth', '1988-01-01')
  //     formData.append('drivers_licence', '1234567')
  //     formData.append(
  //       'doc1',
  //       'PNG\r\n\u001a\n\u0000\u0000\u0000\rIHDR\u0000\u0000\u0000\u0010\u0000\u0000\u0000\u0010\b\u0006\u0000\u0000\u0000\u001fóÿa\u0000\u0000\u0000@IDAT8Ocøÿÿ?\u0003%\u0018Îðl{þ\u001f\u000fÞÏ\u0004H2àâÃ\u0018d\u0000\b \u001bB²\u0001èe\u0000²!$\u0019ÃÐQ\u0003F\rÀn\u0000¹\u0018\u0000¨Ì\u000f}\u000fú\u0000\u0000\u0000\u0000IEND®B`'
  //     )
  //     formData.append(
  //       'doc2',
  //       'PNG\r\n\u001a\n\u0000\u0000\u0000\rIHDR\u0000\u0000\u0000\u0010\u0000\u0000\u0000\u0010\b\u0006\u0000\u0000\u0000\u001fóÿa\u0000\u0000\u0000@IDAT8Ocøÿÿ?\u0003%\u0018Îðl{þ\u001f\u000fÞÏ\u0004H2àâÃ\u0018d\u0000\b \u001bB²\u0001èe\u0000²!$\u0019ÃÐQ\u0003F\rÀn\u0000¹\u0018\u0000¨Ì\u000f}\u000fú\u0000\u0000\u0000\u0000IEND®B`'
  //     )
  //     formData.append('consent_personal', 'true')
  //     formData.append('consent_tax', 'true')
  //     formData.append('application_type', 'individual')
  //     formData.append('spouse_email', '')

  //     response = http.post(
  //       'https://itvr-backend-test.apps.silver.devops.gov.bc.ca/api/application-form',
  //       formData.body(),
  //       {
  //         headers: {
  //           accept: 'application/json, text/plain, */*',
  //           authorization:
  //             'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJIWVZ0SFNHMlF5VGRja1FFbGE2WHd5bE1NRXJwMmI5Qkw5UElHb3NpeGJJIn0.eyJleHAiOjE2NTQyOTEyODAsImlhdCI6MTY1NDI5MDk4MCwiYXV0aF90aW1lIjoxNjU0MjkwOTc5LCJqdGkiOiIxODMzNzkyMC00MmFjLTRlYmQtODk5OC04NDllODlmZTcyYjkiLCJpc3MiOiJodHRwczovL3Rlc3Qub2lkYy5nb3YuYmMuY2EvYXV0aC9yZWFsbXMvb25lc3RvcGF1dGgtYmFzaWMiLCJhdWQiOiJpdHZyLTI2NzQiLCJzdWIiOiJkYjYxNjdlOC0yZDM0LTQxYTEtOTZmMy1jOTQyZGQxMmY0MDEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJpdHZyLTI2NzQiLCJub25jZSI6ImQ1MDZmNGUyLTEwNGItNDFmZC04MDRkLTI0MDU2YjY3MTQxOSIsInNlc3Npb25fc3RhdGUiOiJlMDk3MmZhMy0xZGNkLTQwZWEtYWJkYS0xMmNlODJlMTQ1NmQiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vaXR2ci10ZXN0LmFwcHMuc2lsdmVyLmRldm9wcy5nb3YuYmMuY2EvKiIsImh0dHBzOi8vaXR2ci10ZXN0LmFwcHMuc2lsdmVyLmRldm9wcy5nb3YuYmMuY2EiXSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImlkZW50aXR5X3Byb3ZpZGVyIjoiYmNlaWQtYmFzaWMiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImJjZWlkX3VzZXJpZCI6IjhEQjlGMjVBMDA3NzRCMzRCOTcxNjRBQ0RCQjFFMThFIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibmFvbWlhcm9AYmNlaWQtYmFzaWMiLCJkaXNwbGF5X25hbWUiOiJOYW9taSBBcm8iLCJlbWFpbCI6Im5hb21pLmFyb0Bnb3YuYmMuY2EifQ.JxWFV5Di6nijmu5hReLOi6LLBCeBWJ2JxfpikMDFn1RcObxHLLSSriucHdIIC5rQpW1nklPgeasXrNQMTpcDdx0dSNoFAouHCHaui0BXr_Hxim5IwZhNfCobh2lUcWHgIZFYH8y6mYnx-jsuGLXlT8Zhc_epSVQbslq_uzJ2hfU9CRUjoRQceCx2qTS-kmZ_3vZFJpYnqoKVzEgq9VAHn32QfOKBJ1JV7xYvLktKXVmNnhpdBGEX7zEUKsCUOquYyMjLLW2JaQdZhp0q1rFdRD6UUXasa9QFW_GFcsLxty0RR8G8HUdvDJGo8G4zlvbd52U-YMnhW5xBXmmvSFnz9w',
  //           'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryXtR3B061PayWnNKZ',
  //           'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  //           'sec-ch-ua-mobile': '?0',
  //           'sec-ch-ua-platform': '"macOS"',
  //         },
  //       }
  //     )

  //     response = http.options(
  //       'https://itvr-backend-test.apps.silver.devops.gov.bc.ca/api/application-form',
  //       null,
  //       {
  //         headers: {
  //           accept: '*/*',
  //           'access-control-request-headers': 'authorization',
  //           'access-control-request-method': 'POST',
  //           origin: 'https://itvr-test.apps.silver.devops.gov.bc.ca',
  //           'sec-fetch-mode': 'cors',
  //         },
  //       }
  //     )
  //     sleep(13.3)

  //     response = http.get(
  //       'https://itvr-backend-test.apps.silver.devops.gov.bc.ca/api/application-form/nWMTxad2wn9v5ynS',
  //       {
  //         headers: {
  //           accept: 'application/json, text/plain, */*',
  //           authorization:
  //             'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJIWVZ0SFNHMlF5VGRja1FFbGE2WHd5bE1NRXJwMmI5Qkw5UElHb3NpeGJJIn0.eyJleHAiOjE2NTQyOTEyODAsImlhdCI6MTY1NDI5MDk4MCwiYXV0aF90aW1lIjoxNjU0MjkwOTc5LCJqdGkiOiIxODMzNzkyMC00MmFjLTRlYmQtODk5OC04NDllODlmZTcyYjkiLCJpc3MiOiJodHRwczovL3Rlc3Qub2lkYy5nb3YuYmMuY2EvYXV0aC9yZWFsbXMvb25lc3RvcGF1dGgtYmFzaWMiLCJhdWQiOiJpdHZyLTI2NzQiLCJzdWIiOiJkYjYxNjdlOC0yZDM0LTQxYTEtOTZmMy1jOTQyZGQxMmY0MDEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJpdHZyLTI2NzQiLCJub25jZSI6ImQ1MDZmNGUyLTEwNGItNDFmZC04MDRkLTI0MDU2YjY3MTQxOSIsInNlc3Npb25fc3RhdGUiOiJlMDk3MmZhMy0xZGNkLTQwZWEtYWJkYS0xMmNlODJlMTQ1NmQiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vaXR2ci10ZXN0LmFwcHMuc2lsdmVyLmRldm9wcy5nb3YuYmMuY2EvKiIsImh0dHBzOi8vaXR2ci10ZXN0LmFwcHMuc2lsdmVyLmRldm9wcy5nb3YuYmMuY2EiXSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImlkZW50aXR5X3Byb3ZpZGVyIjoiYmNlaWQtYmFzaWMiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImJjZWlkX3VzZXJpZCI6IjhEQjlGMjVBMDA3NzRCMzRCOTcxNjRBQ0RCQjFFMThFIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibmFvbWlhcm9AYmNlaWQtYmFzaWMiLCJkaXNwbGF5X25hbWUiOiJOYW9taSBBcm8iLCJlbWFpbCI6Im5hb21pLmFyb0Bnb3YuYmMuY2EifQ.JxWFV5Di6nijmu5hReLOi6LLBCeBWJ2JxfpikMDFn1RcObxHLLSSriucHdIIC5rQpW1nklPgeasXrNQMTpcDdx0dSNoFAouHCHaui0BXr_Hxim5IwZhNfCobh2lUcWHgIZFYH8y6mYnx-jsuGLXlT8Zhc_epSVQbslq_uzJ2hfU9CRUjoRQceCx2qTS-kmZ_3vZFJpYnqoKVzEgq9VAHn32QfOKBJ1JV7xYvLktKXVmNnhpdBGEX7zEUKsCUOquYyMjLLW2JaQdZhp0q1rFdRD6UUXasa9QFW_GFcsLxty0RR8G8HUdvDJGo8G4zlvbd52U-YMnhW5xBXmmvSFnz9w',
  //           'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  //           'sec-ch-ua-mobile': '?0',
  //           'sec-ch-ua-platform': '"macOS"',
  //         },
  //       }
  //     )

  //     response = http.options(
  //       'https://itvr-backend-test.apps.silver.devops.gov.bc.ca/api/application-form/nWMTxad2wn9v5ynS',
  //       null,
  //       {
  //         headers: {
  //           accept: '*/*',
  //           'access-control-request-headers': 'authorization',
  //           'access-control-request-method': 'GET',
  //           origin: 'https://itvr-test.apps.silver.devops.gov.bc.ca',
  //           'sec-fetch-mode': 'cors',
  //         },
  //       }
  //     )
  //   }
  // )
}
