{{/*

version: 1.0.0
appVersion: "1.6.0"
nameOverride: ""
fullnameOverride: ""

1. deploy PR based
pr225 is the .Release.Name
Set below to to be empty string in values file
  nameOverride: ""
  fullnameOverride: ""
imageTools value should be the build PR image in tools project
Run the below command
helm template -f ./values-dev.yaml pr225 .
  name: pr225-itvr-backend
  labels:
    helm.sh/chart: itvr-backend-1.0.0
    app.kubernetes.io/name: itvr-backend
    app.kubernetes.io/instance: pr225
    app.kubernetes.io/version: "1.6.0"
    app.kubernetes.io/managed-by: Helm

2. only build racking PR
helm template -f ./values-dev.yaml itvr-backend .
  name: itvr-backend
  labels:
    helm.sh/chart: itvr-backend-1.0.0
    app.kubernetes.io/name: itvr-backend
    app.kubernetes.io/instance: itvr-backend
    app.kubernetes.io/version: "1.6.0"
    app.kubernetes.io/managed-by: Helm

it makes PR based pipeline possible for dev environment

At this moment, when deploy on Dev, Test and Prod, set the value for nameOverride and fullnameOverride to be itvr-backend

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
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
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
Define the route name
*/}}
{{- define "itvr-backend.routeName" -}}
{{- include "itvr-backend.fullname" . }}
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
itvr-django-secret-{{ .Values.envName }}
{{- end }}

{{/*
Define the django-salt name
*/}}
{{- define "itvr-backend.django-salt" -}}
itvr-django-salt-{{ .Values.envName }}
{{- end }}