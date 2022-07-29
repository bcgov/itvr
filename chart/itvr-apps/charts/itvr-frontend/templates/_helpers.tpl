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
  name: pr225-itvr-frontend
  labels:
    helm.sh/chart: itvr-frontend-1.0.0
    app.kubernetes.io/name: itvr-frontend
    app.kubernetes.io/instance: pr225
    app.kubernetes.io/version: "1.6.0"
    app.kubernetes.io/managed-by: Helm

2. only build racking PR
helm template -f ./values-dev.yaml itvr-frontend .
  name: itvr-frontend
  labels:
    helm.sh/chart: itvr-frontend-1.0.0
    app.kubernetes.io/name: itvr-frontend
    app.kubernetes.io/instance: itvr-frontend
    app.kubernetes.io/version: "1.6.0"
    app.kubernetes.io/managed-by: Helm

it makes PR based pipeline possible for dev environment

At this moment, when deploy on Dev, Test and Prod, set the value for nameOverride and fullnameOverride to be itvr-frontend

*/}}


{{/*
Expand the name of the chart.
*/}}
{{- define "itvr-frontend.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
The .Release.Name is the first parameter of command helm install itvr-frontend
*/}}
{{- define "itvr-frontend.fullname" -}}
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
{{- define "itvr-frontend.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels:
app.kubernetes.io/managed-by would be Helm
*/}}
{{- define "itvr-frontend.labels" -}}
helm.sh/chart: {{ include "itvr-frontend.chart" . }}
{{ include "itvr-frontend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "itvr-frontend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "itvr-frontend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "itvr-frontend.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "itvr-frontend.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Define the configmap name
*/}}
{{- define "itvr-frontend.configmapName" -}}
{{- include "itvr-frontend.fullname" . }}-features
{{- end }}

{{/*
Define the deploymentconfig name
*/}}
{{- define "itvr-frontend.deploymentconfigName" -}}
{{- include "itvr-frontend.fullname" . }}
{{- end }}

{{/*
Define the deploymentconfig name
*/}}
{{- define "itvr-frontend.imagestreamName" -}}
{{- include "itvr-frontend.fullname" . }}
{{- end }}

{{/*
Define the service name
*/}}
{{- define "itvr-frontend.serviceName" -}}
{{- include "itvr-frontend.fullname" . }}
{{- end }}


{{/*
Define the route name
*/}}
{{- define "itvr-frontend.routeName" -}}
{{- include "itvr-frontend.fullname" . }}
{{- end }}