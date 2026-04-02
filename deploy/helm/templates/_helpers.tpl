{{/*
Expand the name of the chart.
*/}}
{{- define "evidently-ui.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "evidently-ui.fullname" -}}
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
{{- define "evidently-ui.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "evidently-ui.labels" -}}
helm.sh/chart: {{ include "evidently-ui.chart" . }}
{{ include "evidently-ui.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "evidently-ui.selectorLabels" -}}
app.kubernetes.io/name: {{ include "evidently-ui.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "evidently-ui.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "evidently-ui.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Workspace path: s3, simplecache::s3, or local
*/}}
{{- define "evidently-ui.workspacePath" -}}
{{- if .Values.s3.enabled -}}
{{- if (index (.Values.s3.cache | default dict) "enabled") }}simplecache::{{ end }}s3://{{ .Values.s3.bucketName }}/{{ .Values.s3.path }}
{{- else -}}
/app/workspace
{{- end -}}
{{- end }}

{{/*
Whether S3 cache is enabled
*/}}
{{- define "evidently-ui.s3CacheEnabled" -}}
{{- (index (.Values.s3.cache | default dict) "enabled") -}}
{{- end }}
