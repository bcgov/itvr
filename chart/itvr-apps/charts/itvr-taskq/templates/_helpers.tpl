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
{{- define "itvr-task-queue.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
The .Release.Name is the first parameter of command helm install itvr-task-queue
*/}}
{{- define "itvr-task-queue.fullname" -}}
{{- .Release.Name }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "itvr-task-queue.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels:
app.kubernetes.io/managed-by would be Helm
*/}}
{{- define "itvr-task-queue.labels" -}}
helm.sh/chart: {{ include "itvr-task-queue.chart" . }}
{{ include "itvr-task-queue.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "itvr-task-queue.selectorLabels" -}}
app.kubernetes.io/name: {{ include "itvr-task-queue.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Define the deploymentconfig name
*/}}
{{- define "itvr-task-queue.deploymentconfigName" -}}
{{- include "itvr-task-queue.fullname" . }}
{{- end }}

