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
  name: pr225-itvr-taskq
  labels:
    helm.sh/chart: itvr-taskq-1.0.0
    app.kubernetes.io/name: itvr-taskq
    app.kubernetes.io/instance: pr225
    app.kubernetes.io/version: "1.6.0"
    app.kubernetes.io/managed-by: Helm

2. only build racking PR
helm template -f ./values-dev.yaml itvr-taskq .
  name: itvr-taskq
  labels:
    helm.sh/chart: itvr-taskq-1.0.0
    app.kubernetes.io/name: itvr-taskq
    app.kubernetes.io/instance: itvr-taskq
    app.kubernetes.io/version: "1.6.0"
    app.kubernetes.io/managed-by: Helm

it makes PR based pipeline possible for dev environment

At this moment, when deploy on Dev, Test and Prod, set the value for nameOverride and fullnameOverride to be itvr-taskq

*/}}


{{/*
Expand the name of the chart.
*/}}
{{- define "itvr-taskq.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
The .Release.Name is the first parameter of command helm install itvr-taskq
*/}}
{{- define "itvr-taskq.fullname" -}}
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
{{- define "itvr-taskq.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels:
app.kubernetes.io/managed-by would be Helm
*/}}
{{- define "itvr-taskq.labels" -}}
helm.sh/chart: {{ include "itvr-taskq.chart" . }}
{{ include "itvr-taskq.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "itvr-taskq.selectorLabels" -}}
app.kubernetes.io/name: {{ include "itvr-taskq.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Define the deploymentconfig name
*/}}
{{- define "itvr-taskq.deploymentconfigName" -}}
{{- include "itvr-taskq.fullname" . }}
{{- end }}

{{/*
Define the deploymentconfig name
*/}}
{{- define "itvr-taskq.imagestreamName" -}}
{{- include "itvr-taskq.fullname" . }}
{{- end }}

{{/*
Define the django-secret name
*/}}
{{- define "itvr-taskq.django-secret" -}}
itvr-django-secret-{{ .Values.envName }}
{{- end }}

{{/*
Define the django-salt name
*/}}
{{- define "itvr-taskq.django-salt" -}}
itvr-django-salt-{{ .Values.envName }}
{{- end }}