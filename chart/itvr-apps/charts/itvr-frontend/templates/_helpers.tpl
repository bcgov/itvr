{{/*
The labels for all components:
  labels:
    helm.sh/chart: itvr-frontend-1.0.0
    app.kubernetes.io/name: itvr-frontend
    app.kubernetes.io/instance: itvr-frontend-dev-1977
    app.kubernetes.io/version: "1.17.0"
    app.kubernetes.io/managed-by: Helm

The selector lables:
  selector:
    app.kubernetes.io/name: itvr-frontend
    app.kubernetes.io/instance: itvr-frontend-dev-1977
*/}}


{{/*
Expand the name of the chart.
set the value to be .Chart.NAme if Values.nameOverride is not given
In values file, we don't provide nameOverride
So finally: itvr-frontend.name=itve-frontend
*/}}
{{- define "itvr-frontend.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
.Release.Name is the one in the helm install command, it is one of the following:
    itvr-frontend-dev
    itvr-frontend-dev-<pr number>
    itvr-frontend-test
    itvr-frontend-prod 
*/}}
{{- define "itvr-frontend.fullname" -}}
{{- .Release.Name }}
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
{{- include "itvr-frontend.fullname" . }}
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
{{- include "itvr-frontend.name" . }}
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