{{/*

The labels for all components:
  labels:
    helm.sh/chart: itvr-backend-1.0.0
    app.kubernetes.io/name: itvr-backend
    app.kubernetes.io/instance: itvr-backend-dev-1977
    app.kubernetes.io/version: "1.17.0"
    app.kubernetes.io/managed-by: Helm

The selector lables:
  selector:
    app.kubernetes.io/name: itvr-backend
    app.kubernetes.io/instance: itvr-backend-dev-1977

*/}}


{{/*
Expand the name of the chart.
*/}}
{{- define "itvr-backend.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
The .Release.Name is the first parameter of command helm install itvr-backend
*/}}
{{- define "itvr-backend.fullname" -}}
{{- .Release.Name }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "itvr-backend.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels:
app.kubernetes.io/managed-by would be Helm
*/}}
{{- define "itvr-backend.labels" -}}
helm.sh/chart: {{ include "itvr-backend.chart" . }}
{{ include "itvr-backend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "itvr-backend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "itvr-backend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Define the deploymentconfig name
*/}}
{{- define "itvr-backend.deploymentconfigName" -}}
{{- include "itvr-backend.fullname" . }}
{{- end }}

{{/*
Define the deploymentconfig name
*/}}
{{- define "itvr-backend.imagestreamName" -}}
{{- include "itvr-backend.fullname" . }}
{{- end }}

{{/*
Define the service name
*/}}
{{- define "itvr-backend.serviceName" -}}
{{- include "itvr-backend.fullname" . }}
{{- end }}


{{/*
Define the backend route name
*/}}
{{- define "itvr-backend.routeName" -}}
{{- include "itvr-backend.fullname" . }}
{{- end }}

{{/*
Define the backend admin route name, used by task queue
*/}}
{{- define "itvr-backend.adminRouteName" -}}
itvr-backend-admin{{ .Values.suffix }}
{{- end }}

{{/*
Define the backend static route name, used by task queue
*/}}
{{- define "itvr-backend.staticRouteName" -}}
itvr-backend-static{{ .Values.suffix }}
{{- end }}

{{/*
Define the djangoSecretKey
*/}}
{{- define "itvr-backend.djangoSecretKey" -}}
{{- randAlphaNum 50 | nospace | b64enc }}
{{- end }}

{{/*
Define the djangoSaltKey
*/}}
{{- define "itvr-backend.djangoSaltKey" -}}
{{- randAlphaNum 50 | nospace | b64enc }}
{{- end }}

{{/*
Define the django-secret name
*/}}
{{- define "itvr-backend.django-secret" -}}
itvr-django-secret
{{- end }}

{{/*
Define the django-salt name
*/}}
{{- define "itvr-backend.django-salt" -}}
itvr-django-salt
{{- end }}